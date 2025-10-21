# src/train.py  — minimal trainer (no reports)
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score
from tqdm import tqdm

from .config import DATASETS_DIR, MODELS_DIR, DEVICE, NUM_EPOCHS, LR
from .utils import make_loaders
from .model import LegoMultiTask


def train():
    index_csv = DATASETS_DIR / "index.csv"
    if not index_csv.exists():
        raise FileNotFoundError(f"Dataset index not found: {index_csv}")
    df = pd.read_csv(index_csv)
    if len(df) == 0:
        raise RuntimeError(
            "index.csv is empty. Run download_images.py first or add your own "
            "photos under data/images/<part>/<color>/"
        )

    parts = sorted(df.part_num.unique())
    colors = sorted(df.color_id.astype(int).unique())
    part2idx = {p: i for i, p in enumerate(parts)}
    color2idx = {c: i for i, c in enumerate(colors)}

    print(f"Using device: {DEVICE}")
    print(f"Classes — parts: {len(parts)}, colors: {len(colors)}")

    train_loader, val_loader, _, _ = make_loaders(df, part2idx, color2idx)

    model = LegoMultiTask(num_parts=len(parts), num_colors=len(colors)).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=LR)
    crit_part = nn.CrossEntropyLoss()
    crit_color = nn.CrossEntropyLoss()

    best_val = -1.0  # track best (acc_part + acc_color) / 2

    for epoch in range(1, NUM_EPOCHS + 1):
        # ---- train ----
        model.train()
        loss_sum = 0.0
        for x, y_part, y_color in tqdm(train_loader, desc=f"epoch {epoch} train"):
            x = x.to(DEVICE); y_part = y_part.to(DEVICE); y_color = y_color.to(DEVICE)
            opt.zero_grad()
            logits_part, logits_color = model(x)
            loss = crit_part(logits_part, y_part) + crit_color(logits_color, y_color)
            loss.backward()
            opt.step()
            loss_sum += loss.item() * x.size(0)
        train_loss = loss_sum / len(train_loader.dataset)

        # ---- validate ----
        model.eval()
        y_true_part, y_pred_part, y_true_color, y_pred_color = [], [], [], []
        with torch.no_grad():
            for x, yp, yc in tqdm(val_loader, desc=f"epoch {epoch} val"):
                x = x.to(DEVICE)
                lp, lc = model(x)
                y_true_part.extend(yp.numpy().tolist())
                y_true_color.extend(yc.numpy().tolist())
                y_pred_part.extend(lp.argmax(1).cpu().numpy().tolist())
                y_pred_color.extend(lc.argmax(1).cpu().numpy().tolist())

        acc_part = accuracy_score(y_true_part, y_pred_part)
        acc_color = accuracy_score(y_true_color, y_pred_color)
        val_score = (acc_part + acc_color) / 2.0

        print(f"Epoch {epoch} | train_loss={train_loss:.4f} | acc_part={acc_part:.3f} | acc_color={acc_color:.3f}")

        # save best only
        if val_score > best_val:
            best_val = val_score
            MODELS_DIR.mkdir(parents=True, exist_ok=True)
            torch.save(
                {"model_state": model.state_dict(), "parts": parts, "colors": colors},
                MODELS_DIR / "best.pt",
            )
            print(f"Saved new best model to {MODELS_DIR/'best.pt'} with val_score={val_score:.3f}")


if __name__ == "__main__":
    train()
