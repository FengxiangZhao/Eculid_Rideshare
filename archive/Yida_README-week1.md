# Yida README Week 1



## Design & MISC

- Setting up environment for Django REST Framework
- Completed tutorial for Django REST Framework 
  - [Link to Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)
- Set up barebone Django project
- Planned on implementation on Sever
  - Set up environment for django REST framework
  - Collected information for required packages
  - Generated `yida_project/euclid/requirement.txt` for Python PIP package installation
    - `pip install -r path/to/requirement.txt` to install.
- Edited the [software requirement specification](https://docs.google.com/document/d/1rYNNf4dERF1G1OBTuB4JZ_6RRsQ7WoBdrNMG4ell7Pw/edit?usp=sharing) [Link require CWRU Google Account]
  - Earlier version available on `archive/`
  - Add Revision History
  - Add Access Service as the functional requirements

## Implementation

- Setup barebone project.
- Start a new application for the RESTful API, namely`api`
- Complete django database models in `api/models.py`
  - User: Use django default (will consider use custom user model for the project)
  - Schedule
    - origin and destination
    - the depart time and time range
    - DriverSchedule
      - driver's time constraint: the maximum extra time that the driver would like to spend on sending riders.
    - RiderSchedule
      - matched driver: the driver that will take the rider, as Foreign Key.
- Create serializers for each of the models. `api/serializers.py`

## Todo for Week 2

- Create simple views that has the functionality of RESTful API (The simplest form, without things like permission control)
- Determine the detailed API with Fengxiang.
- Create test for modules