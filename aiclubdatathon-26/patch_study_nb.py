import json

with open('study-notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# ── DEĞİŞİKLİK 1: Cell 9 — create_features düzelt ─────────────────
# Eski: elapsed_time = endtime - starttime (sabit)
# Yeni: elapsed_sec = timestamp - starttime (değişken)
#        remaining_sec = endtime - timestamp (değişken)
#        elapsed_time = proc_dur (toplam, eski adıyla)

new_create_features = [
    "def create_features(df):\n",
    "    df = df.copy()\n",
    "    df['starttime'] = pd.to_datetime(df['starttime'], format='ISO8601', utc=True)\n",
    "    df['endtime']   = pd.to_datetime(df['endtime'],   format='ISO8601', utc=True)\n",
    "\n",
    "    # index = timestamp (UTC)\n",
    "    ts = df.index\n",
    "    if not hasattr(ts, 'tz') or ts.tz is None:\n",
    "        ts = ts.tz_localize('UTC')\n",
    "\n",
    "    # --- DUZELTME: elapsed_time artik timestamp - starttime (her saniye degisir) ---\n",
    "    df['elapsed_time']  = (ts - df['starttime']).dt.total_seconds().clip(lower=0)\n",
    "\n",
    "    # --- YENI: remaining_sec = endtime - timestamp (kalan sure) ---\n",
    "    df['remaining_sec'] = (df['endtime'] - ts).dt.total_seconds().clip(lower=0)\n",
    "\n",
    "    # --- YENI: proc_dur = toplam proses suresi (sabit, eski elapsed_time'in karsiligi) ---\n",
    "    df['proc_dur']      = (df['endtime'] - df['starttime']).dt.total_seconds()\n",
    "\n",
    "    return df\n",
    "\n",
    "df = create_features(df)\n",
    "print('elapsed_time ornekleri (ilk 3, farkli olmalı):')\n",
    "print(df['elapsed_time'].head(3).values)\n",
    "print('remaining_sec ornekleri (ilk 3):')\n",
    "print(df['remaining_sec'].head(3).values)\n",
    "print('proc_dur (sabit olmali):')\n",
    "print(df['proc_dur'].head(3).values)"
]

nb['cells'][9]['source'] = new_create_features
nb['cells'][9]['outputs'] = []
nb['cells'][9]['execution_count'] = None
print("✅ Cell 9 (create_features) güncellendi")


# ── DEĞİŞİKLİK 2: Cell 22 sonrasına yeni hücre ekle ────────────────
# bk_level > 0 filtresi
new_filter_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# --- DUZELTME: bk_level=0 satírlari puanlanmiyor, filtreliyoruz ---\n",
        "n_before = len(df)\n",
        "df = df[df['bk_level'] > 0].copy()\n",
        "n_after = len(df)\n",
        "print(f'bk_level=0 filtrelemesi: {n_before:,} -> {n_after:,} satir')\n",
        "print(f'Cikarilan satir: {n_before - n_after:,} ({(n_before-n_after)/n_before*100:.1f}%)')\n",
        "print(f'Kalan satirlar: {n_after:,}')"
    ]
}

# Cell 22'nin indexi: dropna hücresi
# Cell 22 sonrasına (index 23'e) yeni hücre ekle
nb['cells'].insert(23, new_filter_cell)
print("✅ Cell 23'e bk_level > 0 filtresi eklendi (eski hücreler 1 kayar)")


# ── DEĞİŞİKLİK 3: FEATURES listelerine remaining_sec ekle ─────────
# Cell 28 artık 29 oldu (insert yüzünden)
# Cell 35 artık 36 oldu

# Hücreleri tara, FEATURES listesi içeren kod hücrelerini bul ve güncelle
for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])

    # FEATURES listesi varsa remaining_sec ekle
    if ("FEATURES = ['target_lag3'" in src or "FEATURES = ['target_lag3'" in src) and 'elapsed_time' in src:
        old_feature_line = "            'ak_level', 'fabric_weight', 'bk_irtibat_valve']"
        new_feature_line = "            'ak_level', 'fabric_weight', 'bk_irtibat_valve',\n            'remaining_sec', 'proc_dur']"
        new_src = src.replace(old_feature_line, new_feature_line)
        if new_src != src:
            nb['cells'][idx]['source'] = [new_src]
            nb['cells'][idx]['outputs'] = []
            nb['cells'][idx]['execution_count'] = None
            print(f"✅ Cell {idx} — FEATURES listesine remaining_sec + proc_dur eklendi")

# Tüm hücrelerin output ve execution_count'unu temizle (temiz çalıştırma için)
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

with open('study-notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\n✅ study-notebook.ipynb güncellendi")
print(f"   Toplam hücre sayısı: {len(nb['cells'])}")
