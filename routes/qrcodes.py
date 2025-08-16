from fastapi import APIRouter
from fastapi.responses import Response
import io
import qrcode

router = APIRouter()

@router.get("/api/generate-qrcode" , response_class=Response , tags=["Generate qrcode"])
def generate_qrcode(content: str , dark: int = 0):
    if dark and dark == 1:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(content)
        qr.make()
        img = qr.make_image(fill_color="white", back_color="black")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        binary_data = buffer.getvalue()

    else : 
        qr = qrcode.make(content)
        pil_image = qr.get_image()

        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        binary_data = buffer.getvalue()

    return Response(content=binary_data , media_type="image/png")
