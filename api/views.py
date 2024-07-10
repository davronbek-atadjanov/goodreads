from django.http import JsonResponse
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookReview
from .serializers import BookReviewSerializers

class BookReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)
        serializer = BookReviewSerializers(book_review)
        return Response(data=serializer.data)

class BookReviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        book_reviews = BookReview.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(book_reviews, request)

        serializer = BookReviewSerializers(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)


