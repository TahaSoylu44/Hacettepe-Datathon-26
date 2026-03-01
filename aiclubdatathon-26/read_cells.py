import json

with open('study-notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Print cell 9 (create_features) and cell 28 (training) in full
for i in [9, 16, 21, 22, 26, 28, 29, 35, 37, 39]:
    if i < len(nb['cells']):
        cell = nb['cells'][i]
        src = ''.join(cell['source'])
        print(f'\n{"="*60}')
        print(f'Cell {i} [{cell["cell_type"]}]')
        print('='*60)
        print(src)
