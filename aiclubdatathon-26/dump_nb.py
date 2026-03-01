import json, sys

with open('study-notebook.ipynb', 'r', encoding='utf-8') as f:
    content = f.read()

# Write as UTF-8
with open('study_nb_utf8.txt', 'w', encoding='utf-8') as f:
    data = json.loads(content)
    for i, cell in enumerate(data['cells']):
        src = ''.join(cell['source'])
        f.write(f'\n{"="*60}\nCell {i} [{cell["cell_type"]}]\n{"="*60}\n')
        f.write(src + '\n')

print("done")
