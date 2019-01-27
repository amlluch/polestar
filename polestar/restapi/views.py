from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UploadSerializer, ShipsSerializer, PositionSerializer
from .utils import ImportPositions, ResponseException
from .models import Csv, Ships, Positions

import os

# Create your views here.

class UploadFile(APIView):

    serializer_class = UploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            dato = serializer.save()
            imfile = ImportPositions(serializer.data['csvfile'])
            try:
                serialized = imfile.update()
                Csv.objects.filter(csvfile__contains = os.path.basename(serializer.data['csvfile'])).delete()
                return Response(serialized, status=status.HTTP_200_OK)
            except ResponseException as error:
                Csv.objects.filter(csvfile__contains = os.path.basename(serializer.data['csvfile'])).delete()
                return Response(error.message, status=error.status)
        else:
            return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShipsView(APIView):

    serializer_class = ShipsSerializer
    def get(self, request):
        ships = Ships.objects.all()
        serializer = self.serializer_class(ships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            dato = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PositionsView(APIView):

    serializer_class = PositionSerializer
    def get(self, request, imo):

        positions = Positions.objects.filter(ship__imo__contains = imo).order_by('-timestamp')
        serializer = self.serializer_class(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def home(request):
    return render(request, 'restapi/index.html')
