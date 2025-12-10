from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from posts.models import Posts, Events

class FeedManagerTests(TestCase):
    def setUp(self):
        # Usuários
        self.me = User.objects.create_user(username="me", password="123")
        self.friend = User.objects.create_user(username="friend", password="123")
        self.stranger = User.objects.create_user(username="stranger", password="123")
        
        self.me.following.add(self.friend)
        
        # Posts
        self.post_friend = Posts.objects.create(
            text="Friend Post", postedBy=self.friend
        )
        self.post_stranger = Posts.objects.create(
            text="Stranger Post", postedBy=self.stranger
        )
        
        # Eventos (Datas futuras)
        future_date = timezone.now() + timedelta(days=1)
        self.event_friend = Events.objects.create(
            title="Friend Event", event_date=future_date, 
            locate="Web", postedBy=self.friend
        )
        self.event_stranger = Events.objects.create(
            title="Stranger Event", event_date=future_date, 
            locate="Web", postedBy=self.stranger
        )

    def test_posts_feed_contains_only_followed_users(self):
        # Act
        feed = Posts.objects.get_feed_for_user(self.me)
        
        # Assert
        self.assertIn(self.post_friend, feed)
        self.assertNotIn(self.post_stranger, feed)

    def test_events_feed_scope_following_returns_only_followed(self):
        # Act
        feed = Events.objects.get_feed_for_user(self.me, scope="following")
        
        # Assert
        self.assertIn(self.event_friend, feed)
        self.assertNotIn(self.event_stranger, feed)

    def test_events_feed_scope_all_returns_everyone(self):
        # Act
        feed = Events.objects.get_feed_for_user(self.me, scope="all")
        
        # Assert
        self.assertIn(self.event_friend, feed)
        self.assertIn(self.event_stranger, feed)

    def test_events_feed_filters_past_events(self):
        # Arrange - Criar evento no passado
        past_date = timezone.now() - timedelta(days=1)
        past_event = Events.objects.create(
            title="Old Event", event_date=past_date, 
            locate="Web", postedBy=self.friend
        )
        
        # Act
        feed = Events.objects.get_feed_for_user(self.me, scope="all")
        
        # Assert
        self.assertNotIn(past_event, feed)