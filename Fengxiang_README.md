### Updates of Fengxiang Zhao 





#### Week 7

11/08/2018

##### Goals

Minimum Deliverable Product finished

##### What I have done

- Started the integration with server
- Now the Client is able to Login/Register/Post/Find Trips
- Client is able to edit their account info in client
- Many small improvement for user experience

##### Todo 

- Keep working on communicate with server.
- Complete the matching algorithm with Yida
- Start some testing





#### Week 6

11/02/2018

##### Goals

Implementation of communication with server

##### What I have done

- Complete the registration for users
- Discussed about how to start our integration (With note `Meeting Minutes.md`)
- Some changes of `LoginActivity` (Added a helper method but waiting for more integration)
- Discussed something about our algorithm related to distribute orders. 


##### Todo 

- Keep working on communicate with server.
- Start Integration and design algorithm
- Make sure our minimum useable product is online. 





#### Week 5

10/26/2018

##### Goals

Start working on communication with server

##### What I have done

- Finalized the API standard communication with server
- Use `JsonRequest` that allow client communicate with server
- Request Token from server and use it as authentication. 
- Small update of `PostActivity`
- send request to server, but not finished. (need to show sth if user want to find trip)
- Continue to the translation to integration phase with Yida

##### Todo 

- Working on communicate with server.
- Able to refresh Token in a given period(otherwise it will expire and require login again)
- Make `register account` into the client



#### Week 4

10/18/2018

##### Goals

Finished Client functionalities development

##### What I have done

- A route and eta will should when destination/original location given
- Made UI of `MapsActivity` more reachable, with directly entering the from/to, and a next button will direct user to post/share activity 
- Merged the Activity of post/share to one and user can differentiate them by using switch button there
- Login page enhanced. With the interface of communicating with Server.
- Tried send/receive packets from server, but not finished yet. Make many tests on `LoginActivity` to make it work. 
- Continued to discussed the API specification with Yida.

##### Todo 

- Continue to working on network protocol implementation (send/receive query by JSON) 
- Using Token given by server and communities with it. 
- Ready to move to the integration parse.





#### Week 3

10/12/2018

##### Goals

Continue Client functionalities development

##### What I have done

- Autocomplete is now able to interact with ride/post function
- Post/Share has added more functionalities and is ready to communicate with server
- Applied changes of MapsActivity to make it more reachable(e.g, there was a overlap between the search bar and my location buttom)
- Settings UI added to be used in myProfile
- Test with Google Map Console that make sure Place SDK goes well. 
- Continued to discussed the API specification with Yida.

##### Todo 

- Network protocol implementation (send/receive query by JSON) 

- analysis users input and transfer to JSON

- continue work on UI to make it more reachable and good-looking






#### Week 2

10/05/2018

##### Goals

Continue Client functionalities development

##### What I have done

- Autocomplete has added to the client
- Post/Share Trip UI has added to the client
- Change the structure of `MapsActivity` to make it more stable
- Made some changes in dependencies to make it consistent
- Discussed the API specification with Yida to be readied as interface in the future

##### Todo 

- Finish All UI development

- Show route and ETA given address

- API interface that communicate with server 




#### Week 1        

9/28/2018 

##### Goals

Setup Environment and Create project

##### What I have done

- Setup and deploy the environment on my workbench

- Created and configurated the Project with all background codes

- Login UI to the project

- Map interaction UI added to the project with correct setup of permission

- Basic animation of the map

- Menu UI with the function designed in the SRS

- API stuff with Google Map

   



##### Todo

- Implement more functionalities to project
- UI of address auto complete, post/find trips
- Search address, and show the route of given addresses (and ETA)
- AUTH of Login page

