from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Category, SubCategory, BlogPost, Notification, ForumQuestion, ForumAnswer, Task, Appointment


class CloudinaryUploadWidget(forms.widgets.TextInput):
    """
    Custom widget for Cloudinary image upload in admin
    """
    template_name = 'admin/cloudinary_upload_widget.html'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'vTextField',
            'placeholder': 'Paste Cloudinary image URL here'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class BlogPostAdminForm(forms.ModelForm):
    """
    Custom form for BlogPost with Cloudinary upload widget
    """
    
    class Meta:
        model = BlogPost
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace the featured_image widget with custom Cloudinary widget
        self.fields['featured_image'].required = False
        self.fields['featured_image'].widget = CloudinaryUploadWidget()
        self.fields['featured_image'].widget.attrs.update({
            'placeholder': 'Paste Cloudinary image URL here or use the upload button below'
        })
        self.fields['featured_image'].label = 'Featured Image (Cloudinary URL)'
        self.fields['featured_image'].help_text = 'Upload via Cloudinary widget or paste a Cloudinary image URL'
    
    def clean_featured_image(self):
        """
        Handle Cloudinary URL properly - convert to just the path/URL string
        """
        featured_image = self.cleaned_data.get('featured_image')
        
        # If it's empty or None, return as is
        if not featured_image:
            return featured_image
        
        # If it's already a string (Cloudinary URL), return it
        if isinstance(featured_image, str):
            return featured_image
        
        # If it has a .name attribute, it's a file upload - return as is
        if hasattr(featured_image, 'name'):
            return featured_image
        
        # Otherwise convert to string
        return str(featured_image) if featured_image else None


