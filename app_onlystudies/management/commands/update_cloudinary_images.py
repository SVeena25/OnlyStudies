"""
Django management command to update blog post featured images with Cloudinary URLs
Usage: python manage.py update_cloudinary_images
"""

from django.core.management.base import BaseCommand
from app_onlystudies.models import BlogPost


class Command(BaseCommand):
    help = 'Update blog post featured images with Cloudinary URLs interactively'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Cloudinary Image Updater ===\n'))
        
        blog_posts = BlogPost.objects.all()
        
        if not blog_posts.exists():
            self.stdout.write(self.style.WARNING('No blog posts found.'))
            return
        
        self.stdout.write(f'Found {blog_posts.count()} blog posts.\n')
        
        for idx, post in enumerate(blog_posts, 1):
            self.stdout.write(f'\n[{idx}/{blog_posts.count()}] {post.title}')
            self.stdout.write(f'Current image: {post.featured_image or "None"}')
            
            user_input = input('\nEnter new Cloudinary URL (or press Enter to skip): ').strip()
            
            if user_input:
                if 'cloudinary.com' in user_input:
                    post.featured_image = user_input
                    post.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Updated: {post.title}'))
                else:
                    self.stdout.write(self.style.ERROR('✗ Invalid URL - must be a Cloudinary URL'))
            else:
                self.stdout.write('⊘ Skipped')
        
        self.stdout.write(self.style.SUCCESS('\n=== Update Complete ==='))
