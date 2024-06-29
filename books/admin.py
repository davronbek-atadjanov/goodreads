from django.contrib import admin
from .models import Book, BookAuthor, Author, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_display = ('title', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email')
    search_fields = ('first_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'book')


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'stars_given', )
    search_fields = ('comment', 'stars_given')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