class SubCategoryInline(admin.TabularInline):
    """
    Inline admin for subcategories
    """
    model = SubCategory
    extra = 1
    fields = ('name', 'slug', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for Category model
    """
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]
    search_fields = ('name', 'description')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Admin for SubCategory model
    """
    list_display = ('name', 'category', 'slug', 'created_at')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin for BlogPost model with Cloudinary upload support
    """
    form = BlogPostAdminForm
    list_display = ('title', 'author', 'category', 'image_preview', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at', 'image_preview_large')
    
    fields = ('title', 'slug', 'author', 'category', 'content', 'featured_image', 'image_preview_large', 'is_published')
    
    def image_preview(self, obj):
        """
        Display image preview in list view
        """
        try:
            if not obj.featured_image:
                return '—'
            
            # Get the URL - handle both ImageField and direct URL strings
            img_str = str(obj.featured_image)
            
            # Check if it's already a full URL (starts with http/https)
            if img_str.startswith(('http://', 'https://')):
                img_url = img_str
            elif hasattr(obj.featured_image, 'url'):
                # It's an ImageField, get the URL
                img_url = obj.featured_image.url
            else:
                img_url = img_str
            
            if img_url and img_url.strip() and not img_url.startswith('/media/http'):
                return format_html(
                    '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                    img_url
                )
        except Exception:
            pass
        return '—'
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        """
        Display large image preview in detail view
        """
        try:
            if not obj.featured_image:
                return format_html(
                    '<div style="padding: 10px; background-color: #f9f9f9; border-radius: 4px; border: 1px dashed #ccc;">'
                    '<p style="margin: 0; color: #999;">No image uploaded yet</p>'
                    '<p style="margin: 8px 0 0 0; font-size: 12px; color: #666;">Upload a Cloudinary image URL above</p>'
                    '</div>'
                )
            
            # Get the URL - handle both ImageField and direct URL strings
            img_str = str(obj.featured_image)
            
            # Check if it's already a full URL (starts with http/https)
            if img_str.startswith(('http://', 'https://')):
                img_url = img_str
            elif hasattr(obj.featured_image, 'url'):
                # It's an ImageField, try to get URL but fallback to string
                try:
                    url_value = obj.featured_image.url
                    # Check if Django mangled it by adding /media/
                    if url_value.startswith('/media/http'):
                        img_url = img_str  # Use original string
                    else:
                        img_url = url_value
                except:
                    img_url = img_str
            else:
                img_url = img_str
            
            if img_url and img_url.strip():
                return format_html(
                    '<div style="margin: 10px 0;">'
                    '<img src="{}" style="max-width: 400px; max-height: 300px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd; padding: 8px;" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'block\';" />'
                    '<p style="display: none; margin: 10px 0; padding: 10px; background: #fff3cd; border-radius: 4px; color: #856404;">Image failed to load. Check URL.</p>'
                    '<p style="margin-top: 8px; font-size: 12px; color: #666;"><strong>URL:</strong> <code style="background: #f5f5f5; padding: 4px 6px; border-radius: 3px; word-break: break-all;">{}</code></p>'
                    '</div>',
                    img_url,
                    img_url
                )
        except Exception as e:
            return format_html(
                '<div style="padding: 10px; background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 4px;">'
                '<p style="margin: 0; color: #856404;">Error loading image preview</p>'
                '<p style="margin: 5px 0 0 0; font-size: 11px; color: #666;">Error: {}</p>'
                '</div>',
                str(e)
            )
        
        return format_html(
            '<div style="padding: 10px; background-color: #f9f9f9; border-radius: 4px; border: 1px dashed #ccc;">'
            '<p style="margin: 0; color: #999;">No image uploaded yet</p>'
            '</div>'
        )
    image_preview_large.short_description = 'Image Preview'
    
    def save_model(self, request, obj, form, change):
        """
        Custom save to handle Cloudinary URL in featured_image field
        """
        # If featured_image was changed and it's a URL string, save it directly
        if 'featured_image' in form.changed_data:
            featured_image = form.cleaned_data.get('featured_image')
            if featured_image and isinstance(featured_image, str):
                # It's a Cloudinary URL string, assign it directly
                obj.featured_image = featured_image
        
        super().save_model(request, obj, form, change)
    
    def get_fields(self, request, obj=None):
        """
        Show timestamps only when editing
        """
        fields = list(super().get_fields(request, obj))
        if obj:  # Editing existing object
            fields.extend(['created_at', 'updated_at'])
        return fields
    
    class Media:
        css = {
            'all': ('admin/css/cloudinary_admin.css',)
        }
        js = ('admin/js/cloudinary_admin.js',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin for Notification model
    """
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Links', {
            'fields': ('related_url',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)


class ForumAnswerInline(admin.TabularInline):
    """
    Inline admin for forum answers
    """
    model = ForumAnswer
    extra = 0
    readonly_fields = ('author', 'created_at')
    fields = ('author', 'content', 'is_accepted', 'created_at')


@admin.register(ForumQuestion)
class ForumQuestionAdmin(admin.ModelAdmin):
    """
    Admin for ForumQuestion model
    """
    list_display = ('title', 'author', 'category', 'is_answered', 'views', 'created_at')
    list_filter = ('is_answered', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('slug', 'views', 'created_at', 'updated_at')
    inlines = [ForumAnswerInline]
    
    fieldsets = (
        ('Question Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Status', {
            'fields': ('is_answered', 'views')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ForumAnswer)
class ForumAnswerAdmin(admin.ModelAdmin):
    """
    Admin for ForumAnswer model
    """
    list_display = ('question', 'author', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('content', 'author__username', 'question__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Answer Information', {
            'fields': ('question', 'author', 'is_accepted')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin for Task model
    """
    list_display = ('title', 'created_by', 'category', 'priority', 'due_date', 'created_at')
    list_filter = ('priority', 'category', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at',)
    fields = ('title', 'description', 'category', 'priority', 'due_date', 'created_by')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin for Appointment model
    """
    list_display = ('title', 'created_by', 'appointment_datetime', 'created_at')
    list_filter = ('appointment_datetime', 'created_at')
    search_fields = ('title', 'notes', 'created_by__username')
    readonly_fields = ('created_at',)
    fields = ('title', 'notes', 'appointment_datetime', 'created_by')


