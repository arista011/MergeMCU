import os
import pandas as pd

# === KONFIGURASI ===
excel_file = "Data.xlsx"
folders = ["e-audio", "e-ekg", "e-ilo", "e-ro", "e-spiro", "f-ekg", "f-ilo", "f-ro", "f-spiro"]  # folder yang akan diproses
base_dir = os.path.dirname(os.path.abspath(__file__))

# === BACA DATA EXCEL ===
df = pd.read_excel(excel_file, dtype=str)
df = df.fillna("")

# Pastikan kolom penting ada
required_cols = {"MR", "NIK", "NAMA"}
if not required_cols.issubset(df.columns):
    raise Exception(f"❌ Kolom {required_cols} tidak ditemukan di file Excel!")

# Buat mapping MR -> (NIK, NAMA)
mapping = {
    str(row["MR"]).strip().lstrip("0"): (
        str(row["NIK"]).strip(),
        str(row["NAMA"]).strip()
    )
    for _, row in df.iterrows()
}

# === PROSES SETIAP FOLDER ===
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    if not os.path.isdir(folder_path):
        print(f"⚠️ Folder {folder} tidak ditemukan, dilewati.")
        continue

    print(f"\n=== Memproses folder: {folder} ===")

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        if not os.path.isfile(old_path):
            continue

        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext not in [".pdf", ".jpg"]:
            continue  # hanya rename PDF dan JPG

        # Ambil MR di awal nama file (sebelum tanda " - ")
        mr = name.split("-")[0].strip().lstrip("0")

        if mr in mapping:
            nik, nama = mapping[mr]
            new_name = f"{nik} - {nama}{ext}"
            new_path = os.path.join(folder_path, new_name)

            # Rename
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"✅ {filename} → {new_name}")
            else:
                print(f"⚠️ SKIP (sudah ada): {new_name}")
        else:
            print(f"❌ MR {mr} tidak ditemukan di Excel")

print("\n🎉 Selesai! Semua file sudah diubah namanya.")
