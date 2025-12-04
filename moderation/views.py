from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .models import ModerationQueue

@staff_member_required
def moderation_queue(request):
    items = ModerationQueue.objects.filter(status="pending").order_by("submitted_at")
    return render(request, "moderation/queue.html", {"items": items})


@staff_member_required
def review_item(request, pk):
    item = get_object_or_404(ModerationQueue, pk=pk)

    if request.method == "POST":
        if "approve" in request.POST:
            item.status = "approved"
            item.content_object.approved = True
            item.content_object.save()
        elif "reject" in request.POST:
            item.status = "rejected"
            item.content_object.approved = False
            item.content_object.save()
        item.reviewed_by = request.user
        item.save()
        return redirect("moderation_queue")
    

    return render(request, "moderation/review.html", {"item": item})
