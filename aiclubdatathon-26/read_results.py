import json

with open('study-notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find score cell and feature importance cell
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    for out in cell.get('outputs', []):
        otype = out.get('output_type', '')
        txt = ''
        if otype == 'stream':
            txt = ''.join(out.get('text', []))
        elif otype in ('execute_result', 'display_data'):
            txt = ''.join(out.get('data', {}).get('text/plain', []))
        if 'Score across folds' in txt or ('importance' in txt and 'bk_target_level' in txt):
            print(f'=== Cell {i} ===')
            print(txt[:800])
            print()
