import fitz  # PyMuPDF
import os

# === KONFIGURASI ===
pdf_folder = "a-pdf"
foto_folder = "a-foto"
output_folder = "hasil"

# Ukuran foto (3x4 cm) dalam satuan point (1 cm = 28.35 pt)
foto_width = 3 * 28.35
foto_height = 4 * 28.35

# Margin dari tepi kertas (pojok kanan atas)
margin_right = 72  # pt
margin_top = 170    # pt

# Pastikan folder hasil ada
os.makedirs(output_folder, exist_ok=True)

# === LOOP SETIAP FILE PDF ===
for pdf_file in os.listdir(pdf_folder):
    if not pdf_file.lower().endswith(".pdf"):
        continue

    base_name = os.path.splitext(pdf_file)[0]
    pdf_path = os.path.join(pdf_folder, pdf_file)

    # Coba cari file foto dengan ekstensi .jpg atau .jpeg
    foto_path_jpg = os.path.join(foto_folder, base_name + ".jpg")
    foto_path_jpeg = os.path.join(foto_folder, base_name + ".jpeg")

    if os.path.exists(foto_path_jpg):
        foto_path = foto_path_jpg
    elif os.path.exists(foto_path_jpeg):
        foto_path = foto_path_jpeg
    else:
        print(f"⚠️ Foto tidak ditemukan untuk {pdf_file}")
        continue

    # === PROSES MERGE ===
    doc = fitz.open(pdf_path)
    if len(doc) < 2:
        print(f"⚠️ {pdf_file} hanya memiliki 1 halaman, dilewati.")
        doc.close()
        continue

    page = doc[1]  # halaman ke-2 (index dimulai dari 0)
    rect = page.rect

    # Hitung posisi pojok kanan atas
    x1 = rect.width - foto_width - margin_right
    y1 = margin_top
    x2 = x1 + foto_width
    y2 = y1 + foto_height
    posisi = fitz.Rect(x1, y1, x2, y2)

    # Tempelkan foto
    page.insert_image(posisi, filename=foto_path)

    # Simpan hasil
    output_path = os.path.join(output_folder, base_name + ".pdf")
    doc.save(output_path)
    doc.close()

    print(f"✅ {pdf_file} → foto berhasil ditempel di halaman ke-2 → {output_path}")

print("\n🎉 Semua file selesai diproses!")
