from fastapi import APIRouter , UploadFile , File
from fastapi.responses import Response
import io
import qrcode
import numpy as np
import cv2
from qreader import QReader

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

@router.post("/api/read-qrcode" , tags=["Read qrcode image"])
async def read_qrcode(file: UploadFile = File(...)):
    img_bytes = await file.read()

    np_arr = np.frombuffer(img_bytes, np.uint8)
    img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    qreader = QReader()

    try :
        decoded_text = qreader.detect_and_decode(image=image)

        decoded_text = decoded_text[0].strip('"')

        return {"decoded" : decoded_text}
    
    except : 
        return {"error" : "Error while decoding the qrcode"}

