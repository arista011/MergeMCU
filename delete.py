import os
import glob

# Daftar folder target
folders = ["a-pdf","lab", "f-ro", "e-ro", "f-ekg", "e-ekg", "f-spiro", "e-spiro", "e-audio", "f-tread","e-tread","hasil"]

# Base path lokasi folder berada
base_dir = os.path.dirname(os.path.abspath(__file__))

for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    
    if os.path.exists(folder_path):
        # Ambil semua file dalam folder tersebut
        files = glob.glob(os.path.join(folder_path, "*"))
        
        for f in files:
            try:
                if os.path.isfile(f):
                    os.remove(f)
                    print(f"Dihapus: {f}")
            except Exception as e:
                print(f"Gagal hapus: {f}, Error: {e}")
    else:
        print(f"Folder tidak ditemukan: {folder_path}")
