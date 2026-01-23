from app_onlystudies.models import BlogPost

# Update Time Management blog post
post = BlogPost.objects.get(title__icontains='Time Management')
post.featured_image = 'https://res.cloudinary.com/dzuzzg6cy/image/upload/v1769211044/Time_Management_wks5vh.png'
post.save()

print(f'✓ Image updated successfully for: {post.title}')
print(f'Image URL: {post.featured_image}')
