# API Integration Documentation

## Overview
Simple API integration for blog feed and notifications has been successfully implemented.

## Features Implemented

### 1. Database Models
- **BlogPost**: Stores blog articles with featured images
  - Fields: title, content, author, category, featured_image, slug, is_published, timestamps
  
- **Notification**: Stores user notifications with type classification
  - Fields: user, title, message, notification_type, is_read, related_url, timestamps

### 2. API Endpoints

#### Blog Feed API
- **Endpoint**: `GET /api/blog-feed/`
- **Response Format**: JSON
```json
{
  "blogs": [
    {
      "id": 1,
      "title": "Blog Title",
      "content": "Preview of the content...",
      "author": "Author Name",
      "category": "Category Name",
      "featured_image": "/media/blog/image.jpg",
      "created_at": "2026-01-11T18:16:09Z",
      "slug": "blog-slug"
    }
  ]
}
```
- **Features**: Returns 5 most recent published blog posts
- **Authentication**: Not required

#### Notifications API
- **Endpoint**: `GET /api/notifications/`
- **Response Format**: JSON
```json
{
  "notifications": [
    {
      "id": 1,
      "title": "Notification Title",
      "message": "Notification message",
      "notification_type": "course",
      "is_read": false,
      "created_at": "2026-01-11T18:16:09Z"
    }
  ]
}
```
- **Features**: Returns 5 most recent unread notifications for authenticated user
- **Authentication**: Required (returns 401 if not authenticated)

### 3. Frontend Integration

#### JavaScript Implementation
The home page (`index.html`) includes automatic API fetching:

1. **Blog Feed Loading**:
   - Fetches from `/api/blog-feed/`
   - Displays latest blog post with featured image, title, author, date, and preview
   - Shows "Read More" button for each post
   - Fallback message if no posts available

2. **Notifications Loading**:
   - Fetches from `/api/notifications/`
   - Displays up to 5 latest unread notifications
   - Shows notification title, message, and date
   - Graceful fallback for unauthenticated users

### 4. Sample Data
Five blog posts have been created:
1. Tips for Passing Your MBA Exams
2. Engineering Mathematics Essentials
3. Medical Terminology for Healthcare Professionals
4. Effective Study Techniques for Online Learning
5. Time Management for Competitive Exams

Three notifications have been created for the admin user:
1. Welcome to OnlyStudies
2. New Blog Post Published
3. Achievement Unlocked

### 5. URL Routes
- `path('api/blog-feed/', views.blog_feed_api, name='blog_feed_api')`
- `path('api/notifications/', views.notifications_api, name='notifications_api')`

## How It Works

### Page Load Flow
1. User loads home page (`/`)
2. `index.html` loads with JavaScript in the `extra_js` block
3. JavaScript automatically fetches blog feed and notifications
4. Data is rendered dynamically into the respective containers
5. If user is not authenticated, notifications show fallback message

### Database Interactions
- BlogPost model is linked to Django User model (author)
- Notification model is linked to Django User model (recipient)
- All queries filter by published/unread status

### Error Handling
- API fetch errors are logged to console
- Graceful fallbacks displayed to users
- Unauthenticated users see "Sign in to view notifications"

## Testing

### Manual Testing
1. Visit http://127.0.0.1:8000/ to see home page with populated blog and notifications
2. Visit http://127.0.0.1:8000/api/blog-feed/ to see raw JSON response
3. Visit http://127.0.0.1:8000/api/notifications/ (requires login) to see notifications

### Admin Interface
Access Django admin at http://127.0.0.1:8000/admin/ to:
- View and manage BlogPost entries
- View and manage Notification entries
- Add new blog posts or notifications

## Files Modified/Created

### Created Files:
- `app_onlystudies/management/commands/populate_blog_data.py` - Management command for sample data
- `app_onlystudies/migrations/0002_notification_blogpost.py` - Database migration

### Modified Files:
- `templates/index.html` - Added JavaScript fetch integration
- `app_onlystudies/models.py` - Added BlogPost and Notification models
- `app_onlystudies/views.py` - Added blog_feed_api and notifications_api views
- `app_onlystudies/urls.py` - Added API endpoint routes
- `app_onlystudies/admin.py` - Added admin classes for new models

## Future Enhancements

Potential improvements for full integration:
- [ ] Pagination for blog posts (currently shows 5)
- [ ] Search functionality in blog feed
- [ ] Filtering by category
- [ ] Mark notifications as read via API
- [ ] Delete notifications
- [ ] Rich text editor for blog content
- [ ] Comments on blog posts
- [ ] Notifications for forum activity
- [ ] Email notification sending

## Deployment Notes

Before deploying to production:
1. Ensure Pillow is installed (`pip install Pillow`)
2. Configure MEDIA_URL and MEDIA_ROOT in settings.py
3. Collect static files: `python manage.py collectstatic`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Run populate_blog_data: `python manage.py populate_blog_data`
7. Configure allowed hosts in settings.py
8. Set DEBUG = False
9. Configure database settings for production

## Summary

The API integration provides a clean, simple approach to dynamic content loading without requiring Django REST Framework. The implementation follows Django best practices and is easily extensible for future features.
