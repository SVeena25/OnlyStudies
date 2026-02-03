"""
Django management command to generate a complete static site export.
Exports all public pages to static HTML files that can be hosted without Django.
"""

import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.test import Client
from django.urls import reverse
from django.conf import settings
from app_onlystudies.models import Category, SubCategory, BlogPost


class Command(BaseCommand):
    help = 'Generate a complete static site export that can be hosted without Django'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='static_export',
            help='Output directory for static site (default: static_export)',
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output'])
        
        # Create output directory
        if output_dir.exists():
            self.stdout.write(self.style.WARNING(f'Removing existing {output_dir} directory...'))
            shutil.rmtree(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        self.stdout.write(self.style.SUCCESS(f'Created output directory: {output_dir}'))

        # Step 1: Collect static files
        self.stdout.write(self.style.HTTP_INFO('Step 1: Collecting static files...'))
        self.collect_static_files(output_dir)

        # Step 2: Generate static HTML pages
        self.stdout.write(self.style.HTTP_INFO('Step 2: Generating static HTML pages...'))
        self.generate_static_pages(output_dir)

        # Step 3: Create index and sitemap
        self.stdout.write(self.style.HTTP_INFO('Step 3: Creating index and configuration files...'))
        self.create_config_files(output_dir)

        self.stdout.write(self.style.SUCCESS(f'\n✓ Static site export complete!'))
        self.stdout.write(f'Static site location: {output_dir.absolute()}')
        self.stdout.write(f'Open: {(output_dir / "index.html").absolute()}\n')

    def collect_static_files(self, output_dir):
        """Collect all static files to the output directory"""
        static_dir = output_dir / 'static'
        static_dir.mkdir(exist_ok=True)

        # Copy static files from Django's static directories
        for static_location in settings.STATICFILES_DIRS:
            if Path(static_location).exists():
                for item in Path(static_location).iterdir():
                    dest = static_dir / item.name
                    if item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Static files collected'))

    def generate_static_pages(self, output_dir):
        """Generate static HTML pages for all public URLs"""
        client = Client()
        
        # List of public URLs to export
        public_urls = [
            ('', 'index.html'),  # Home
            ('about/', 'about.html'),  # About
            ('blog/', 'blog.html'),  # Blog Feed
            ('forum/', 'forum.html'),  # Forum
        ]

        # Generate public pages
        for url_path, filename in public_urls:
            try:
                response = client.get(f'/{url_path}')
                if response.status_code == 200:
                    output_file = output_dir / filename
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(response.content.decode('utf-8'))
                    self.stdout.write(f'  ✓ Generated {filename}')
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Failed to generate {filename} (status: {response.status_code})')
                    )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error generating {filename}: {str(e)}'))

        # Generate category pages
        self.stdout.write('  Generating category pages...')
        categories = Category.objects.all()
        for category in categories:
            try:
                response = client.get(reverse('category', args=[category.slug]))
                if response.status_code == 200:
                    cat_dir = output_dir / 'categories'
                    cat_dir.mkdir(exist_ok=True)
                    output_file = cat_dir / f'{category.slug}.html'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(response.content.decode('utf-8'))
                    self.stdout.write(f'    ✓ Generated category: {category.name}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'    ⚠ Error generating {category.slug}: {str(e)}'))

        # Generate subcategory pages
        self.stdout.write('  Generating subcategory pages...')
        subcategories = SubCategory.objects.all()
        for subcategory in subcategories:
            try:
                response = client.get(
                    reverse('subcategory', args=[subcategory.category.slug, subcategory.slug])
                )
                if response.status_code == 200:
                    subcat_dir = output_dir / 'subcategories'
                    subcat_dir.mkdir(exist_ok=True)
                    output_file = subcat_dir / f'{subcategory.slug}.html'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(response.content.decode('utf-8'))
                    self.stdout.write(f'    ✓ Generated subcategory: {subcategory.name}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'    ⚠ Error generating {subcategory.slug}: {str(e)}'))

        # Generate blog post detail pages
        self.stdout.write('  Generating blog post pages...')
        blog_posts = BlogPost.objects.all()
        for post in blog_posts:
            try:
                response = client.get(reverse('blog_detail', args=[post.slug]))
                if response.status_code == 200:
                    blog_dir = output_dir / 'blog'
                    blog_dir.mkdir(exist_ok=True)
                    output_file = blog_dir / f'{post.slug}.html'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(response.content.decode('utf-8'))
                    self.stdout.write(f'    ✓ Generated blog post: {post.title}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'    ⚠ Error generating {post.slug}: {str(e)}'))

    def create_config_files(self, output_dir):
        """Create additional configuration files"""
        # Create a README for the static site
        readme_content = """# OnlyStudies Static Site Export

This is a static HTML version of the OnlyStudies application.

## Contents

- `index.html` - Home page
- `about.html` - About page
- `blog.html` - Blog feed
- `forum.html` - Forum
- `static/` - CSS, JavaScript, and images
- `categories/` - Category pages
- `subcategories/` - Subcategory pages
- `blog/` - Individual blog post pages

## Hosting

You can host this static site on:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

## Limitations

This is a static export and includes only read-only content. The following features are NOT included:
- User authentication/login
- Task management
- Appointments
- Forum posting/answering
- Blog post creation/editing
- Search functionality (requires backend)

To use these features, deploy the full Django application.

## Generated

Generated at: {timestamp}
"""
        from datetime import datetime
        readme_file = output_dir / 'README.md'
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content.format(timestamp=datetime.now().isoformat()))

        self.stdout.write(f'  ✓ Created README.md')

        # Create a .htaccess file for Apache servers
        htaccess_content = """# Enable GZIP compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Set proper caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 1 hour"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/jpeg "access plus 1 month"
  ExpiresByType image/gif "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
</IfModule>

# Rewrite rules for clean URLs
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  
  # Rewrite directory requests to index.html
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule ^(.*)$ index.html [L]
</IfModule>
"""
        htaccess_file = output_dir / '.htaccess'
        with open(htaccess_file, 'w', encoding='utf-8') as f:
            f.write(htaccess_content)

        self.stdout.write(f'  ✓ Created .htaccess')
