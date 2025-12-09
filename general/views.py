from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from products.models import products
from general.models import Tag
from django.db.models import Q


class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            context["favorites"] = user.favorite_books.all()
            context["owned_books"] = user.user_owned_products.all()
        else:
            context["favorites"] = []
            context["owned_books"] = []

        # NEW
        # Favorite-genre recommendations
        fav_genre = None
        if user.is_authenticated:
            fav_genre = getattr(user, "favorite_genre", None)

        if fav_genre:
            if isinstance(fav_genre, Tag):
                genre_qs = products.objects.filter(
                    product_tags_m2m=fav_genre
                ).distinct()
                fav_genre_label = fav_genre.name
            else:
                fav_genre_label = str(fav_genre)
                genre_qs = products.objects.filter(
                    Q(product_tags_m2m__name__iexact=fav_genre_label)
                    | Q(product_tags__icontains=fav_genre_label)
                ).distinct()

            context["favorite_genre_label"] = fav_genre_label
            context["genre_recs"] = genre_qs.order_by("-product_id")[:4]
            context["has_genre_recs"] = genre_qs.exists()
        else:
            context["favorite_genre_label"] = ""
            context["genre_recs"] = products.objects.none()
            context["has_genre_recs"] = False

        # New & Noteworthy – most recently added books
        context["recent_books"] = products.objects.all().order_by("-product_id")[:4]

        return context
