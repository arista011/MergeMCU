import os
import re

source_folders = ["e-audio","e-spiro","f-spiro","e-ekg","f-ekg","e-ro","f-ro","e-tread","f-tread"]

for folder in source_folders:
    if not os.path.exists(folder):
        print(f"⚠️ Folder tidak ditemukan: {folder}")
        continue

    print(f"\n📂 Memproses folder: {folder}")

    for filename in os.listdir(folder):

        # Hanya proses PDF dan JPG
        if not filename.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            continue

        name, ext = os.path.splitext(filename)

        # ✔ Jika SUDAH rapi: "1234 - NAMA"
        if " - " in name:
            print(f"✔ Sudah rapi, skip: {filename}")
            continue

        old_path = os.path.join(folder, filename)

        # ✔ CASE 1: Format "1234-NAMA" → rapikan
        dash_match = re.match(r"^(\d+)-(.+)$", name)
        if dash_match:
            nik = dash_match.group(1)
            nama = dash_match.group(2).strip(" -")
            new_name = f"{nik} - {nama}{ext}"
            new_path = os.path.join(folder, new_name)

            if os.path.exists(new_path):
                print(f"⚠️ File tujuan sudah ada, skip: {new_name}")
                continue

            os.rename(old_path, new_path)
            print(f"✓ {filename} → {new_name}")
            continue

        # ✔ CASE 2: Format "1234 NAMA"
        space_match = re.match(r"^(\d+)\s*(.*)$", name)
        if space_match:
            nik = space_match.group(1)
            nama = space_match.group(2).strip()

            if nama == "":
                print(f"⚠️ Nama kosong: {filename}")
                continue

            new_name = f"{nik} - {nama}{ext}"
            new_path = os.path.join(folder, new_name)

            if os.path.exists(new_path):
                print(f"⚠️ File tujuan sudah ada, skip: {new_name}")
                continue

            os.rename(old_path, new_path)
            print(f"✓ {filename} → {new_name}")
            continue

        print(f"⚠️ Tidak bisa diproses: {filename}")

print("\n🎉 Semua selesai!")
