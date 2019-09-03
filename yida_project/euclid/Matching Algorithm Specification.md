# Matching Algorithm

### Specifications

#### Driver

1. Driver can post new sharing schedule and the information is stored in the database

2. Matching
   1. If there is match, driver is notified by push notifications that a match is found, including the matched rider's information
   2. Prior to N minutes before scheduled departure, the driver's request will not be matched; The driver will receive a notification (reminder) about the trip, including the riders who will share the ride, if there are matches.
3. Modifying the trip / Modified Trip
   1. Prior to N minutes before the scheduled departure, the driver is able to modify the trip; After that, the driver could only cancel the trip. 
   2. If there is no matching yet, the driver could change any part of the trip.
   3. If there are matches already, the driver could only change a limited number of trip settings; These settings should not influence the existing matched rider; A force change will have the result of cancelling the existing trip and creating a new trip; 
   4. The driver is able to remove matched rider.
   5. Cancelling the existing trip will send all the matched rider to the queue

#### Rider

1. Rider can post new rider schedule and information is stored in the database
2. Matching
   1. Rider will be automatically matched with a driver.
   2. Rider's client will be notified by push message any updates: such as a match is found or driver cancelled the schedule
   3. Prior to N minutes before scheduled departure, if there is a match, the rider will receive a notification about the trip, including with whom he will be travelling, otherwise the rider would be notified with trip unsuccessful
   4. The rider's information will be placed in the to-be-matched queue; every time a new driver schedule comes in, it will be checked 

