import json, sys

with open('study-notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'Toplam hucre: {len(nb["cells"])}\n')

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])
    ctype = cell['cell_type']
    sep = '='*70
    print(sep)
    print(f'[Cell {i}] type={ctype}')
    print(sep)
    # Print full source
    for line in src.splitlines():
        print(line)
    # Check outputs
    if cell.get('outputs'):
        for out in cell['outputs']:
            otype = out.get('output_type', '')
            if otype == 'error':
                print(f'\n  !!ERROR!! {out.get("ename")}: {out.get("evalue")}')
            elif otype == 'stream':
                txt = ''.join(out.get('text', []))
                if txt.strip():
                    print(f'\n  [stdout] {txt[:500]}')
            elif otype in ('execute_result', 'display_data'):
                data = out.get('data', {})
                txt = ''.join(data.get('text/plain', []))
                if txt.strip():
                    print(f'\n  [result] {txt[:500]}')
    print()
