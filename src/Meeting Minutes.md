## Meeting Minutes

### 

- Talk about the models in the backend
  - User model details
    - Remove twice password on server end, handle it in Client
  - Schedule
    - Departure datetime
      - Client choose between some datetime A - B
      - Parameter A, B-A (minutes)
    - Driver Time Constraint 
      - Driver Choose time constraint of k minute
      - Driver's route costs c minute
      - Then latest time driver should arrive \<driver arrive time> $<$ B + k + c

- Permissions [Proposed schema]
  - User could only see trips related to him/her
  - User must be verified to post trip [email]
  - Only anonymous user could register.
- Authentication
  - JWT
    - Obtain token using username and pw
    - An extra field in HTTP header `Authentication: JWT <your_token>`
    - Client logic: maintain a timer
      - if timer on token expired: auth again
      - if timer on token approach threshold, refresh token
  - Restframework session-based and basic

- Use `postman` as debugging tools