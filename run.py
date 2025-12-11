import os, re
from datetime import datetime
import pandas as pd
import fitz
import subprocess
from PIL import Image
from tqdm import tqdm

# === KONFIGURASI ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "DATA.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "hasil")
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_EXT = (".jpg", ".jpeg", ".png")
DOC_EXT = (".pdf",) + IMG_EXT
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
steps = [
    ("STEP 1: Rename file LAB",        "lab.py"),
    ("STEP 2: Rename file NAME",       "name.py"),
    # ("STEP 3: Rename file NAME",       "logo-pdf.py"),
    # ("STEP 3: Rename file NAME",       "logo-jpg.py"),

]
for title, script in steps:
    print(f"\n=== {title} ===")
    subprocess.run(["python", os.path.join(BASE_DIR, script)])

# === CACHING FILE DI SEMUA FOLDER ===
FOLDERS_ALL = ["a-pdf","lab","f-ro","e-ro","f-ekg","e-ekg","f-spiro","e-spiro","e-audio","f-tread","e-tread"]
file_index = {folder: {} for folder in FOLDERS_ALL}

for folder in FOLDERS_ALL:
    path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(path):
        continue
    for fname in os.listdir(path):
        low = fname.lower()
        if not low.endswith(DOC_EXT): 
            continue
        nik = low.split(" -")[0]
        file_index[folder][nik] = os.path.join(path, fname)

def find_file(folder, nik):
    nik_low = nik.lower()
    folder_dict = file_index.get(folder, {})
    for key in folder_dict:
        if key == nik_low or key.lstrip("0") == nik_low.lstrip("0"):
            return folder_dict[key]
    return None

def merge_files(nik, nama, folders):
    merged_pdf = fitz.open()
    missing = []
    for folder in folders:
        fpath = find_file(folder, nik)
        if not fpath:
            missing.append(folder)
            continue
        try:
            if fpath.lower().endswith(IMG_EXT):
                img = Image.open(fpath).convert("RGB")
                img_bytes = img.tobytes()
                rect = fitz.Rect(0, 0, *img.size)
                pdf_img = fitz.open()
                page = pdf_img.new_page(width=rect.width, height=rect.height)
                page.insert_image(rect, filename=fpath)
                merged_pdf.insert_pdf(pdf_img)
                pdf_img.close()
            else:
                with fitz.open(fpath) as src:
                    merged_pdf.insert_pdf(src)
        except Exception as e:
            missing.append(f"{folder} (error: {e})")

    out_name = f"{nik} - {nama}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    if merged_pdf.page_count > 0:
        merged_pdf.save(out_path)
        merged_pdf.close()
        return missing, out_path
    else:
        merged_pdf.close()
        return FOLDERS_ALL, None

# === BACA EXCEL DAN PROSES ===
df = pd.read_excel(DATA_PATH, dtype=str, keep_default_na=False)
for col in ["STATUS", "FILE_HILANG"]:
    if col not in df.columns:
        df[col] = ""

for i, row in tqdm(df.iterrows(), total=len(df), desc="Proses pasien"):
    nik = str(row.get("NIK", "")).strip()
    nama = str(row.get("NAMA", "")).strip()
    ekg   = str(row.get("EKG", "0")).strip()
    spiro = str(row.get("Spiro", "0")).strip()
    audio = str(row.get("Audio", "0")).strip()
    tread = str(row.get("Tread", "0")).strip()

    base = ["a-pdf","lab","f-ro","e-ro"]
    folders = base.copy()
    if ekg   == "1": folders += ["f-ekg","e-ekg"]
    if spiro == "1": folders += ["f-spiro","e-spiro"]
    if audio == "1": folders += ["e-audio"]
    if tread == "1": folders += ["f-tread","e-tread"]
    
    missing, out = merge_files(nik, nama, folders)
    if not missing:
        df.at[i, "STATUS"] = "COMPLETE"
        df.at[i, "FILE_HILANG"] = "-"
    else:
        df.at[i, "STATUS"] = "FILE HILANG"
        df.at[i, "FILE_HILANG"] = ", ".join(missing)

# === SIMPAN KE FILE BARU ===
status_file = os.path.join(OUTPUT_DIR, "ABSEN-STATUS.xlsx")
df.to_excel(status_file, index=False)

print(f"\n✅ Update selesai.")
print(f"Status ditulis ke: {status_file}")
print(f"Hasil PDF tersimpan di folder: {OUTPUT_DIR}")
