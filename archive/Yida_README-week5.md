# Yida README Week 5

## Design & MISC

- Deployed HTTPS to `api.extrasmisc.com`
  - AWS *Elastic Load Balancer* (ELB)
    - The inbound connection to the ELB is HTTPS enforced
    - The Webserver does not expose the HTTP connection to from the public IP
  - AWS *Certificate Manager*
    - Provides the Amazon signed CA to the domain

- Restructured and modularized the original `api` module
  - Two parts
    - `euclid_userauth` handles the user registration and authorization
    - `euclid_schedule` handles Driver and Rider schedules
  - Utilizes the design principle of Django Applications
  - The functionalities were preserved
  - Reduced the coupling of programs and provides a clearer structure

## Implementation

- Token authentications
  - Uses `restframework_jwt` as the Token generator
  - Provides Token authorization and refresh.
  - Client transmits information with the token included as the header of the HTTP request
    - Header form: `Authorization: token <token> `
  - Add entry point at `api_root` for the token authorization and refresh
- Removed `driver_posts` & `rider_posts` from `ClientSerializer`
  - Redundancy: client could always retrieve the list of driver/rider schedules related to current user from other api entries
- Replaced`ClientList` and `ClientDetails` by `CurrentClient`:
  - The two previous class-based views is not straight forward and puts redundancy
  - `CurrentClient` provides more integration of both views
- Updated `DriverSchedule` and `RiderSchedule` with an abstract based class
- Email Verification
  - New package `euclid_verification` handles models and views for email verification token
  - Logic for creating token for each client at registration, at `euclid_userauth/views`
  - HTML Templates for websites, at `templates/api` 

## Todo for Week 6

- Guide to server configurations
- Update the API specification
- Fixme:
  - Make email un-editable once created
  - Allow password change