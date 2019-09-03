# Euclid Rideshare API	

### Main

`<url>/`: Root url, provide the API reference

`<url>/driver/`: Driver schedule list; 

- `GET` retrieves a list of schedules associated with the authenticated user
- `POST` adds a new request

`<url>/driver/<pk>/`: Driver schedule details; `<pk>` a numbered index of the primary key of a driver schedule;  

- `GET` retrieves the specified schedule
- `POST` fully updates the specified schedule
- `PATCH` partially updates the specified schedule
- `DELETE` deletes the specified schedule

`<url>/rider/`: Rider schedule list; 

- `GET` retrieves a list of schedules
- `POST` adds a new request

`<url>/rider/<pk>/`: rider schedule details; `<pk>` a numbered index of the primary key of a rider schedule;  

- `GET` retrieves the specified schedule
- `POST` fully updates the specified schedule
- `PATCH` partially updates the specified schedule
- `DELETE` deletes the specified schedule

`<url>/account/`: information for current logged-in account

- `GET` retrieves the account information for the account that is currently logged in

`<url>/account/register/`: register for a new account

- `POST` creates a new account

### Token Authentication

`<url>/token/authorize/`: obtain authorization token

- `POST` username and password to obtain a authorization token

`<url>/token/refresh/`: refresh current authoziation token

- `POST` token to refresh the token

When using token authorization, the client must include token as the header of the HTTP message for the system to function correctly.

- i.e. `Authorization: Token <Token>`







