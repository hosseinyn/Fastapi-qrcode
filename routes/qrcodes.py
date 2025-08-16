from fastapi import APIRouter
from fastapi.responses import Response
import io
import qrcode

router = APIRouter()

@router.get("/api/generate-qrcode" , response_class=Response , tags=["Generate qrcode"])
def generate_qrcode(content: str):
    qr = qrcode.make(content)
    pil_image = qr.get_image()

    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    binary_data = buffer.getvalue()

    return Response(content=binary_data , media_type="image/png")
