from django.shortcuts import render, get_object_or_404, redirect
from .models import forums, forum_post


# remove once base user returning correctly
def get_forum_user(request):
    if not request.user.is_authenticated:
        return None

    try:
        # If base_user exists for this Django user
        return request.user.base_user
    except:
        return None


def forum_list(request):
    all_forums = forums.objects.all()
    return render(request, "forums/forum_list.html", {"forums": all_forums})


def forum_detail(request, forum_id):
    forum = get_object_or_404(forums, pk=forum_id)
    # shows posts whether base_user exists or not. base user for some reason not working for me.
    posts = forum_post.objects.all().filter(
        author__isnull=True
    ) | forum_post.objects.all().filter(author__isnull=False)
    return render(request, "forums/forum_detail.html", {"forum": forum, "posts": posts})


def create_post(request, forum_id):
    forum = get_object_or_404(forums, pk=forum_id)

    if request.method == "POST":
        text = request.POST.get("text")
        author = get_forum_user(request)  # change once base user working correctly

        forum_post.objects.create(author=author, post_text=text)

        return redirect("forum_detail", forum_id=forum_id)

    return render(request, "forums/create_post.html", {"forum": forum})


def create_forum(request):
    if request.method == "POST":
        # get fields from post
        name = request.POST.get("forum_name")
        description = request.POST.get("forum_description")
        tags = request.POST.get("forum_tags")
        start_date = request.POST.get("start_date")
        meeting_day = request.POST.get("meeting_day")
        meeting_time = request.POST.get("meeting_time")

        owner = get_forum_user(
            request
        )  # change once base user working correctly/i figure out what im doin wrong

        # Convert comma-separated tags into a list
        try:
            tag_list = [t.strip() for t in tags.split(",")] if tags else []
        except:
            tag_list = []

        # Save the new forum
        forums.objects.create(
            forum_name=name,
            forum_description=description,
            forum_tags=tag_list,
            owner=owner,  # owner can be none for now!!! dont forget to change
            start_date=start_date or None,
            meeting_day=meeting_day or None,
            meeting_time=meeting_time or None,
        )

        return redirect("forum_list")  # back to list page

    # GET request: show the empty form
    return render(request, "forums/create_forum.html")
