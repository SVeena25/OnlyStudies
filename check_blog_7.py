import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'only_studies.settings')
django.setup()

from app_onlystudies.models import BlogPost

try:
    p = BlogPost.objects.get(id=7)
    print(f'Title: {p.title}')
    print(f'Featured Image Type: {type(p.featured_image).__name__}')
    print(f'Featured Image Value: {repr(p.featured_image)}')
    print(f'Featured Image String: {str(p.featured_image)}')
    print(f'Has URL attr: {hasattr(p.featured_image, "url")}')
    
    if hasattr(p.featured_image, 'url'):
        try:
            print(f'URL value: {p.featured_image.url}')
        except Exception as e:
            print(f'Error getting URL: {e}')
except BlogPost.DoesNotExist:
    print('Blog post #7 does not exist')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
