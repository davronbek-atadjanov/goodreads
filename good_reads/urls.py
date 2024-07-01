from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from good_reads import settings
from good_reads.view import landing_page

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("books/", include("books.urls"))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


