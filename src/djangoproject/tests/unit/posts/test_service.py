import uuid
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from posts import service
from posts.models import Events, Posts
from users.models import User

#Testes unitários para os metódos de Posts e criação de eventos.

GIF_BYTES_TEST = (
    b"\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x02\x00"
    b"\x01\x00\x00\x02\x02D\x01\x00;"
)


def make_image(name: str = "test.gif"):
    return SimpleUploadedFile(name, GIF_BYTES_TEST, content_type="image/gif")


class PostsServiceTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass123")
        self.reader = User.objects.create_user(username="reader", password="pass123")
        self.post = Posts.objects.create(
            image=make_image("initial.gif"),
            text="Initial text",
            postedBy=self.owner,
        )

    def test_toggle_post_like_adds_like_for_new_reaction(self):
        # Arrange
        post_id = str(self.post.id)

        # Act
        message = service.toggle_post_like(self.reader, post_id)

        # Assert
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 1)
        self.assertTrue(self.post.likedBy.filter(id=self.reader.id).exists())
        self.assertIn("liked", message)

    def test_toggle_post_like_removes_like_when_already_liked(self):
        # Arrange
        post_id = str(self.post.id)
        self.post.likedBy.add(self.reader)
        self.post.likes = 1
        self.post.save(update_fields=["likes"])

        # Act
        message = service.toggle_post_like(self.reader, post_id)

        # Assert
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 0)
        self.assertFalse(self.post.likedBy.filter(id=self.reader.id).exists())
        self.assertIn("unliked", message)

    def test_toggle_post_like_raises_for_missing_post(self):
        # Arrange
        missing_id = str(uuid.uuid4())

        # Act / Assert
        with self.assertRaises(ValidationError):
            service.toggle_post_like(self.reader, missing_id)

    def test_get_all_posts_returns_posts_in_descending_order(self):
        # Arrange
        older_post = Posts.objects.create(
            image=make_image("older.gif"),
            text="Older post",
            postedBy=self.reader,
        )
        older_post.postedAt = timezone.now() - timedelta(days=1)
        older_post.save(update_fields=["postedAt"])
        self.post.postedAt = timezone.now()
        self.post.save(update_fields=["postedAt"])

        # Act
        posts = list(service.get_all_posts())

        # Assert
        self.assertGreaterEqual(len(posts), 2)
        self.assertEqual(posts[0], self.post)
        self.assertEqual(posts[1], older_post)

    def test_get_post_by_id_returns_instance(self):
        # Arrange
        post_id = str(self.post.id)

        # Act
        found_post = service.get_post_by_id(post_id)

        # Assert
        self.assertEqual(found_post, self.post)

    def test_get_post_by_id_raises_for_missing_post(self):
        # Arrange
        missing_id = str(uuid.uuid4())

        # Act / Assert
        with self.assertRaises(ValidationError):
            service.get_post_by_id(missing_id)

    def test_get_posts_by_user_returns_only_target_user(self):
        # Arrange
        another_post = Posts.objects.create(
            image=make_image("second.gif"),
            text="Second post",
            postedBy=self.owner,
        )
        Posts.objects.create(
            image=make_image("other.gif"),
            text="Other user post",
            postedBy=self.reader,
        )

        # Act
        posts = list(service.get_posts_by_user(self.owner))

        # Assert
        self.assertEqual(posts, [another_post, self.post])

    def test_create_post_persists_text_and_author(self):
        # Arrange
        image = make_image("new.gif")
        text = "New service post"

        # Act
        created_post = service.create_post(self.owner, image, text)

        # Assert
        self.assertIsInstance(created_post, Posts)
        self.assertEqual(created_post.postedBy, self.owner)
        self.assertEqual(created_post.text, text)
        self.assertTrue(Posts.objects.filter(id=created_post.id).exists())


class EventServiceTests(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            username="organizer", password="pass123"
        )
        self.attendee = User.objects.create_user(username="attendee", password="pass123")
        self.event = Events.objects.create(
            title="IMD 60+",
            event_date=timezone.now() + timedelta(days=5),
            locate="https://example.com/location",
            postedBy=self.organizer,
        )

    def test_toggle_event_rsvp_join_adds_participant(self):
        # Arrange
        event_id = str(self.event.id)

        # Act
        message = service.toggle_event_rsvp(self.attendee, event_id, "join")

        # Assert
        self.event.refresh_from_db()
        self.assertIn(self.attendee, self.event.participants.all())
        self.assertEqual(self.event.participants_count, 1)
        self.assertIn("joined", message)

    def test_toggle_event_rsvp_join_twice_is_invalid(self):
        # Arrange
        event_id = str(self.event.id)
        service.toggle_event_rsvp(self.attendee, event_id, "join")

        # Act / Assert
        with self.assertRaises(ValidationError):
            service.toggle_event_rsvp(self.attendee, event_id, "join")

    def test_toggle_event_rsvp_leave_after_join(self):
        # Arrange
        event_id = str(self.event.id)
        service.toggle_event_rsvp(self.attendee, event_id, "join")

        # Act
        message = service.toggle_event_rsvp(self.attendee, event_id, "leave")

        # Assert
        self.event.refresh_from_db()
        self.assertNotIn(self.attendee, self.event.participants.all())
        self.assertEqual(self.event.participants_count, 0)
        self.assertIn("left", message)

    def test_toggle_event_rsvp_leave_respects_non_negative_counter(self):
        # Arrange
        event_id = str(self.event.id)
        service.toggle_event_rsvp(self.attendee, event_id, "join")
        self.event.refresh_from_db()
        self.event.participants_count = 0
        self.event.save(update_fields=["participants_count"])

        # Act
        service.toggle_event_rsvp(self.attendee, event_id, "leave")

        # Assert
        self.event.refresh_from_db()
        self.assertEqual(self.event.participants_count, 0)

    def test_toggle_event_rsvp_leave_without_join_is_invalid(self):
        # Arrange
        event_id = str(self.event.id)

        # Act / Assert
        with self.assertRaises(ValidationError):
            service.toggle_event_rsvp(self.attendee, event_id, "leave")

    def test_toggle_event_rsvp_with_invalid_action_raises(self):
        # Arrange
        event_id = str(self.event.id)

        # Act / Assert
        with self.assertRaises(ValidationError):
            service.toggle_event_rsvp(self.attendee, event_id, "maybe")

    def test_toggle_event_rsvp_missing_event_raises(self):
        # Arrange
        missing_id = str(uuid.uuid4())

        # Act / Assert
        with self.assertRaises(ValidationError):
            service.toggle_event_rsvp(self.attendee, missing_id, "join")

