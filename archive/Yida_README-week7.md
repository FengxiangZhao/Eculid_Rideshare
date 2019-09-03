# Yida README Week 7

## Design & MISC

- Updated the API specification at `API specification.md`
- Read Agatz et al. (2012) for a generic analysis for ridesharing algorithms

### Implementation

- Fixed Problem: Email is editable after creation and verification
  - In our case, email is a perpetual part that is related to a single account. User could only use accounts once their Case email is verified for security reasons.
  - Made `email` field read_only in `ClientSerializer` at `euclid_userauth/serializers.py`
- Allow client to change their password
  - Add `ClientPasswordChangeSerializer` for user password change at `euclid_userauth/serializers.py`
  - Add `ClientPasswordChange` view at `euclid_userauth/views.py `
- Changed content for schedule serializers at `euclid_schedules/serializers.py`

## Todo for Week 8

- Fix Problem:
  - Trips that have overlap in timeframe could be posted
- Utilize `celery` to perform asynchronous tasks (unblock)
  - email sending
  - matching algorithm

## Reference

- N. Agatz, A. Erera, M. Savelsbergh, and X. Wang, "Optimization for dynamic ride-sharing: A review," *European Journal of Operational Research,* vol 233, issue 2, 2012, pp 295 - 303, doi: [10.1016/j.ejor.2012.05.028](https://doi.org/10.1016/j.ejor.2012.05.028).

