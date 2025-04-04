from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import easyocr
from PIL import Image
import numpy as np
from io import BytesIO

def extract_numbers_from_image(image):
    # EasyOCR o'qish obyektini yaratish
    reader = easyocr.Reader(['en'])

    # Faylni numpy massiviga o'zgartirish
    img = Image.open(image)  # Image obyektiga o'zgartiramiz
    img_array = np.array(img)  # Rasmni numpy massiviga o'zgartiramiz

    # Rasmni o'qish
    result = reader.readtext(img_array)

    # Faqat raqamlarni ajratib olish
    numbers = ''.join([text[1] for text in result if text[1].isdigit()])

    return numbers

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        image = request.FILES.get('image')
        if image:
            # Rasmni o'qish va raqamlarni olish
            numbers = extract_numbers_from_image(image)
            return Response({"message": numbers}, status=status.HTTP_200_OK)
        return Response({"error": "Rasm topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
