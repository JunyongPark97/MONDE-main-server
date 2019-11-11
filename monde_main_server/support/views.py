from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from support.models import Official, MondeSupport
from support.serializers import OfficialSerializer, ContactSerializer


class OfficialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

    @action(detail=False, methods=['GET'], url_path='use-terms')
    def use_terms(self, request):
        obj = self.get_queryset().filter(official_type=0).order_by('version').last()
        serializer = self.get_serializer(obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='privacy-policy')
    def privacy_policy(self, request):
        obj = self.get_queryset().filter(official_type=1).order_by('version').last()
        serializer = self.get_serializer(obj)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = MondeSupport.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        if 'file' in data:
            image = data.pop('file')[0]
            data.update({'attached_file': image})

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
