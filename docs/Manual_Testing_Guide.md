# OnlyStudies Manual Testing Guide

This guide provides step-by-step scenarios to validate the core features of the OnlyStudies application. Each scenario includes prerequisites, steps, and expected results.

## Prerequisites
- Python virtual environment activated
- Migrations applied
- Development server running

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Authentication

### Sign Up
- Steps:
  - Navigate to `/signup`.
  - Fill `username`, `email`, `password`, confirm password.
  - Submit.
- Expected:
  - Redirect to home.
  - User session is active.

### Login / Logout
- Steps:
  - Visit `/login` and authenticate.
  - Confirm header shows logged-in state.
  - Visit `/logout`.
- Expected:
  - Login redirects to home.
  - Logout redirects to home and clears session.

## Blog

### Blog Feed
- Steps:
  - Visit `/blog`.
- Expected:
  - Published posts listed with title, author, category, created date.

### Blog Detail
- Steps:
  - Click a blog post.
- Expected:
  - Post content, related posts, author info.

### Delete Blog Post (Author Only)
- Pre-req: Authored post exists.
- Steps:
  - Open your post detail.
  - Click `Delete`.
  - Confirm.
- Expected:
  - Success message.
  - Redirect to blog feed.
  - Post no longer listed.

## Forum

### Forum List
- Steps:
  - Visit `/forum`.
- Expected:
  - Questions listed with category and answer counts.

### Ask Question (Logged In)
- Steps:
  - Visit `/forum/ask`.
  - Submit title, content, category.
- Expected:
  - Success message.
  - Redirect to question detail.

### Question Detail + Answers
- Steps:
  - Open a question.
  - Post an answer using the form.
- Expected:
  - Answer appears under the question.
  - `is_answered` toggles on first answer.

### Delete Question/Answer (Author Only)
- Steps:
  - For your question/answer, click `Delete`.
  - Confirm.
- Expected:
  - Success message.
  - Redirect appropriately (forum/question page).
  - Item is removed.

## Categories & Subcategories
- Steps:
  - Visit `/category/<slug>`.
  - Visit `/category/<category-slug>/<subcategory-slug>`.
- Expected:
  - Category page lists subcategories.
  - Subcategory page shows scoped content.

## Notifications

### Full List
- Steps:
  - Visit `/notifications` (logged in).
- Expected:
  - Notifications listed, unread indicated.

### API
- Steps:
  - GET `/api/notifications` unauthenticated.
- Expected:
  - 401 Unauthorized.
- Steps:
  - GET `/api/notifications` authenticated.
- Expected:
  - 200 OK; JSON payload of unread notifications.

## Home Page UX: View Updates Button
- Steps:
  - On home page, click `View Updates`.
- Expected:
  - Inline Bootstrap alert displays.
  - Notifications card refreshes.

## Search
- Steps:
  - Visit `/search?q=<term>`.
- Expected:
  - Blog and forum results for the query.

## Tasks: Filtering & Sorting
- Pre-req: Create tasks via admin or shell; `created_by`=current user.
- Steps:
  - Visit `/tasks` (logged in).
  - Filter by `category`, `priority`, `due_before`, `due_after`.
  - Sort by `due_asc/due_desc`, `priority_asc/desc`, `title_asc/desc`, `created_desc`.
- Expected:
  - Task list reflects filters and sorts.
  - Badges show priority and due date.

## Appointments: Booking & Management
- Pre-req: Logged in user.
- Steps:
  - Visit `/appointments`.
  - Click `Book Appointment`.
  - Fill title, select date & time (datetime-local), add optional notes.
  - Submit.
- Expected:
  - Success message displayed.
  - Redirect to appointments list.
  - Appointment visible with scheduled date/time.
  - Badge shows "Scheduled" status.

## Security (Production)
- Pre-req: `DEBUG=False` environment.
- Steps:
  - Deploy or simulate `DEBUG=False`.
- Expected:
  - SSL redirect and secure cookies enabled.
  - HSTS/CSP headers applied (per settings).

## Data Seeding (Optional)
- Steps:
  - Run management commands:
```
python manage.py populate_categories
python manage.py populate_blog_data
```
- Expected:
  - Categories and sample posts added.

## Troubleshooting
- Run diagnostics:
```
python manage.py check
python manage.py test
```
- Verify environment:
  - Local dev uses `env.py` for `DEBUG=True`.
  - Production defaults `DEBUG=False`.
