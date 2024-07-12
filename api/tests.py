from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Davronbek")
        self.user.set_password("Hasanov1")
        self.user.save()
        self.client.login(username="Davronbek", password="Hasanov1")


    def test_book_review_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse("api:review-detail", kwargs={"id": book_review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], book_review.id)
        self.assertEqual(response.data['stars_given'], book_review.stars_given)
        self.assertEqual(response.data['comment'], book_review.comment)
        self.assertEqual(response.data['book']['id'], book_review.book.id)
        self.assertEqual(response.data['book']['title'], book_review.book.title)
        self.assertEqual(response.data['book']['description'], book_review.book.description)
        self.assertEqual(response.data['book']['isbn'], book_review.book.isbn)
        self.assertEqual(response.data['user']['id'], book_review.user.id)
        self.assertEqual(response.data['user']['id'], book_review.user.id)
        self.assertEqual(response.data['user']['username'], book_review.user.username)

    def test_book_review_list(self):
        user2 = CustomUser.objects.create(username="Sombody")
        user2.set_password("Hasanov1")
        user2.save()

        book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        book_review1 = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")
        book_review2 = BookReview.objects.create(book=book, user=user2, stars_given=3, comment="Good luck!")

        response = self.client.get(reverse("api:review-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)


        # user uchun test
        self.assertEqual(response.data['results'][1]['id'], book_review1.id)
        self.assertEqual(response.data['results'][1]['stars_given'], book_review1.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], book_review1.comment)
        self.assertEqual(response.data['results'][1]['book']['id'], book_review1.book.id)
        self.assertEqual(response.data['results'][1]['book']['title'], book_review1.book.title)
        self.assertEqual(response.data['results'][1]['book']['description'], book_review1.book.description)
        self.assertEqual(response.data['results'][1]['book']['isbn'], book_review1.book.isbn)
        self.assertEqual(response.data['results'][1]['user']['id'], book_review1.user.id)
        self.assertEqual(response.data['results'][1]['user']['id'], book_review1.user.id)
        self.assertEqual(response.data['results'][1]['user']['username'], book_review1.user.username)

        # user2 uchun test

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], book_review2.id)
        self.assertEqual(response.data['results'][0]['stars_given'], book_review2.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], book_review2.comment)
        self.assertEqual(response.data['results'][0]['book']['id'], book_review2.book.id)
        self.assertEqual(response.data['results'][0]['book']['title'], book_review2.book.title)
        self.assertEqual(response.data['results'][0]['book']['description'], book_review2.book.description)
        self.assertEqual(response.data['results'][0]['book']['isbn'], book_review2.book.isbn)
        self.assertEqual(response.data['results'][0]['user']['id'], book_review2.user.id)
        self.assertEqual(response.data['results'][0]['user']['id'], book_review2.user.id)
        self.assertEqual(response.data['results'][0]['user']['username'], book_review2.user.username)

    def test_review_delete(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.delete(reverse("api:review-detail", kwargs={"id": book_review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.patch(reverse("api:review-detail", kwargs={"id": book_review.id}),
                                     data={
                                         "stars_given": 3
                                     })
        book_review.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 3)

    def test_put_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.put(reverse("api:review-detail", kwargs={"id": book_review.id}),
                                     data={
                                         "stars_given": 3,
                                         "comment": "Good lock",
                                         "user_id": self.user.id,
                                         "book_id": book.id
                                     })
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 3)
        self.assertEqual(book_review.comment, "Good lock")

    def test_create_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="23234242")
        data = {
            "stars_given": 4,
            "comment": "good book",
            "user_id": self.user.id,
            "book_id": book.id
        }

        response = self.client.post(reverse("api:review-list"), data=data)

        book_review = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(book_review.stars_given, 4)
        self.assertEqual(book_review.comment, "good book")

