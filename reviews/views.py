from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import products
from .models import Review


@login_required
def create_review(request):
    if request.method == "GET":
        context = {
            "products": products.objects.all(),
        }
        return render(request, "reviews/create_review.html", context)

    if request.method == "POST":

        product_id = request.POST.get("product_id")
        product = get_object_or_404(products, product_id=product_id)

        review_text = request.POST.get("review_text", "")

        star_rating = request.POST.get("star_rating", 1)
        spice_rating = request.POST.get("spice_rating", 1)
        violence_rating = request.POST.get("violence_rating", 1)

        review_tags = request.POST.getlist("review_tags")
        trigger_warnings = request.POST.getlist("trigger_warnings")

        Review.objects.create(
            author=request.user,
            product=product,
            review_text=review_text,
            star_rating=star_rating,
            spice_rating=spice_rating,
            violence_rating=violence_rating,
            review_tags=review_tags,
            trigger_warnings=trigger_warnings,
        )

        return redirect("product_details", product_id=product.product_id)
