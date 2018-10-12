# Yida README Week 2

## Design & MISC

- Amazon Web Service
  - Setting up educational account
  - Getting free-tier instance and public IPs
  - Install and setting up dependent packages
    - python dependencies
    - nginx
- Setting up private gitlab repository 
- Setting up an gmail account for the email verification

## Implementation

- Problem: Unable to use `PointField` provided by `GeoDjango`
  - `GeoDjango` requires installation for `libgdal` 
    - The installaition process is complicated on local machine.
    - Spent a lot of time on figure out the installation process and still failed to install on my machine.
  - Fix: Since we are using the longitude and latitude, use two `DecimalFields` with fixed digit instead.
- Created simple views that provides basic functionalities for the RESTful API
  - Details see `api/views.py` and `api/API Specifications.md`
  - ![screenshot](G:\My Drive\rideshare\img\w2-django-screenshot.png)
- Created simple permission class in `api/permissions.py`
  - Proposed to have `isOwner` permission for the `DriverSchedule` and `RiderSchedule` so that only owner could view the schedule they created.
  - Proposed to have `isVerifiedUserOrReadOnly` permission to restrict the behaviors of unverified users.
- Created barebone verification procedures in `api/verifications.py`
  - investigated how to send email using python
  - Create barebone method for verification email sending and generate verification token
  - Completed a regular expression to match Case id:
    - See line 4, `api/verifications.py`
    - Matches case id in the form \<three lower case letter>\<0-9999> 



## Todo for Week 3

- Automated deployment from gitlab to AWS
- Modify the user model in django to satisfy our needs
- Write test for database models
- Complete email token verification part
  - (?)Add a table to store token and user relation

