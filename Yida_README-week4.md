# Yida README Week 4

## Design & MISC

- Hosting the django project on AWS
  - Architecture
    - AWS T3 Micro
    - Nginx (Webserver)
    - Gunicorn (Python WSGI HTTP Server)
  - Accessible via my own domain `api.extrasmisc.com`
  - Spent 10+ hours on this

## Implementation

- Reworked the views with Generic views of REST Framework
- Validate_case_email
  - Fixed error on domain
  - Add debug mode options that allows other type of emails to go through
- Client registration
  - Add registration serializer at `api/serializer.py`
  - Add registration API views at `api/views.py`
  - Add entry point at `api/urls.py`
- Email Verification
  - Configured the mail templates at `templates/api/`
  - Send mail with templates at `api/mails.py`

## Todo for Week 5

- Token authentications
- Email verification
- Documentations for server configurations guide
- Figure out ways to add HTTPS for security