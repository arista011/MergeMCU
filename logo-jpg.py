import os
from PIL import Image, ImageDraw

# === KONFIGURASI ===
folder_list = ["f-ro"]

# 3 LOGO TERPISAH
logo_mitra_path     = "LOGO/Mitra.png"
logo_lovelife_path  = "LOGO/Lovelife.png"
logo_senyum_path    = "LOGO/Senyum.png"

# A4 LANDSCAPE (842 × 595 px)
A4_W = 842
A4_H = 595

# HEADER & FOOTER
HEADER_HEIGHT = int(A4_H * 0.10)   # header 10%
FOOTER_HEIGHT = int(A4_H * 0.08)   # footer 8%

# ==== LOAD LOGO ====
logo_mitra    = Image.open(logo_mitra_path).convert("RGBA")
logo_lovelife = Image.open(logo_lovelife_path).convert("RGBA")
logo_senyum   = Image.open(logo_senyum_path).convert("RGBA")

asp_mitra    = logo_mitra.width / logo_mitra.height
asp_lovelife = logo_lovelife.width / logo_lovelife.height
asp_senyum   = logo_senyum.width / logo_senyum.height


# ================================================================
#         FUNGSI: GENERATE A4 LANDSCAPE – LOGO DI DEPAN
# ================================================================
def make_a4_image(body_img):

    canvas = Image.new("RGBA", (A4_W, A4_H), "white")

    # =========================================================
    #                     FOTO BODY (PUSAT)
    # =========================================================
    max_w = A4_W - 20
    max_h = A4_H - HEADER_HEIGHT - FOOTER_HEIGHT - 20

    scale = min(max_w / body_img.width, max_h / body_img.height)
    new_w = int(body_img.width * scale)
    new_h = int(body_img.height * scale)

    body_resized = body_img.resize((new_w, new_h), Image.LANCZOS)

    body_x = (A4_W - new_w) // 2
    body_y = HEADER_HEIGHT + 10   # dekat header

    canvas.paste(body_resized, (body_x, body_y))

    # =========================================================
    #                   LOGO HEADER (RESPONSIF)
    # =========================================================

    # Tinggi logo header ideal = 70% dari HEADER_HEIGHT
    LOGO_H = int(HEADER_HEIGHT * 0.70)

    # --- Logo Mitra (kiri atas)
    mitra_w = int(LOGO_H * asp_mitra)
    mitra_res = logo_mitra.resize((mitra_w, LOGO_H), Image.LANCZOS)

    mitra_x = 40
    mitra_y = (HEADER_HEIGHT - LOGO_H) // 2
    canvas.paste(mitra_res, (mitra_x, mitra_y), mitra_res)

    # --- Logo Lovelife (kanan atas) — sedikit lebih kecil
    love_h = int(LOGO_H * 0.75)
    love_w = int(love_h * asp_lovelife)
    love_res = logo_lovelife.resize((love_w, love_h), Image.LANCZOS)

    love_x = A4_W - love_w - 40
    love_y = (HEADER_HEIGHT - love_h) // 2
    canvas.paste(love_res, (love_x, love_y), love_res)

    # =========================================================
    #                   LOGO FOOTER (RESPONSIF)
    # =========================================================

    # Tinggi footer logo = 60% dari FOOTER_HEIGHT
    senyum_h = int(FOOTER_HEIGHT * 0.60)
    senyum_w = int(50 * asp_senyum)
    senyum_res = logo_senyum.resize((senyum_w, senyum_h), Image.LANCZOS)

    senyum_x = A4_W - senyum_w - 30
    senyum_y = A4_H - senyum_h - 20
    canvas.paste(senyum_res, (senyum_x, senyum_y), senyum_res)

    return canvas.convert("RGB")

# =======================================================================
#                           PROCESS FILES
# =======================================================================
for folder_path in folder_list:
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):

            file_path = os.path.join(folder_path, filename)
            print("🔧 Memproses:", file_path)

            body = Image.open(file_path).convert("RGB")
            result = make_a4_image(body)

            # Simpan JPG hasil
            result.save(file_path, "JPEG", quality=95, dpi=(100,100))

print("\n✅ Semua JPG berhasil dibuat ke format A4 Landscape — LOGO SUDAH PROPORSIONAL!")
