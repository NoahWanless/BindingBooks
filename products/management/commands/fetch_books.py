from django.core.management.base import BaseCommand
from products.models import products  # your model is named 'products'
import requests
import random

class Command(BaseCommand):
    help = "Fetch books from Open Library and add to products table"

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default="fiction", help="Search OpenLibrary for a topic")
        parser.add_argument('--count', type=int, default=40, help="Number of books to try to import")

    def handle(self, *args, **options):
        query = options['query']
        count = options['count']

        url = f"https://openlibrary.org/search.json?q={query}&limit={count}"  # API for search
        r = requests.get(url)
        if not r.ok:
            self.stderr.write("Failed to fetch data from Open Library.")
            return

        data = r.json()

        books_added = 0
        for obj in data.get('docs', []):
            title = obj.get('title')
            authors = obj.get('author_name', [])
            description = obj.get('first_sentence', [""])[0] if obj.get('first_sentence') else ""
            tags = obj.get('subject', [])[:5]
            ol_key = obj.get('key')
            cover_id = obj.get('cover_i')

            # Required fields
            if not title or not ol_key:
                continue

            # Build product fields
            product_name = title
            product_description = description[:500]
            product_price = round(random.uniform(7.99, 34.99), 2)
            product_tags = tags
            product_images = []
            if cover_id:
                product_images.append(f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg")
            product_text = ""  # Placeholder
            product_link = f"https://openlibrary.org{ol_key}"
            product_stripe_id = "PLACE_HOLDER"

            # Avoid duplicate titles+link if possible
            if products.objects.filter(product_name=product_name, product_link=product_link).exists():
                continue

            # Create instance
            p = products.objects.create(
                product_name=product_name,
                product_description=product_description,
                product_price=product_price,
                product_tags=product_tags,
                product_images=product_images,
                product_text=product_text,
                product_link=product_link,
                product_stripe_id=product_stripe_id,
            )
            books_added += 1

            if books_added >= count:
                break

        self.stdout.write(f"Added {books_added} new products from Open Library under query '{query}'.")
