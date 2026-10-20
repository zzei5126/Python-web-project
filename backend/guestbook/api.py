from django.http import FileResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .charts import build_chart
from .models import Entry
from .serializers import EntrySerializer, StatsSerializer
from .services import create_entry, delete_entry, statistics


class EntryListCreateApi(APIView):
    @extend_schema(tags=["Lời nhắn"], responses={200: EntrySerializer(many=True)})
    def get(self, request):
        entries = Entry.objects.all()
        return Response(EntrySerializer(entries, many=True).data)

    @extend_schema(tags=["Lời nhắn"], request=EntrySerializer, responses={201: EntrySerializer})
    def post(self, request):
        serializer = EntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        entry = create_entry(serializer.validated_data)
        return Response(EntrySerializer(entry).data, status=status.HTTP_201_CREATED)


class EntryDeleteApi(APIView):
    @extend_schema(tags=["Lời nhắn"], responses={204: OpenApiResponse(description="Đã xóa")})
    def delete(self, request, id):
        delete_entry(id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatsApi(APIView):
    @extend_schema(tags=["Thống kê"], responses={200: StatsSerializer})
    def get(self, request):
        return Response(statistics())


class ChartApi(APIView):
    @extend_schema(tags=["Thống kê"], responses={(200, "image/png"): OpenApiResponse(description="Ảnh biểu đồ cột PNG")})
    def get(self, request):
        path = build_chart(statistics()["senders"])
        return FileResponse(path.open("rb"), content_type="image/png")
