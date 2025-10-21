from typing import Tuple
import torch
import torch.nn as nn
import torchvision.models as models

class LegoMultiTask(nn.Module):
    def __init__(self, num_parts: int, num_colors: int, dropout: float = 0.2):
        super().__init__()
        backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.features = nn.Sequential(*list(backbone.children())[:-1])
        feat_dim = backbone.fc.in_features
        self.head_part = nn.Sequential(nn.Dropout(dropout), nn.Linear(feat_dim, num_parts))
        self.head_color = nn.Sequential(nn.Dropout(dropout), nn.Linear(feat_dim, num_colors))

    def forward(self, x) -> Tuple[torch.Tensor, torch.Tensor]:
        z = self.features(x)
        z = z.flatten(1)
        logits_part = self.head_part(z)
        logits_color = self.head_color(z)
        return logits_part, logits_color
