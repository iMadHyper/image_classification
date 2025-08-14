from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from . import utils
from .serializers import PredictSerializer


class PredictAPI(APIView):
    serializer_class = PredictSerializer
    
    def post(self, request, format=None):
        '''
        Takes an image, returns JSON prediction
        '''
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            result = utils.predict_image(image_file)
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)