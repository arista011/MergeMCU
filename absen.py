import os
import re
import pandas as pd

# === KONFIGURASI ===
excel_path = "DATA.xlsx"    # File Excel sumber
folder_path = "hasil/"      # Folder PDF hasil
output_path = "ABSEN - STATUS.xlsx"  # File hasil update

# === BACA EXCEL ===
df = pd.read_excel(excel_path, dtype=str)  # baca semua kolom sebagai string
df = df.fillna("")  # ganti NaN jadi string kosong

# Pastikan kolom yang diperlukan ada
required_cols = {"NIK", "STATUS"}
if not required_cols.issubset(df.columns):
    raise Exception(f"Kolom {required_cols} tidak ditemukan di Excel!")

# Bersihkan format NIK dari ".0" dan spasi
df["NIK"] = df["NIK"].str.replace(r"\.0$", "", regex=True).str.strip()

# === Ambil daftar NIK dari file PDF di folder ===
nik_folder = []
for fname in os.listdir(folder_path):
    if fname.lower().endswith(".pdf"):
        match = re.match(r"(\d+)", fname)  # ambil angka di depan nama file
        if match:
            nik_folder.append(match.group(1))

# === Update kolom STATUS ===
df["STATUS"] = df["NIK"].apply(lambda nik: "X" if nik in nik_folder else "0")

# === Simpan hasil ke file baru ===
df.to_excel(output_path, index=False)

print("✅ Proses selesai!")
print(f"File hasil disimpan ke: {output_path}")
