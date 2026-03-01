import json

with open('study-notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Tüm hücreleri tara ve test ile ilgili sorunları düzelt
for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])

    # Cell 15: test_csv ilk yüklenme (sadece okuma, index yok)
    if 'test_csv = pd.read_csv("test.csv")' in src and 'ztimestamp' not in src and 'set_index' not in src:
        new_src = (
            'test_csv = pd.read_csv("test.csv")\n'
            '# ztimestamp veya timestamp sütununu index yap\n'
            'ts_col = "ztimestamp" if "ztimestamp" in test_csv.columns else "timestamp"\n'
            'test_csv = test_csv.set_index(ts_col)\n'
            'test_csv.index = pd.to_datetime(test_csv.index, format="ISO8601", utc=True)\n'
            'test_csv = test_csv.sort_index()\n'
            'test_csv\n'
        )
        nb['cells'][idx]['source'] = [new_src]
        nb['cells'][idx]['outputs'] = []
        nb['cells'][idx]['execution_count'] = None
        print(f"✅ Cell {idx} (test_csv ilk yükleme) düzeltildi")

    # Cell 37: test_csv ikinci yüklenme (set_index('ztimestamp') hatası)
    if 'test_csv = pd.read_csv("test.csv")' in src and 'ztimestamp' in src:
        new_src = (
            'test_csv = pd.read_csv("test.csv")\n'
            '# ztimestamp veya timestamp sütununu index yap\n'
            'ts_col = "ztimestamp" if "ztimestamp" in test_csv.columns else "timestamp"\n'
            'test_csv = test_csv.set_index(ts_col)\n'
            'test_csv.index = pd.to_datetime(test_csv.index, format="ISO8601", utc=True)\n'
            'test_csv = test_csv.sort_index()\n'
        )
        nb['cells'][idx]['source'] = [new_src]
        nb['cells'][idx]['outputs'] = []
        nb['cells'][idx]['execution_count'] = None
        print(f"✅ Cell {idx} (test_csv yeniden yükleme) düzeltildi")

    # Cell 39: test prediction — remaining_sec ve proc_dur NaN olabilir, fillna yap
    if 'X_test_final = test_and_history.tail' in src:
        new_src = (
            'history_tail = df.tail(10)\n'
            'test_and_history = pd.concat([history_tail, test_csv])\n'
            'test_and_history = create_features(test_and_history)\n'
            'test_and_history = add_lags(test_and_history)\n'
            'X_test_final = test_and_history.tail(len(test_csv))[FEATURES].fillna(0)\n'
            'test_predictions = reg_final.predict(X_test_final)\n'
            'print(f"Test tahmin tamamlandi: {len(test_predictions):,} satir")\n'
        )
        nb['cells'][idx]['source'] = [new_src]
        nb['cells'][idx]['outputs'] = []
        nb['cells'][idx]['execution_count'] = None
        print(f"✅ Cell {idx} (test prediction) düzeltildi - fillna(0) + history 10 satır")

    # sample_submission_sample -> sample_submission.csv
    if 'sample_submission_sample.csv' in src:
        import os
        # Hangi dosya var kontrol et
        new_src = src.replace('sample_submission_sample.csv', 'sample_submission.csv')
        nb['cells'][idx]['source'] = [new_src]
        nb['cells'][idx]['outputs'] = []
        nb['cells'][idx]['execution_count'] = None
        print(f"✅ Cell {idx} — sample_submission_sample.csv -> sample_submission.csv")

with open('study-notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\n✅ Tüm düzeltmeler uygulandı")
