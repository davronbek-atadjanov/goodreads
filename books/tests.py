from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author, BookAuthor, BookReview
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(
            reverse("books:list")
        )
        self.assertContains(response, "No books found.")

    def test_book_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="134324242")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="134324242")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="252452452")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        books = Book.objects.all()

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book3", description="Description3", isbn="252452452")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_query(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="134324242")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="134324242")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="252452452")

        response = self.client.get(reverse("books:list") + "?q=Book1")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Book2")
        self.assertNotContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse("books:list") + "?q=Book3")
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertContains(response, book3.title)

class BookReviewTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Book1", description="Description1", isbn="134324242")
        self.user = CustomUser.objects.create(username="Davronbek")
        self.user.set_password("Hsanov123")
        self.user.save()
        self.client.login(username="Davronbek", password="Hsanov123")

    def test_add_review(self):
        self.client.post(reverse("books:reviews", kwargs={"id": self.book.id}), data={
            "stars_given": 3,
            "comment": "Nice book"
        })

        book_review = self.book.bookreview_set.all()
        self.assertEqual(book_review.count(), 1)
        self.assertEqual(book_review[0].comment, "Nice book")
        self.assertEqual(book_review[0].book, self.book)
        self.assertEqual(book_review[0].user, self.user)

    def test_add_invalid_review(self):
        response = self.client.post(reverse("books:reviews", kwargs={"id": self.book.id}), data={
            "stars_given": 7,
            "comment": "Nice book"
        })
        book_review = self.book.bookreview_set.all()
        self.assertEqual(book_review.count(), 0)
        self.assertEqual(response.status_code, 200)

class BookEditReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Book1", description="Description1", isbn="234234234")
        self.user = CustomUser.objects.create(username="Davronbek")
        self.user.set_password("Hasanov123")
        self.user.save()
        self.client.login(username="Davronbek", password="Hasanov123")
        self.client.post(reverse("books:reviews", kwargs={"id": self.book.id}), data={
            "stars_given": 3,
            "comment": "Nice book"

        })
        self.review = BookReview.objects.get(book=self.book, user=self.user)
    def test_edit_review(self):
        response = self.client.post(reverse("books:edit-review", kwargs={"book_id": self.book.id, "review_id": self.review.id}),
                                    data = {
                                        "stars_given": 5,
                                        "comment": "Good project"
                                    })
        self.review.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.review.stars_given, 5)
        self.assertEqual(self.review.comment, "Good project")


class BookDeleteReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        self.user = CustomUser.objects.create(username="Davronbek")
        self.user.set_password("Hasanov1")
        self.user.save()
        self.client.login(username="Davronbek", password="Hasanov1")
        self.client.post(reverse("books:reviews", kwargs={"id": self.book.id}), data={
            "stars_given": 5,
            "comment": "Good luck!"
        })

        self.review = BookReview.objects.get(book=self.book, user=self.user)

    def test_confirm_delete_review_template(self):
        response = self.client.get(reverse("books:confirm-delete-review", kwargs={"book_id": self.book.id, "review_id": self.review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/confirm_delete_review.html")
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.review.comment)

    def test_delete_review(self):
        response = self.client.get(reverse("books:delete-review", kwargs={"book_id": self.book.id, "review_id": self.review.id}))
        book_review = self.book.bookreview_set.all()
        self.assertEqual(book_review.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully deleted this review")

    def test_delete_review_redirect(self):
        response = self.client.get(reverse("books:delete-review", kwargs={"book_id": self.book.id, "review_id": self.review.id}))
        self.assertRedirects(response, reverse("books:detail", kwargs={"id": self.book.id}))





class BookAuthorTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Book1", description="Description1", isbn="134324242")
        self.user = CustomUser.objects.create_user(username="Davronbek", password="Hsanov123")
        self.author = Author.objects.create(first_name="Toni", last_name="Joni", email="jonitoni@gmail.com",
                                            bio="Nice bio")
        self.book_author = BookAuthor.objects.create(book=self.book, author=self.author)

    def test_author_is_valid(self):
        self.client.login(username="Davronbek", password="Hsanov123")
        response = self.client.get(reverse("books:detail", kwargs={"id": self.book.id}))
        self.assertContains(response, self.author.first_name)
        self.assertContains(response, self.author.last_name)

        self.assertEqual(self.author.first_name, "Toni")
        self.assertEqual(self.author.last_name, "Joni")
        self.assertEqual(self.author.email, "jonitoni@gmail.com")
        self.assertEqual(self.author.bio, "Nice bio")

    def test_book_author_relation(self):
        self.assertEqual(self.book_author.book, self.book)
        self.assertEqual(self.book_author.author, self.author)


    def test_author_display_is_template(self):
        self.client.login(username="Davronbek", password="Hsanov123")
        response = self.client.get(reverse("books:detail", kwargs={"id": self.book.id}))
        self.assertContains(response, f"{self.author.first_name} {self.author.last_name}")
