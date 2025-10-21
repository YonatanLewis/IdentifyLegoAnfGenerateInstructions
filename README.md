


# 1. Create and activate a virtual environment, do not neccessery need to use this.
python -m venv .venv
.venv\Scripts\activate

# 2. Install everything needed
pip install -r requirements.txt

# 3. Add your Rebrickable API key (keep the quotes)
#This code has my API key already
$env:REBRICKABLE_API_KEY="5b66d38214c92e0ed8b8012df59fabaf"

# 4. Prepare data and images (only needed once)
python scripts/prepare_common_parts.py --csv data/raw/inventory_parts.csv --top 150
python scripts/download_images.py --parts data/datasets/common_parts.txt

# 5. Train the AI model
python scripts/train_model.py

Add your own photos under `data/images/<part_num>/<color_id>/...` and retrain.
