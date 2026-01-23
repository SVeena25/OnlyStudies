import os
from django.core.management.base import BaseCommand
from django.core.files import File
from app_onlystudies.models import BlogPost
from django.conf import settings


class Command(BaseCommand):
    help = 'Upload local media files to Cloudinary and update blog posts'

    def handle(self, *args, **kwargs):
        media_path = os.path.join(settings.BASE_DIR, 'media', 'blog')
        
        if not os.path.exists(media_path):
            self.stdout.write(self.style.ERROR(f'Media path does not exist: {media_path}'))
            return
        
        # Get all image files
        image_files = [f for f in os.listdir(media_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        self.stdout.write(f'Found {len(image_files)} images in {media_path}')
        
        blog_posts = BlogPost.objects.all()
        
        for post in blog_posts:
            # Try to find a matching image
            for image_file in image_files:
                # Match by post title or specific image name
                if (image_file.lower().replace('_', ' ').replace('-', ' ') in post.title.lower() or
                    'time' in image_file.lower() and 'time' in post.title.lower() or
                    'lighthouse' in image_file.lower()):
                    
                    image_path = os.path.join(media_path, image_file)
                    
                    try:
                        with open(image_path, 'rb') as img_file:
                            post.featured_image.save(
                                image_file,
                                File(img_file),
                                save=True
                            )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Uploaded {image_file} for "{post.title}"'
                            )
                        )
                        break
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'✗ Failed to upload {image_file}: {str(e)}'
                            )
                        )
        
        self.stdout.write(self.style.SUCCESS('\nUpload process completed!'))
