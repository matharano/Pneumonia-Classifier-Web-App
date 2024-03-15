import numpy as np
import wandb
import torch
from torch.nn import Softmax
from torch.utils.data import DataLoader
from tqdm import tqdm

from utils import ConfusionMatrix

@torch.no_grad
def evaluate(model:torch.nn, dataloader:DataLoader, device:torch.device, classes:list[str]=['NORMAL', 'PNEUMONIA'], threshold_step:float=.02) -> None:
    """Logs evaluation metrics (precision, recall, and accuracy) to wandb across 20 different thresholds"""
    pos = classes.index('PNEUMONIA')
    cm = ConfusionMatrix(pos)
    model.eval()
    softmax = Softmax(dim=1)
    for threshold in tqdm(np.arange(0, 1, threshold_step)):
        cm.reset()
        for images, labels in dataloader:
            images = images.to(device, dtype=torch.float)
            labels = labels.to(device)

            outputs = model(images)
            confs = softmax(outputs)
            cm.append(confs[:, pos] >= threshold, labels == pos)
        
        wandb.log({'test precision': cm.precision,
                   'test recall': cm.recall,
                   'test accuracy': cm.accuracy,
                   'test conf threshold': threshold})