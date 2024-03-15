import os
import wandb
import torch
from torch.utils.data import DataLoader
from torch.optim import Optimizer
from tempfile import TemporaryDirectory
from tqdm import tqdm

from utils import init_logging, ConfusionMatrix

log = init_logging('DEBUG')

def train_model(
        model,
        dataloaders: dict[str, DataLoader],
        criterion,
        optimizer: Optimizer,
        classes: list[str] = ['NORMAL', 'PNEUMONIA'],
        device: torch.device = 'cuda' if torch.cuda.is_available() else 'cpu',
        scheduler = None,
        num_epochs: int=25):
    
    experiment = wandb.init(project='Deeplify', resume='allow', anonymous='must')
    experiment.config.update(
        dict(epochs=num_epochs,
             classes=classes,
             save_checkpoint=True,)
    )

    best_metric = 0
    cm = ConfusionMatrix(classes.index('PNEUMONIA'))
    with TemporaryDirectory() as tempdir:
        best_model_params_path = os.path.join(tempdir, 'best_model_params.pt')

        for epoch in range(1, num_epochs+1):
            log.info(f"Starting epoch: {epoch}")
            
            for phase in ['train', 'valid']:
                if phase == 'train': 
                    model.train()
                else:
                    model.eval()

                running_loss = 0.0
                cm.reset()

                for batch in tqdm(dataloaders[phase], desc=f"Phase {phase}"):
                    image, label = batch
                    image = image.to(device, dtype=torch.float)
                    label = label.to(device)

                    optimizer.zero_grad()
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(image)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, label)

                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    if scheduler is not None and phase == 'train': scheduler.step()
                    
                    # statistics
                    running_loss += loss.item() * image.size(0)
                    cm.append(preds, label.data)
                    
                epoch_loss = running_loss / len(dataloaders[phase])

                log.info(f'{phase} Loss: {epoch_loss:.4f} Acc: {cm.accuracy:.4f}')

                # deep copy the model
                if phase == 'valid' and cm.accuracy > best_metric:
                    best_metric = cm.accuracy
                    torch.save(model.state_dict(), best_model_params_path)
                
                lr = optimizer.param_groups[0]['lr']
                experiment.log({
                    f'{phase} learning rate': lr,
                    f'{phase} loss': epoch_loss,
                    f'{phase} precision': cm.precision,
                    f'{phase} recall': cm.recall,
                    f'{phase} accuracy': cm.accuracy,
                    f'{phase} epoch': epoch,
                    f'{phase} images': wandb.Image(image[0].cpu(), caption=f"gt {classes[label[0]]} | pred {classes[preds[0]]}"),
                })
        
        model.load_state_dict(torch.load(best_model_params_path))
    return model