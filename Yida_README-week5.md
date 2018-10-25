# Yida README Week 5

## Design & MISC

- Deployed HTTPS to `api.extrasmisc.com`
  - AWS *Elastic Load Balancer* (ELB)
    - The inbound connection to the ELB is HTTPS enforced
    - The Webserver does not expose the HTTP connection to from the public IP
  - AWS *Certificate Manager*
    - Provides the Amazon signed CA to the domain

- 

## Implementation

- Token authentications
  - Uses `restframework_jwt` as the Token generator
  - Usage
    - Client POST credentials to `<url>/api/jwt/auth` to receive the login token
    - Client transmits information with the token included as the header of the HTTP request
      - Header form: `Authorization: token <token> `
    - Token will expire in a short period of time and the client should POST the old token to `<url>/api/jwt/refresh` to refresh the token.
  - Add entry point at `api_root` for the token authorization and refresh
- Removed `driver_posts` & `rider_posts` from `ClientSerializer`
  - Redundancy: client could always retrieve the list of driver/rider schedules related to current user from other api entries
- Replaced`ClientList` and `ClientDetails` by `CurrentClient`:
  - The two previous class-based views is not straight forward and puts redundancy
  - `CurrentClient` provides more integration of both views
- Updated `DriverSchedule` and `RiderSchedule` with an abstract based class
- 

## Todo for Week 6

- Guide to server configurations
- Fix:
  - Make email un-editable once created
  - Allow password change