from abc import ABC, abstractmethod
from typing import Literal
import numpy as np
from PIL import Image
import torch, os
from torch.nn import Conv2d, Softmax
from torchvision.models import resnet18, efficientnet_v2_s
from torchvision.transforms import v2 as transforms

class Model(ABC):
    """Abstract class of models to use for inference"""
    def __init__(self, device:Literal['cpu', 'cuda'] = 'cpu', classes:list[bool] = ['Normal', 'Pneumonia']) -> None:
        self.device = torch.device(device)
        self.classes = classes
        self.model: torch.nn

    @abstractmethod
    def preprocess(image:np.ndarray) -> np.ndarray:
        """Makes the appropriate transformations in the image to prepare it for inference."""
        ...

    @abstractmethod
    def infere(self, image:np.ndarray) -> tuple[str, float]:
        """Inferes whether the image presents pneumonia (True), or not (False), and the confidence of the evaluation"""
        ...

class ResNet():
    def __init__(self,
                 device:Literal['cpu', 'cuda'] = 'cpu',
                 classes:list[str] = ['Normal', 'Pneumonia'],
                 weights_path:str = 'backend/weights/Resnet-Adam(0.001)-batch(16).pth'
                 ) -> None:
        self.device = torch.device(device)
        self.classes = classes
        self.target_class_idx = self.classes.index('Pneumonia')  # The index of pneumonia
        self.model = resnet18()
        self.model.conv1 = Conv2d(1, 64, kernel_size=(7,7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, len(self.classes), bias=False)
        self.model.load_state_dict(torch.load(os.path.abspath(weights_path), map_location=self.device))
        self.model = self.model.to(device, dtype=torch.float)
        self.softmax = Softmax(dim=1)
    
    def preprocess(self, image:Image) -> np.ndarray:
        transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((980, 1340)),
            transforms.CenterCrop((768, 1024)),
            transforms.ToImage(),
            transforms.ToDtype(torch.float32, scale=True),
        ])
        transformed = transform(image)
        transformed = transformed.reshape((1, *transformed.shape))
        return transformed

    def infere(self, image:Image) -> tuple[str, float]:
        self.model.eval()
        processed_image = self.preprocess(image)
        weights:torch.Tensor = self.softmax(self.model(processed_image))
        inference:str = self.classes[weights.argmax()]
        probability = weights[0, self.target_class_idx]
        return inference, probability
    
class EfficientNet():
    def __init__(self,
                 device:Literal['cpu', 'cuda'] = 'cpu',
                 classes:list[str] = ['Normal', 'Pneumonia'],
                 weights_path:str = 'backend/weights/EfficientNetv2-SGD(0.001)-batch(4)-weightedloss.pth'
                 ) -> None:
        self.device = torch.device(device)
        self.classes = classes
        self.target_class_idx = self.classes.index('Pneumonia')  # The index of pneumonia
        self.model = efficientnet_v2_s()
        self.model.features[0][0] = Conv2d(1, 24, kernel_size=(3,3), stride=(2, 2), padding=(1,1), bias=False)
        self.model.classifier[1] = torch.nn.Linear(self.model.classifier[1].in_features, len(classes), bias=False)
        self.model.load_state_dict(torch.load(os.path.abspath(weights_path), map_location=self.device))
        self.model = self.model.to(device, dtype=torch.float)
        self.softmax = Softmax(dim=1)
    
    def preprocess(self, image:Image) -> np.ndarray:
        transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((490, 670)),
            transforms.CenterCrop((480, 480)),
            transforms.ToImage(),
            transforms.ToDtype(torch.float32, scale=True),
        ])
        transformed = transform(image)
        transformed = transformed.reshape((1, *transformed.shape))
        return transformed

    def infere(self, image:Image) -> tuple[str, float]:
        self.model.eval()
        processed_image = self.preprocess(image)
        weights:torch.Tensor = self.softmax(self.model(processed_image))
        probability = weights[0, self.target_class_idx]
        inference:str = self.classes[self.target_class_idx if weights[0, self.target_class_idx] >= .92 else not weights[0, self.target_class_idx]]
        return inference, probability