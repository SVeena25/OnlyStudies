import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'only_studies.settings')
django.setup()

from app_onlystudies.models import BlogPost

# Update Effective Study Techniques blog post
post = BlogPost.objects.get(title__icontains='Effective Study Techniques')
post.featured_image = 'https://res.cloudinary.com/dzuzzg6cy/image/upload/v1769211043/how_to_bcm_teacher_grjew8.png'
post.save()

print(f'✓ Image updated successfully for: {post.title}')
print(f'Image URL: {post.featured_image}')
