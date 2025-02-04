import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def qr_code_generator(value, filename="qr_code.png"):
    """
    Génère un QR code pour une valeur donnée et retourne un fichier utilisable
    dans un champ FileField ou ImageField.
    
    Arguments:
    - value (str) : Les données à encoder dans le QR code.
    - filename (str) : Nom du fichier (par défaut "qr_code.png").

    Retourne:
    - ContentFile : Un fichier compatible avec Django.
    """
    # Générer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(value)
    qr.make(fit=True)

    # Convertir en image
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Créer un fichier utilisable par Django
    return ContentFile(buffer.read(), name=filename)
