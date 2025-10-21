import random
from typing import Dict
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
import torchvision.transforms as T
from .config import IMAGE_SIZE, BATCH_SIZE, VAL_SPLIT, SEED

random.seed(SEED)

class LegoDataset(Dataset):
    def __init__(self, df: pd.DataFrame, part2idx: Dict[str,int], color2idx: Dict[int,int], train: bool):
        self.df = df.reset_index(drop=True)
        self.part2idx = part2idx
        self.color2idx = color2idx
        if train:
            self.t = T.Compose([
                T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
                T.RandomHorizontalFlip(),
                T.RandomRotation(10),
                T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.02),
                T.ToTensor(),
                T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]),
            ])
        else:
            self.t = T.Compose([
                T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
                T.ToTensor(),
                T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]),
            ])

    def __len__(self): return len(self.df)
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img = Image.open(row.image_path).convert("RGB")
        x = self.t(img)
        part_idx = self.part2idx[row.part_num]
        color_idx = self.color2idx[int(row.color_id)]
        return x, part_idx, color_idx

def split_dataframe(df: pd.DataFrame):
    df = df.sample(frac=1.0, random_state=SEED)
    n_val = max(1, int(len(df) * VAL_SPLIT))
    return df.iloc[n_val:], df.iloc[:n_val]

def make_loaders(df: pd.DataFrame, part2idx, color2idx):
    train_df, val_df = split_dataframe(df)
    train_ds = LegoDataset(train_df, part2idx, color2idx, train=True)
    val_ds = LegoDataset(val_df, part2idx, color2idx, train=False)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)
    return train_loader, val_loader, train_df, val_df
