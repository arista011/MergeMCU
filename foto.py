import fitz  # PyMuPDF
import os

# === KONFIGURASI ===
pdf_folder = "a-pdf"
foto_folder = "a-foto"
output_folder = "hasil"

# Ukuran foto 3x4 cm dalam satuan point (1 cm = 28.35 pt)
foto_width = 3 * 28.35
foto_height = 4 * 28.35

# Margin dari tepi kertas
margin_right = 30  # pt
margin_top = 30   # pt

os.makedirs(output_folder, exist_ok=True)

# === PROSES GABUNG ===
for pdf_file in os.listdir(pdf_folder):
    if not pdf_file.lower().endswith(".pdf"):
        continue

    base_name = os.path.splitext(pdf_file)[0]  # contoh: "1234 - aris"
    foto_name_jpg = os.path.join(foto_folder, base_name + ".jpg")
    foto_name_jpeg = os.path.join(foto_folder, base_name + ".jpeg")

    # Cek ekstensi foto yang tersedia
    foto_path = None
    if os.path.exists(foto_name_jpg):
        foto_path = foto_name_jpg
    elif os.path.exists(foto_name_jpeg):
        foto_path = foto_name_jpeg

    if not foto_path:
        print(f"⚠️ Foto tidak ditemukan untuk: {pdf_file}")
        continue

    pdf_path = os.path.join(pdf_folder, pdf_file)
    doc = fitz.open(pdf_path)

    # Ambil halaman pertama saja
    page = doc[0]
    rect = page.rect

    # Tentukan posisi pojok kanan atas
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

    print(f"✅ Selesai: {output_path}")

print("\n🎉 Semua PDF berhasil digabung di folder 'hasil/'")
