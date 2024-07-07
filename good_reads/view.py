from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from books.models import BookReview


def landing_page(request):
    return render(request, "landing.html")

class HomePageView(View):

    def get(self, request):
        book_reviews = BookReview.objects.all().order_by("-created_at")

        page_size = request.GET.get('page_size', 5)
        paginator = Paginator(book_reviews, page_size)
        page_num = request.GET.get('page', 1)
        page_object = paginator.get_page(page_num)

        context = {
            "page_obj": page_object
        }
        return render(request, "home.html", context)


