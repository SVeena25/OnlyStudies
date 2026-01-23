# Security Configuration for OnlyStudies

"""
Security best practices implemented:

1. Password Security:
   - Passwords are hashed using Django's PBKDF2 algorithm
   - Password validation enforces:
     * Minimum 8 characters
     * Mix of uppercase and lowercase letters
     * Numbers and special characters
   - Password confirmation to prevent typos

2. CSRF Protection:
   - CSRF tokens on all forms
   - CSRF middleware enabled by default in Django
   - Forms use {% csrf_token %} template tag

3. SQL Injection Prevention:
   - Django ORM parameterizes all queries
   - No raw SQL queries in forms

4. User Input Validation:
   - Email validation using EmailField
   - Username uniqueness check
   - Email uniqueness check
   - Username minimum length (3 characters)

5. Session Security:
   - Sessions stored server-side by default
   - Session cookie HTTP-only flag
   - Session cookie secure flag (set to True in production)

6. Authentication:
   - Built-in Django authentication system
   - Password hashing with salt
   - User login required for protected views

7. Rate Limiting (to be added):
   - Consider using django-ratelimit for login attempts
   - Prevents brute force attacks

8. HTTPS (Production):
   - Always use HTTPS in production
   - Set SECURE_SSL_REDIRECT = True
   - Set SECURE_BROWSER_XSS_FILTER = True
   - Set SECURE_CONTENT_SECURITY_POLICY = True

9. Settings to configure in production:
   - DEBUG = False
   - SECRET_KEY = use environment variable
   - ALLOWED_HOSTS = specific domain
   - SESSION_COOKIE_SECURE = True
   - SESSION_COOKIE_HTTPONLY = True
   - CSRF_COOKIE_SECURE = True
   - CSRF_COOKIE_HTTPONLY = True
"""

# Django settings.py configurations needed:

# Password validation (already configured in Django)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# CSRF settings
CSRF_COOKIE_SECURE = True  # Only send over HTTPS (production)
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ['yourdomain.com']  # Set in production

# Session settings
SESSION_COOKIE_SECURE = True  # Only send over HTTPS (production)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security headers (production)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
}

# Login settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
