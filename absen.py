import os
import pandas as pd
import subprocess
from tqdm import tqdm

# === KONFIGURASI ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "DATA.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "hasil")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOC_EXT = (".pdf", ".jpg", ".jpeg", ".png")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
steps = [
    ("STEP 1: Rename file LAB",        "lab.py"),
    ("STEP 2: Rename file MINUS",      "minus.py"),
    ("STEP 3: Rename file NAME",       "name.py"),
]
for title, script in steps:
    print(f"\n=== {title} ===")
    subprocess.run(["python", os.path.join(BASE_DIR, script)])

# === CACHING SEMUA FILE DARI SETIAP FOLDER ===
FOLDERS_ALL = [
    "a-pdf","lab",
    "f-ro","e-ro","f-ekg","e-ekg","f-spiro","e-spiro",
    "e-audio","f-tread","e-tread"
]

file_index = {folder: {} for folder in FOLDERS_ALL}

for folder in FOLDERS_ALL:
    path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(path):
        continue
    for fname in os.listdir(path):
        if fname.lower().endswith(DOC_EXT):
            nik = fname.split(" -")[0].lower()
            file_index[folder][nik] = fname

def find_file(folder, nik):
    nik_low = nik.lower()
    folder_dict = file_index.get(folder, {})
    for key in folder_dict:
        if key == nik_low or key.lstrip("0") == nik_low.lstrip("0"):
            return folder_dict[key]
    return None

# === BACA EXCEL DAN TAMBAHKAN KOLOM PER FOLDER ===
df = pd.read_excel(DATA_PATH, dtype=str, keep_default_na=False)

folder_columns = {
    "lab": "LAB",
    "f-ro": "F-RO",
    "e-ro": "E-RO",
    "f-ekg": "F-EKG",
    "e-ekg": "E-EKG",
    "f-spiro": "F-SPIRO",
    "e-spiro": "E-SPIRO",
    "e-audio": "E-AUDIO",
    "e-tread": "E-TREAD",
    "f-tread": "F-TREAD"
}

# buat kolom kosong default "-"
for col in folder_columns.values():
    if col not in df.columns:
        df[col] = "-"

df["STATUS"] = ""

# === CEK FILE ===
for i, row in tqdm(df.iterrows(), total=len(df), desc="Checking files"):
    nik = str(row.get("NIK", "")).strip()
    ekg   = str(row.get("EKG", "0")).strip()
    spiro = str(row.get("Spiro", "0")).strip()
    audio = str(row.get("Audio", "0")).strip()
    tread = str(row.get("Tread", "0")).strip()

    base = ["a-pdf","lab","f-ro","e-ro"]
    folders = base.copy()
    if ekg   == "1": folders += ["f-ekg","e-ekg"]
    if spiro == "1": folders += ["f-spiro","e-spiro"]
    if audio == "1": folders += ["e-audio"]
    if audio == "1": folders += ["f-tread","e-tread"]

    missing = []
    for folder in folders:
        result = find_file(folder, nik)
        col = folder_columns[folder]
        if result:
            df.at[i, col] = folder
        else:
            df.at[i, col] = "-"
            missing.append(folder)

    df.at[i, "STATUS"] = "COMPLETE" if not missing else "FILE HILANG"

# === SIMPAN EXCEL HASIL ===
status_file = os.path.join(OUTPUT_DIR, "ABSEN.xlsx")
df.to_excel(status_file, index=False)

print("\n=== SELESAI ===")
print(f"Output Excel: {status_file}")
