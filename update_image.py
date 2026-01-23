import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'only_studies.settings')
django.setup()

from app_onlystudies.models import BlogPost

# ============================================================================
# UPDATE THIS SECTION WITH YOUR BLOG POST TITLE AND CLOUDINARY IMAGE URL
# ============================================================================

POST_TITLE = 'Become a Teacher'  # Change this to the blog post title
CLOUDINARY_URL = 'https://res.cloudinary.com/dzuzzg6cy/image/upload/v1769211041/heroimage_p7uxkw.png'  # Change this to your Cloudinary URL

# ============================================================================
# Script execution
# ============================================================================

try:
    post = BlogPost.objects.get(title__icontains=POST_TITLE)
    post.featured_image = CLOUDINARY_URL
    post.save()
    
    print(f'✓ Image updated successfully!')
    print(f'  Blog Post: {post.title}')
    print(f'  Image URL: {post.featured_image}')
except BlogPost.DoesNotExist:
    print(f'✗ Error: Blog post with title containing "{POST_TITLE}" not found.')
    print(f'  Available blog posts:')
    for post in BlogPost.objects.all():
        print(f'    - {post.title}')
except Exception as e:
    print(f'✗ Error: {str(e)}')
