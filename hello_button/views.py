from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
def index(request):
    return Response({'message':'test'}, status=status.HTTP_404_NOT_FOUND)
