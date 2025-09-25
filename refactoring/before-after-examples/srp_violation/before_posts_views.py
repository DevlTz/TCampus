
class FeedView(ListAPIView):
    
   # Combined feed: posts + events. By default shows posts+events from followed users.
   #  If ?events_scope=all is present, events will include upcoming events from ALL users
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        #
        # POSTS: we want posts from followed users only
        posts_qs = Posts.objects.filter(postedBy__in=user.following.all()).order_by('-postedAt')
        posts_data = PostsSerializer(posts_qs, many=True, context={"request": request}).data

        # EVENTS: can be filtered by scope
        # ?events_scope=all  -> include events from any user
        # Anything else (default) -> include events from followed users only
        scope = request.query_params.get('events_scope', 'following')
        now = timezone.now()

        if scope == 'all':
            # Include only upcoming events from all users
            events_qs = Events.objects.filter(event_date__gte=now).order_by('-event_date')
        else:
            # Default: include events from followed users only
            # Can include past events too (e.g., from yesterday)
            events_qs = Events.objects.filter(postedBy__in=user.following.all()).order_by('-event_date')

        events_data = EventsSerializer(events_qs, many=True, context={"request": request}).data

        # Now we have two lists of dicts: posts_data and events_data
        # We need to merge them into a single feed, sorted by date (most recent first)
        normalized = []
        # adding posts to normalized list
        for p in posts_data:
            normalized.append({
                "type": "post",
                "sort_date": p.get("postedAt") or p.get("created_at"),
                "data": p
            })
            # adding events to normalized list
        for e in events_data:
            normalized.append({
                "type": "event",
                "sort_date": e.get("event_date"),
                "data": e
            })

        normalized.sort(key=lambda x: x["sort_date"] or "", reverse=True)
        # constructing final feed
        feed = []
        for item in normalized:
            obj = dict(item["data"])
            obj["type"] = item["type"]
            feed.append(obj)

        # return combined feed. 
        return Response(feed)