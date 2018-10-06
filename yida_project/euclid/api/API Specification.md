## API Specification

`url/`: Root url, provide the API reference

`url/driver/`: Driver schedule list; 

- `GET` retrieves a list of schedules associated with the authenticated user
- `POST` adds a new request

`/url/driver/<pk>/`: Driver schedule details; `<pk>` a numbered index of the primary key of a driver schedule;  

- `GET` retrieves the specified schedule
- `POST` fully updates the specified schedule
- `DELETE` deletes the specified schedule

`url/rider/`: Rider schedule list; 

- `GET` retrieves a list of schedules
- `POST` adds a new request

`/url/rider/<pk>/`: rider schedule details; `<pk>` a numbered index of the primary key of a rider schedule;  

- `GET` retrieves the specified schedule
- `POST` fully updates the specified schedule
- `DELETE` deletes the specified schedule