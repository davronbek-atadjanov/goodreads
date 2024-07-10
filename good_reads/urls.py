from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from good_reads import settings
from good_reads.view import landing_page, HomePageView
urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("home/", HomePageView.as_view(), name="home_page"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),
    path("api/v1/", include("api.urls")),


    path('api-auth/', include('rest_framework.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


