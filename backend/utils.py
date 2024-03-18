import logging, os
from pathlib import Path
from typing import Literal
import torch
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import v2 as transforms

def init_logging(log_level='DEBUG'):
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(module)-10s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
    rootLogger = logging.getLogger("Deeplify")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(log_level)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(log_level)
    return rootLogger

class ConfusionMatrix:
    """Manager of the evaluation criterion"""
    def __init__(self, positive_idx:int=1) -> None:
        """@param positive_idx: the index of the class that shall be considered the positive.
        Can be given by `class_to_idx['pneumonia']`"""
        self.reset()
        self.positive_class = positive_idx

    def append(self, prediction:torch.Tensor, ground_truth: torch.Tensor) -> None:
        """Updates counters based on the similarities between prediction and ground truth.
           Considers 1 as positive and 0 as negative."""
        positive = prediction == self.positive_class
        negative = prediction != self.positive_class
        true = prediction == ground_truth
        false = prediction != ground_truth

        self.true_positive += torch.sum(torch.logical_and(true, positive))
        self.false_positive += torch.sum(torch.logical_and(false, positive))
        self.false_negative += torch.sum(torch.logical_and(false, negative))
        self.true_negative += torch.sum(torch.logical_and(true, negative))

    def reset(self) -> None:
        """Reset counters to zero"""
        self.true_positive: int = 0
        self.false_positive: int = 0
        self.false_negative: int = 0
        self.true_negative: int = 0

    @property
    def accuracy(self) -> float:
        """True / (True + False)"""
        return (self.true_negative + self.true_positive) / (self.true_negative + self.true_positive + self.false_negative + self.false_positive)
    
    @property
    def recall(self) -> float:
        """TP / (TP + FN)"""
        return self.true_positive / (self.true_positive + self.false_negative)
    
    @property
    def precision(self) -> float:
        """TP / (TP + FP)"""
        return self.true_positive / (self.true_positive + self.false_positive)

def mount_dataset(folder_path:str, batch_size:int=4, num_workers:int=4, image_size=(768, 1024), image_resize_scale=(980, 1340)) -> tuple[list[str], dict[Literal['train', 'valid', 'test'], DataLoader]]:
    """From the dataset path, returns a dictionary with the dataloaders of training and validation.
    @return list of classes, a dict of dataloaders"""
    augmented_transformations = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize(image_resize_scale),
        transforms.CenterCrop(image_size),
        transforms.RandomRotation(20),
        transforms.ToImage(),
        transforms.ToDtype(torch.float32, scale=True)
    ])

    standard_transformation = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize(image_resize_scale),
        transforms.CenterCrop(image_size),
        transforms.ToImage(),
        transforms.ToDtype(torch.float32, scale=True)
    ])

    trainval_set = ImageFolder(str(Path(folder_path) / 'train'), augmented_transformations)
    train_set, val_set = random_split(trainval_set, (.8, .2))
    test_set = ImageFolder(str(Path(folder_path) / 'test'), standard_transformation)

    dataloaders = {k: DataLoader(s, batch_size=batch_size, shuffle=True, num_workers=num_workers) for k, s in zip(['train', 'valid', 'test'], [train_set, val_set, test_set])}
    return test_set.classes, dataloaders