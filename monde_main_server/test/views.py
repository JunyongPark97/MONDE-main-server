import os
import json
from django.shortcuts import render
from django.urls import path
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response


def home(request):
    return render(request, 'home.html')

class ListTestAPIView(GenericAPIView):

    def get(self, *args, **kwargs):
        jsondata = {}
        jsondata_path = os.path.join(os.path.dirname(__file__), 'data.json')
        if os.path.exists(jsondata_path):
            with open(jsondata_path) as f:
                print('====')
                jsondata = json.loads(f.read())
        return Response(jsondata,status=status.HTTP_200_OK)


class ZIGZAGListTestAPIView(GenericAPIView):

    def get(self, *args, **kwargs):
        zigzagdata = {}
        zigzagdata_path = os.path.join(os.path.dirname(__file__), 'zigzag_data.json')
        if os.path.exists(zigzagdata_path):
            with open(zigzagdata_path) as f:
                print('====')
                zigzagdata = json.loads(f.read())
        return Response(zigzagdata,status=status.HTTP_200_OK)