from abc import ABC, abstractmethod
from typing import Literal
import numpy as np
from PIL import Image
import torch, os
from torch.nn import Conv2d, Softmax
from torchvision.models import resnet18
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
                 weights_path:str = 'weights/Resnet-Adam(0.001)-batch(16).pth'
                 ) -> None:
        self.device = torch.device(device)
        self.classes = classes
        self.model = resnet18()
        self.model.conv1 = Conv2d(1, 64, kernel_size=(7,7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, len(self.classes), bias=True)
        self.model.load_state_dict(torch.load(os.path.abspath(weights_path), map_location=self.device))
        self.model = self.model.to(device, dtype=torch.float)
        self.softmax = Softmax(dim=0)
    
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
        confidence = weights.max()
        return inference, confidence