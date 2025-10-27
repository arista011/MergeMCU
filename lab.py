import os

# Folder target
folder_path = "lab/"

# Loop semua file dalam folder
for filename in os.listdir(folder_path):
    if not filename.lower().endswith(".pdf"):
        continue  # lewati non-PDF

    parts = filename[:-4].split("_")  # hapus ".pdf", lalu pecah pakai "_"

    # Pastikan ada minimal 3 bagian
    if len(parts) < 3:
        print(f"⚠️ Lewati (format tidak sesuai): {filename}")
        continue

    # Ambil bagian sesuai urutan contoh
    nama_raw = parts[1].strip()
    nik_raw = parts[2].strip()

    # Hapus nol di depan NIK
    nik_bersih = nik_raw.lstrip("0") or "0"

    # Format baru: NIK - Nama.pdf
    new_name = f"{nik_bersih} - {nama_raw}.pdf"

    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)

    # Rename file
    os.rename(old_path, new_path)
    print(f"✅ {filename} → {new_name}")

print("\n🎉 Selesai! Semua file sudah diubah namanya.")
