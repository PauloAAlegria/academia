from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageOps

def process_image_field(image_field, max_size=(3000, 3000), quality=90):
    """
    Processa uma imagem de forma segura:
    - Corrige orientação EXIF
    - Redimensiona até max_size
    - Converte para RGB se necessário
    - Salva em WebP mantendo qualidade
    """
    if not image_field:
        return

    try:
        img = Image.open(image_field)
    except Exception:
        return  # não quebra se não for possível abrir a imagem

    # Corrige orientação EXIF
    img = ImageOps.exif_transpose(img)

    # Redimensiona mantendo proporção
    max_width, max_height = max_size
    w, h = img.size
    if w > max_width or h > max_height:
        ratio = min(max_width / w, max_height / h)
        new_size = (int(w * ratio), int(h * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Converter para RGB se necessário
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Salvar em WebP
    buffer_webp = BytesIO()
    img.save(
        buffer_webp,
        format="WEBP",
        quality=quality,
        method=6  # melhor compressão WebP
    )

    # Gerar nome WebP a partir do original
    base_name = image_field.name.rsplit('.', 1)[0]
    webp_name = f"{base_name}.webp"

    # Substituir arquivo original pelo WebP
    image_field.save(
        webp_name,
        ContentFile(buffer_webp.getvalue()),
        save=False
    )
