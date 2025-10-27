import os
import re
import fitz  # PyMuPDF
import csv
from datetime import datetime
from PIL import Image

# === KONFIGURASI FOLDER ===
base_dir = os.path.dirname(os.path.abspath(__file__))
folders = ["a-pdf","lab", "f-ro", "e-ro", "f-ekg", "e-ekg", "f-spiro", "e-spiro", "e-audio"]
output_folder = os.path.join(base_dir, "hasil")

os.makedirs(output_folder, exist_ok=True)

# === SIAPKAN LOG FILE ===
log_file = os.path.join(output_folder, f"log_merge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
log_data = []

# === AMBIL SEMUA NIK YANG ADA DI FOLDER ===
nik_set = set()
nik_pattern = re.compile(r"^(\d+)\s*-")  # ambil angka di depan sebelum tanda " -"

for folder in folders:
    path = os.path.join(base_dir, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    for file in os.listdir(path):
        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            match = nik_pattern.match(file)
            if match:
                nik_set.add(match.group(1))

nik_list = sorted(list(nik_set))
print(f"Ditemukan {len(nik_list)} NIK unik.\nMulai proses merge...\n")

# === PROSES MERGE BERDASARKAN NIK ===
for nik in nik_list:
    merged_pdf = fitz.open()
    missing_files = []
    success = False

    # cari nama lengkap dari folder RO
    ro_folder = os.path.join(base_dir, "e-ro")
    nama_pasien = None
    for file in os.listdir(ro_folder):
        if file.lower().startswith(f"{nik} -") and file.lower().endswith(".pdf"):
            # ambil bagian setelah NIK dan strip ekstensi
            nama_pasien = os.path.splitext(file[len(f"{nik} -"):])[0].strip()
            break

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        matched_files = [
            f for f in os.listdir(folder_path)
            if f.lower().startswith(f"{nik} -") and f.lower().endswith((".pdf", ".jpg", ".jpeg", ".png"))
        ]

        if matched_files:
            file_path = os.path.join(folder_path, matched_files[0])
            try:
                if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
                    # konversi gambar ke PDF sementara
                    temp_pdf = os.path.join(folder_path, f"_{nik}_temp.pdf")
                    img = Image.open(file_path).convert("RGB")
                    img.save(temp_pdf)
                    with fitz.open(temp_pdf) as src:
                        merged_pdf.insert_pdf(src)
                    os.remove(temp_pdf)
                else:
                    with fitz.open(file_path) as src:
                        merged_pdf.insert_pdf(src)
            except Exception as e:
                missing_files.append(f"{folder} (error: {e})")
        else:
            missing_files.append(folder)

    # === Simpan hasil dengan format [NIK] - [NAMA] - merged.pdf ===
    if not nama_pasien:
        nama_pasien = "TANPA NAMA"  # fallback jika tidak ada file di folder ro

    output_name = f"{nik} - {nama_pasien}.pdf"
    output_path = os.path.join(output_folder, output_name)

    if len(missing_files) < len(folders):
        try:
            merged_pdf.save(output_path)
            success = True
            status = "BERHASIL"
        except Exception as e:
            status = f"GAGAL (saat simpan: {e})"
    else:
        status = "GAGAL (semua file hilang)"

    merged_pdf.close()

    # Catat log
    log_data.append({
        "NIK": nik,
        "Nama Pasien": nama_pasien,
        "Status": status,
        "File Hilang / Catatan": ", ".join(missing_files) if missing_files else "-"
    })

    print(f"{status:25} | {nik} - {nama_pasien}")

# === SIMPAN LOG KE CSV ===
with open(log_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["NIK", "Nama Pasien", "Status", "File Hilang / Catatan"])
    writer.writeheader()
    writer.writerows(log_data)

print("\n=== SELESAI ===")
print(f"Hasil PDF disimpan di: {output_folder}")
print(f"Log proses disimpan di: {log_file}")
