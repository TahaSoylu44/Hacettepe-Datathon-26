import json

with open('model_v2.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and cell.get('outputs'):
        for out in cell['outputs']:
            otype = out.get('output_type', '')
            if otype == 'stream':
                txt = ''.join(out.get('text', []))
                if txt.strip():
                    print(f'[Cell {i} stdout]\n{txt[:800]}\n')
            elif otype in ('execute_result', 'display_data'):
                data = out.get('data', {})
                txt = ''.join(data.get('text/plain', []))
                if txt.strip():
                    print(f'[Cell {i} result]\n{txt[:800]}\n')
