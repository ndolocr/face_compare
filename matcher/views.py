import face_recognition

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["POST"])
def compare_faces(request):
    """
    Expects two images: 'id_image' and 'selfie_image' in multipart/form-data.
    Returns: { "match": True/False, "distance": float }
    """
    id_image_file = request.FILES.get("id_image")
    selfie_image_file = request.FILES.get("selfie_image")

    print(f"ID Image Captured --> {id_image_file}")
    print(f"Selfie Image Captured --> {selfie_image_file}")

    if not id_image_file or not selfie_image_file:
        return Response(
            {"error": "Please provide both 'id_image' and 'selfie_image'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Load images
        id_image = face_recognition.load_image_file(id_image_file)
        selfie_image = face_recognition.load_image_file(selfie_image_file)

        # Encode faces
        id_encodings = face_recognition.face_encodings(id_image)
        selfie_encodings = face_recognition.face_encodings(selfie_image)

        print(f"ID Image Encoding --> {id_encodings}")
        print(f"Selfie Image Encoding --> {selfie_encodings}")

        if not id_encodings or not selfie_encodings:
            return Response(
                {"error": "No face detected in one of the images."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        id_encoding = id_encodings[0]
        selfie_encoding = selfie_encodings[0]

        print(f"ID Image Encoding[0] --> {id_encodings}")
        print(f"Selfie Image Encoding[0] --> {selfie_encodings}")

        # Compare faces
        results = face_recognition.compare_faces([id_encoding], selfie_encoding, tolerance=0.6)
        distance = face_recognition.face_distance([id_encoding], selfie_encoding)[0]

        print(f"Results --> {results}")
        print(f"Distance --> {distance}")

        print(f"Match --> {results[0]}")
        print(f"Matched Distance --> {float(distance)}")

        return Response({"match": results[0], "distance": float(distance)})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)