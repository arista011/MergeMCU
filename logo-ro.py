import os
from PIL import Image, ImageDraw

# === KONFIGURASI ===
folder_path = "f-ro/"
logo_path = os.path.join( "LOGO", "LOGO.png")

# === BUKA LOGO SEKALI SAJA ===
logo = Image.open(logo_path).convert("RGBA")

# === LOOP SEMUA FILE JPG DALAM f-ro/ ===
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".jpg"):
        file_path = os.path.join(folder_path, filename)
        print(f"🔧 Memproses: {filename}")

        # Buka foto rontgen
        body = Image.open(file_path).convert("RGBA")

        # === Hitung ukuran header responsif ===
        header_height = int(body.height * 0.14)  # tinggi header proporsional
        new_height = body.height + header_height
        new_width = body.width

        # === Buat kanvas putih baru ===
        new_img = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(new_img)

        # === Hitung ukuran logo responsif (maks 70% lebar header, tapi dengan margin) ===
        horizontal_margin = int(new_width * 0)
        logo_max_width = new_width - (2 * horizontal_margin)
        aspect_ratio = logo.height / logo.width
        logo_new_height = int(logo_max_width * aspect_ratio)

        # Jika logo terlalu tinggi untuk header, sesuaikan lagi
        if logo_new_height > header_height - 20:
            logo_new_height = header_height - 20
            logo_max_width = int(logo_new_height / aspect_ratio)

        # Resize logo proporsional
        logo_resized = logo.resize((logo_max_width, logo_new_height), Image.LANCZOS)

        # === Posisi logo di tengah atas ===
        logo_x = (new_width - logo_max_width) // 2
        logo_y = (header_height - logo_new_height) // 2

        # === Tempel logo ===
        new_img.paste(logo_resized, (logo_x, logo_y), logo_resized)

        # === Tambah garis pemisah tipis di bawah header (opsional tapi profesional) ===
        line_y = header_height - 1
        draw.line([(0, line_y), (new_width, line_y)], fill=(180, 180, 180, 255), width=2)

        # === Tempel foto X-ray di bawah header ===
        new_img.paste(body, (0, header_height))

        # === Simpan hasil ===
        new_img.convert("RGB").save(file_path, "JPEG")

print("✅ Semua gambar sudah diberi header logo yang responsif dan profesional.")
