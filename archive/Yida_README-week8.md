# Yida README Week 8

## Design & MISC

- Updated project dependencies in `euclid/requirement.txt`
- Created tests at `tests/`
  - Achieved coverage rate of 85%
- Used `celery` as the asynchronous task scheduler
  - Installed `celery` Python package
  - Installed `rabbitMQ-server` as the intermediate task queue
- Reviewed a few papers (see reference) for more specific optimization models and algorithms for matching problem. 

### Implementation

- Use FCM devices to send notifications to the user
  - `userauth`: Add models and serializers for client to add the device information
  - `schedule`: Add abstract method for sending notification to driver and rider at `BaseSchedule`
- Added specific settings for `euclid_schedule/settings.py`
- Used `celery` tasks to replace the procedures for sending verification email, at `euclid_verfications` with an asynchronous one.

## Todo for Week 9

- Add additional checks and constrains on database models
- Work on the implementation of Matching algorithm

## Reference

- Agatz, Niels, Alan L. Erera, Martin WP Savelsbergh, and Xing Wang. "Dynamic ride-sharing: A simulation study in metro Atlanta." *Procedia-Social and Behavioral Sciences* 17 (2011): 532-550.
- Jaw, Jang-Jei, Amedeo R. Odoni, Harilaos N. Psaraftis, and Nigel HM Wilson. "A heuristic algorithm for the multi-vehicle advance request dial-a-ride problem with time windows." *Transportation Research Part B: Methodological* 20, no. 3 (1986): 243-257.
- Dumas, Yvan, Jacques Desrosiers, and Francois Soumis. "The pickup and delivery problem with time windows." *European journal of operational research* 54, no. 1 (1991): 7-22.

