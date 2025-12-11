import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw

# ============================================================
#                       KONFIGURASI
# ============================================================
folder_list = ["f-ekg", "f-spiro", "f-tread"]

logo_mitra_path     = "LOGO/Mitra.png"
logo_lovelife_path  = "LOGO/Lovelife.png"
logo_senyum_path    = "LOGO/Senyum.png"

# A4 LANDSCAPE (842 × 595)
A4_W = 842
A4_H = 595

# HEADER & FOOTER
HEADER_HEIGHT = int(A4_H * 0.10)
FOOTER_HEIGHT = int(A4_H * 0.08)

# ============================================================
#                       LOAD LOGO
# ============================================================
logo_mitra    = Image.open(logo_mitra_path).convert("RGBA")
logo_lovelife = Image.open(logo_lovelife_path).convert("RGBA")
logo_senyum   = Image.open(logo_senyum_path).convert("RGBA")

asp_mitra    = logo_mitra.width / logo_mitra.height
asp_lovelife = logo_lovelife.width / logo_lovelife.height
asp_senyum   = logo_senyum.width / logo_senyum.height

# ============================================================
#      TEMPLATE A4 (SAMA PERSIS DENGAN VERSION JPG)
# ============================================================
def make_a4(body_img):

    canvas = Image.new("RGBA", (A4_W, A4_H), "white")

    # ================ BODY ================
    max_w = A4_W
    max_h = A4_H - HEADER_HEIGHT - FOOTER_HEIGHT

    scale = min(max_w / body_img.width, max_h / body_img.height)
    new_w = int(body_img.width * scale) + 120
    new_h = int(body_img.height * scale)

    body_resized = body_img.resize((new_w, new_h), Image.LANCZOS)
    body_x = (A4_W - new_w) // 2
    body_y = HEADER_HEIGHT - 20
    canvas.paste(body_resized, (body_x, body_y))

    # ================ HEADER LOGO ================
    LOGO_H = int(HEADER_HEIGHT * 0.70)

    # Mitra
    mitra_w = int(LOGO_H * asp_mitra)
    mitra = logo_mitra.resize((mitra_w, LOGO_H), Image.LANCZOS)
    mitra_y = (HEADER_HEIGHT - LOGO_H)//2
    canvas.paste(mitra, (40, mitra_y), mitra)

    # Lovelife
    love_h = int(LOGO_H * 0.75)
    love_w = int(love_h * asp_lovelife)
    love = logo_lovelife.resize((love_w, love_h), Image.LANCZOS)
    love_y = (HEADER_HEIGHT - love_h)//2
    canvas.paste(love, (A4_W - love_w - 40, love_y), love)

    # ================ FOOTER LOGO ================
    senyum_h = int(FOOTER_HEIGHT * 0.95)
    senyum_w = int(senyum_h * asp_senyum)
    senyum = logo_senyum.resize((senyum_w, senyum_h), Image.LANCZOS)

    canvas.paste(senyum, (A4_W - senyum_w - 30, A4_H - senyum_h - 20), senyum)

    return canvas.convert("RGB")

# ============================================================
#                       PROSES PDF
# ============================================================
for folder_path in folder_list:
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(folder_path, filename)
        print("🔧 Memproses:", filename)

        pdf = fitz.open(file_path)
        new_pdf = fitz.open()

        for i, page in enumerate(pdf):

            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # MASUKKAN KE TEMPLATE
            out_img = make_a4(img)

            # Simpan sementara JPG untuk dimasukkan ke PDF
            temp_jpg = f"{file_path}_temp_{i}.jpg"
            out_img.save(temp_jpg, "JPEG", quality=95, dpi=(200,200))

            rect = fitz.Rect(0, 0, A4_W, A4_H)
            new_page = new_pdf.new_page(width=A4_W, height=A4_H)
            new_page.insert_image(rect, filename=temp_jpg)

            os.remove(temp_jpg)

        pdf.close()

        # overwrite aman
        temp_output = file_path + ".tmp.pdf"
        new_pdf.save(temp_output)
        new_pdf.close()
        os.replace(temp_output, file_path)

print("\n✅ PDF berhasil dirapikan dan LOGO tampil seperti versi JPG!")
