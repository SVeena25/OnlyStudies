# Production Security Hardening Guide

## Quick Implementation

### Step 1: Update Settings for Production

Add this to the bottom of `settings.py`:

```python
# Production Security Settings
if not DEBUG:
    # HTTPS/SSL
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Session & CSRF Cookie Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 1209600  # 2 weeks
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_AGE = 31449600  # 1 year
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Clickjacking Protection
    X_FRAME_OPTIONS = 'DENY'
    
    # Content Security Policy
    SECURE_CONTENT_SECURITY_POLICY = {
        "default-src": ("'self'",),
        "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "code.jquery.com"),
        "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
        "img-src": ("'self'", "data:", "https:"),
        "font-src": ("'self'", "cdn.jsdelivr.net"),
        "connect-src": ("'self'",),
    }
```

### Step 2: Add Rate Limiting (Recommended)

Install package:
```bash
pip install django-ratelimit
```

Add to `middleware`:
```python
'django_ratelimit.middleware.RatelimitMiddleware',
```

Add to views:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST')
class CustomLoginView(LoginView):
    # Login attempts limited to 5 per hour per IP
    pass

@ratelimit(key='ip', rate='10/h', method='POST')
class SignUpView(CreateView):
    # Signup limited to 10 per hour per IP
    pass
```

### Step 3: Add Logging (Recommended)

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/security.log'),
            'formatter': 'verbose',
        },
        'auth_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/auth.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'authentication': {
            'handlers': ['auth_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Step 4: Update Custom Login View (Optional Enhancement)

```python
import logging
from django.contrib.auth.views import LoginView

logger = logging.getLogger('authentication')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_invalid(self, form):
        # Log failed login attempts
        username = form.cleaned_data.get('username', 'unknown')
        ip_address = self.get_client_ip()
        logger.warning(f'Failed login attempt - User: {username}, IP: {ip_address}')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        # Log successful login
        username = form.cleaned_data.get('username')
        ip_address = self.get_client_ip()
        logger.info(f'Successful login - User: {username}, IP: {ip_address}')
        return super().form_valid(form)
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
```

### Step 5: Environment Variables (Critical)

Create `.env` file (add to `.gitignore`):

```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

Never commit `.env` to version control!

### Step 6: Database Connection Hardening

```python
# Ensure database uses strong passwords
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

# Add connection pooling for production
if not DEBUG:
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
        'options': '-c default_transaction_isolation=read_committed'
    }
```

### Step 7: Security Headers Middleware (Optional Custom)

Create `middleware.py`:

```python
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
```

Add to `MIDDLEWARE`:
```python
MIDDLEWARE = [
    # ... other middleware
    'app_onlystudies.middleware.SecurityHeadersMiddleware',
]
```

---

## Pre-Deployment Checklist

### Critical ⚠️
- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is random and unique (40+ chars)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database credentials in environment variables
- [ ] HTTPS/SSL certificate configured
- [ ] `SECURE_SSL_REDIRECT = True`

### Important
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_HTTPONLY = True`
- [ ] `CSRF_COOKIE_HTTPONLY = True`
- [ ] Email SMTP configured for password resets
- [ ] Static files collected (`python manage.py collectstatic`)

### Monitoring
- [ ] Error logging configured
- [ ] Security event logging enabled
- [ ] Email alerts for errors
- [ ] Rate limiting implemented
- [ ] Database backups configured
- [ ] Firewall rules in place

---

## Testing Security Settings

Run Django's security check:

```bash
python manage.py check --deploy
```

This will verify all production security settings.

Expected output:
```
System check identified no issues (0 silenced).
```

---

## Common Security Issues Fixed

### ✅ Session Fixation
- Resolved by `SESSION_COOKIE_HTTPONLY = True`

### ✅ CSRF Attacks
- Protected by CSRF middleware + tokens

### ✅ Clickjacking
- Protected by `X_FRAME_OPTIONS = 'DENY'`

### ✅ Man-in-the-Middle
- Resolved by HTTPS enforcement + HSTS

### ✅ XSS Attacks
- Protected by Django auto-escaping + CSP

### ✅ SQL Injection
- Resolved by Django ORM usage

---

## References

- Django Deployment Checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Django Security: https://docs.djangoproject.com/en/4.2/topics/security/
- OWASP: https://owasp.org/
