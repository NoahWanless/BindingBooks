from django.core.management.base import BaseCommand
from products.models import products
# CHANGE 1: Capitalized 'Tag'
from general.models import Tag 
import requests
import random

class Command(BaseCommand):
    help = "Fetch books from Open Library Subjects API and add to products table"

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default="fiction", help="Subject to search (e.g., fiction, romance, science)")
        parser.add_argument('--count', type=int, default=10, help="Number of books to import")

    def handle(self, *args, **options):
        query = options['query'].lower()
        count = options['count']

        self.stdout.write(f"Fetching {count} books for subject: '{query}'...")

        # CHANGE 2: Used 'Tag.objects.all()' (Capital T)
        valid_tags_db = Tag.objects.all()
        tag_lookup = {t.name.lower(): t for t in valid_tags_db}
        
        self.stdout.write(f"Loaded {len(tag_lookup)} valid tags from database.")

        url = f"https://openlibrary.org/subjects/{query}.json?limit={count}"
        
        headers = {
            "User-Agent": "DjangoBookFetcher/1.0" 
        }

        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(f"Failed to connect to Open Library: {e}")
            return

        data = r.json()
        books_added = 0
        
        for obj in data.get('works', []):
            ol_key = obj.get('key')
            title = obj.get('title')
            cover_id = obj.get('cover_id')

            if not title or not ol_key:
                continue

            matching_tag_objects = []
            
            try:
                details_url = f"https://openlibrary.org{ol_key}.json"
                response = requests.get(details_url, headers=headers, timeout=5)
                
                if response.ok:
                    ol_subjects = response.json().get('subjects', [])
                    for subject in ol_subjects:
                        subject_lower = subject.lower()
                        if subject_lower in tag_lookup:
                            matching_tag_objects.append(tag_lookup[subject_lower])
            except requests.RequestException:
                pass 

            if not matching_tag_objects and query in tag_lookup:
                matching_tag_objects.append(tag_lookup[query])

            raw_authors = obj.get('authors', [])
            author_names = [a.get('name') for a in raw_authors if 'name' in a]
            description = f"A book by {', '.join(author_names[:2])}"

            product_name = title
            product_description = description[:500]
            product_price = round(random.uniform(7.99, 34.99), 2)
            
            product_tags_list = [t.name for t in matching_tag_objects]
            
            product_images = []
            if cover_id:
                product_images.append(f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg")
            
            product_link = f"https://openlibrary.org{ol_key}"
            product_stripe_id = "PLACE_HOLDER"

            if products.objects.filter(product_name=product_name, product_link=product_link).exists():
                self.stdout.write(f"Skipping existing: {title}")
                continue

            new_product = products.objects.create(
                product_name=product_name,
                product_description=product_description,
                product_price=product_price,
                product_tags=product_tags_list,
                product_images=product_images,
                product_text="",
                product_link=product_link,
                product_stripe_id=product_stripe_id,
            )
            
            if matching_tag_objects:
                new_product.product_tags_m2m.set(matching_tag_objects)

            books_added += 1
            self.stdout.write(f"Imported: {title} with tags: {product_tags_list}")

            if books_added >= count:
                break

        self.stdout.write(self.style.SUCCESS(f"Successfully added {books_added} new products."))