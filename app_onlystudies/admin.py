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
            'placeholder': 'Paste Cloudinary image URL here or use the upload button below'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['cloudinary_upload'] = True
        return context


class BlogPostAdminForm(forms.ModelForm):
    """
    Custom form for BlogPost with Cloudinary upload widget
    """
    featured_image = forms.CharField(
        required=False,
        label='Featured Image (Cloudinary URL)',
        widget=CloudinaryUploadWidget(),
        help_text='Upload via Cloudinary widget or paste a Cloudinary image URL'
    )
    
    class Meta:
        model = BlogPost
        fields = '__all__'


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
        if obj.featured_image:
            if isinstance(obj.featured_image, str):
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.featured_image)
            elif obj.featured_image.url:
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.featured_image.url)
        return '—'
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        """
        Display large image preview in detail view
        """
        if obj.featured_image:
            if isinstance(obj.featured_image, str):
                return format_html(
                    '<div style="margin: 10px 0;">'
                    '<img src="{}" style="max-width: 400px; max-height: 300px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd; padding: 8px;" />'
                    '<p style="margin-top: 8px; font-size: 12px; color: #666;"><strong>URL:</strong> {}</p>'
                    '</div>',
                    obj.featured_image if isinstance(obj.featured_image, str) else obj.featured_image.url,
                    obj.featured_image if isinstance(obj.featured_image, str) else obj.featured_image.url
                )
        return format_html(
            '<div style="padding: 10px; background-color: #f9f9f9; border-radius: 4px; border: 1px dashed #ccc;">'
            '<p style="margin: 0; color: #999;">No image uploaded yet</p>'
            '<p style="margin: 8px 0 0 0; font-size: 12px; color: #666;">Upload a Cloudinary image URL above</p>'
            '</div>'
        )
    image_preview_large.short_description = 'Image Preview'
    
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


