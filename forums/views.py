from django.shortcuts import render, get_object_or_404, redirect
from .models import forums, forum_post, forum_comment
from django.contrib.auth.decorators import login_required


def forum_list(request):
    all_forums = forums.objects.all()
    return render(request, "forums/forum_list.html", {"forums": all_forums})


def forum_detail(request, forum_id):
    forum = get_object_or_404(forums, pk=forum_id)
    posts = forum.posts.filter(approved=True)  # shows only this forums posts
    return render(request, "forums/forum_detail.html", {"forum": forum, "posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(forum_post, pk=post_id)
    comments = post.comments.all()

    return render(
        request, "forums/post_detail.html", {"post": post, "comments": comments}
    )

from django.core.validators import ValidationError
from django.http import HttpResponse

@login_required
def create_post(request, forum_id):
    forum = get_object_or_404(forums, pk=forum_id)
    

    if request.method == "POST":
        text = request.POST.get("text") #gets text from the html 
        author = request.user  # gets current user
        new_post = forum_post(forum=forum, author=author, post_text=text)

    #__________form validation__________#
        #we first try and clean/valid the post, if it fails, takes you back to making a new form ideal with all the old info already there
        try: 
            new_post.full_clean()
            new_post.save()
            print("we did not find a bad word and have sent the data to the database")
            return redirect("forum_detail", forum_id=forum_id)
        except ValidationError as ve:
            print("ERROR ERROR WE FOUND A BAD WORD")
                #!MAKE IT SO IT TRYS TO RESUBMIT THE FORM, USE THE FOLLOWING WEBSTIE:
                #https://forum.djangoproject.com/t/form-validationerror-not-showing-in-form/33363
            context = {'text': text}
            #return HttpResponse('')
            return render(request,
                        "forums/create_post.html",
                        context={"forum": forum,'text_entry': text} #{"forum": forum, "post_text":text}
                        )  # Pass the form with errors
                #TODO
                #TODO
                #TODO
                #TODO
        #new_post.save()
        #___________________________________#
        #print("we did not find a bad word and have sent the data to the database")
        #return redirect("forum_detail", forum_id=forum_id)
    elif request.method == "GET":
        #!add here contex for if we send a string maybe
        return render(request, "forums/create_post.html", {"forum": forum})


@login_required
def create_forum(request):
    if request.method == "POST":
        # get fields from post
        name = request.POST.get("forum_name")
        description = request.POST.get("forum_description")
        tags = request.POST.get("forum_tags")
        start_date = request.POST.get("start_date")
        meeting_day = request.POST.get("meeting_day")
        meeting_time = request.POST.get("meeting_time")

        forum_lead = request.user  # changed to forum lead for clarity

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
            forum_lead=forum_lead,
            start_date=start_date,
            meeting_day=meeting_day,
            meeting_time=meeting_time,
        )

        return redirect("forum_list")  # back to list page

    # show empty form
    return render(request, "forums/create_forum.html")


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(forum_post, pk=post_id)

    if request.method == "POST":
        text = request.POST.get("text")

        # owner can be none for now, dont forget to change
        author = request.user

        forum_comment.objects.create(post=post, author=author, comment_text=text)

        return redirect("post_detail", post_id=post_id)  # return to forum page

    return redirect("post_detail", post_id=post_id)
