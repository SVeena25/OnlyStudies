# OnlyStudies User Guide

## Overview
OnlyStudies is a study community platform offering blogs, a student forum, notifications, and personal task management.

## Getting Started
- Sign up at `/signup` or login at `/login`.
- Explore categories from the home page.

## Navigation
- Home: `/`
- Blog Feed: `/blog`
- Forum: `/forum`
- Ask a Question: `/forum/ask` (requires login)
- Notifications: `/notifications` (requires login)
- Tasks: `/tasks` (requires login)
- Appointments: `/appointments` (requires login)
- About: `/about`

## Features
- Blog: Read published posts; authors can delete their posts from the detail page.
- Forum: Ask questions, answer peers, and delete your own content.
- Notifications: See unread alerts relevant to your activity.
- Tasks: Filter and sort tasks by category, priority, and due date.
- Appointments: Book appointments, events, or services for specific date and time.

## Using Tasks
- Go to `/tasks`.
- Filter:
  - By category using the dropdown.
  - By priority: `low`, `medium`, `high`.
  - By due date range: `due_before`, `due_after` in `YYYY-MM-DD`.
- Sort:
  - `due_asc`, `due_desc`, `priority_asc`, `priority_desc`, `title_asc`, `title_desc`, `created_desc`.

## Booking Appointments
- Go to `/appointments` to view your scheduled appointments.
- Click `Book Appointment` to create a new booking.
- Fill in:
  - Title: Name of appointment/event/service.
  - Date & Time: Use the datetime picker.
  - Notes: Optional additional details.
- After booking, your appointment appears in the list with scheduled status.

## Notifications API
- Endpoint: `/api/notifications`
- Behavior:
  - Unauthenticated: returns 401 Unauthorized.
  - Authenticated: JSON list of latest unread notifications.

## Account Management
- Update password via default Django auth flows.
- Logout via `/logout`.

## Tips
- Use the footer quick links for fast navigation.
- Use search at `/search?q=term` to find content across blog and forum.

## Support
If you encounter issues, run diagnostics and contact the maintainer with logs:
```
python manage.py check
python manage.py test
```
