import json
with open('eda_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

errors_found = False
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and cell.get('outputs'):
        for out in cell['outputs']:
            if out.get('output_type') == 'error':
                print(f'Cell {i} ERROR: {out.get("ename")} : {out.get("evalue")}')
                errors_found = True

if not errors_found:
    print('No errors found.')
