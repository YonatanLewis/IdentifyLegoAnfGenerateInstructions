import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR     = PROJECT_ROOT / "data"
RAW_DIR      = DATA_DIR / "raw"
IMAGES_DIR   = DATA_DIR / "images"
DATASETS_DIR = DATA_DIR / "datasets"
MODELS_DIR   = PROJECT_ROOT / "models"

# Create only the folders we actually use
for d in [DATA_DIR, RAW_DIR, IMAGES_DIR, DATASETS_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

REBRICKABLE_API_KEY = os.getenv("REBRICKABLE_API_KEY", "")
REBRICKABLE_BASE = "https://rebrickable.com/api/v3/lego"

TOP_N_PARTS           = int(os.getenv("TOP_N_PARTS", "150"))
MIN_COLORS_PER_PART   = int(os.getenv("MIN_COLORS_PER_PART", "2"))
BATCH_SIZE            = int(os.getenv("BATCH_SIZE", "32"))
NUM_EPOCHS            = int(os.getenv("NUM_EPOCHS", "10"))
LR                    = float(os.getenv("LR", "1e-3"))
IMAGE_SIZE            = int(os.getenv("IMAGE_SIZE", "224"))
VAL_SPLIT             = float(os.getenv("VAL_SPLIT", "0.15"))
SEED                  = int(os.getenv("SEED", "42"))
DEVICE                = os.getenv("DEVICE", "cuda" if os.getenv("CUDA", "1") == "1" else "cpu")
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR     = PROJECT_ROOT / "data"
RAW_DIR      = DATA_DIR / "raw"
IMAGES_DIR   = DATA_DIR / "images"
DATASETS_DIR = DATA_DIR / "datasets"
MODELS_DIR   = PROJECT_ROOT / "models"

# Create only the folders we actually use
for d in [DATA_DIR, RAW_DIR, IMAGES_DIR, DATASETS_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

REBRICKABLE_API_KEY = os.getenv("REBRICKABLE_API_KEY", "")
REBRICKABLE_BASE = "https://rebrickable.com/api/v3/lego"

TOP_N_PARTS           = int(os.getenv("TOP_N_PARTS", "150"))
MIN_COLORS_PER_PART   = int(os.getenv("MIN_COLORS_PER_PART", "2"))
BATCH_SIZE            = int(os.getenv("BATCH_SIZE", "32"))
NUM_EPOCHS            = int(os.getenv("NUM_EPOCHS", "10"))
LR                    = float(os.getenv("LR", "1e-3"))
IMAGE_SIZE            = int(os.getenv("IMAGE_SIZE", "224"))
VAL_SPLIT             = float(os.getenv("VAL_SPLIT", "0.15"))
SEED                  = int(os.getenv("SEED", "42"))
DEVICE                = os.getenv("DEVICE", "cuda" if os.getenv("CUDA", "1") == "1" else "cpu")
