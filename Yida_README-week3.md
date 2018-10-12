# Yida README Week 3

## Design & MISC

- Hosting the django project to the AWS
  - Architecture: Apache2 + uwsgi
  - Status: Spent a couple of hours on it and failed to deploy, due to error in configurations

## Implementation

- Customized user model
  - `Client` and `ClientManager` in `api/models.py`
  - Email address should be validated before saving to the database using `api.verifications.validate_case_email`
  - Changes to related fields such as `settings.AUTH_USER_MODEL`

- User information access point on the website
  - `ClientSerializer` in `api/serializer.py` to serialize user
- Email token verification status update
  - Changes in concept:
    - Django template is used in order to provide flexibility of the email message body
      - The template should be placed under `<PROJECT>/templates/<APP_NAME>`
      - The name of the template should be `email_<template_prefix>_[subject | body].txt`
      - Current method only supports plain text emails, will consider using html email later (Stretch goal)
  - Implementations in `api/verifications.py`
    - `send_email_with_templates`
    - `get_verification_token` 
      - Uses python lib `uuid` to provide platform independent random verification token

## Todo for Week 4

- Add permissions to the API

- Create access interface for client registration
- Create API navigation page for access to the APIs

- From Week 3: 
  - Automated deployment from gitlab to AWS
  - Write test for Models