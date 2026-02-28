import json, re

with open('eda_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Fix date parsing cell
old_lines = [
    "# Parse edecek tarih sütunları\n",
    "DATE_COLS = ['timestamp','starttime','endtime']\n",
    "\n",
    "print('⏳ Train yükleniyor...')\n",
    "train = pd.read_csv(TRAIN_PATH, parse_dates=DATE_COLS, low_memory=False)\n",
    "print(f'✅ Train: {train.shape[0]:,} satır × {train.shape[1]} sütun')\n",
    "\n",
    "print('⏳ Test yükleniyor...')\n",
    "test  = pd.read_csv(TEST_PATH,  parse_dates=DATE_COLS, low_memory=False)\n",
    "print(f'✅ Test : {test.shape[0]:,} satır × {test.shape[1]} sütun')\n",
    "\n",
    "sample = pd.read_csv(SAMPLE_PATH)\n",
    "print(f'✅ Sample submission sütunları: {list(sample.columns)}')"
]

new_lines = [
    "DATE_COLS = ['timestamp','starttime','endtime']\n",
    "\n",
    "print('⏳ Train yükleniyor...')\n",
    "train = pd.read_csv(TRAIN_PATH, low_memory=False)\n",
    "for c in DATE_COLS:\n",
    "    if c in train.columns:\n",
    "        train[c] = pd.to_datetime(train[c], format='mixed', utc=True)\n",
    "print(f'✅ Train: {train.shape[0]:,} satır × {train.shape[1]} sütun')\n",
    "\n",
    "print('⏳ Test yükleniyor...')\n",
    "test = pd.read_csv(TEST_PATH, low_memory=False)\n",
    "for c in DATE_COLS:\n",
    "    if c in test.columns:\n",
    "        test[c] = pd.to_datetime(test[c], format='mixed', utc=True)\n",
    "print(f'✅ Test : {test.shape[0]:,} satır × {test.shape[1]} sütun')\n",
    "\n",
    "sample = pd.read_csv(SAMPLE_PATH)\n",
    "print(f'✅ Sample submission sütunları: {list(sample.columns)}')"
]

fixed = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = cell['source']
        # Match by checking if the parse_dates line is present
        joined = ''.join(src)
        if 'parse_dates=DATE_COLS' in joined and 'read_csv(TRAIN_PATH' in joined:
            cell['source'] = new_lines
            # Clear previous outputs
            cell['outputs'] = []
            cell['execution_count'] = None
            fixed = True
            print('✅ Date-parse cell fixed.')
            break

if not fixed:
    print('⚠️  Target cell not found — checking all cells...')
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            print(f'  Cell {i}: {repr("".join(cell["source"])[:80])}')

# Also clear all outputs so the notebook is ready to execute fresh
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

with open('eda_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('✅ Notebook saved. Running nbconvert...')
