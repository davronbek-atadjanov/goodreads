

from django.contrib import admin
from django.urls import path, include

from good_reads.view import landing_page

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="users"),

]


