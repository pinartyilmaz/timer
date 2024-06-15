## About project
This is a very simple timer which have the following features.
1. “set timer” endpoint: /timer

   Receives a JSON object containing hours, minutes, seconds, and a web url. 
  
     Returns a JSON object with the amount of seconds left until the timer expires and an id for querying the timer in the future.
  
     The endpoint should start an internal timer, which calls the defined URL when the timer expires.
  
2. a “get timer” endpoint: /timer/{timer_uuid}
   
      Receives the timer id in the URL, as the resource uuid.
   
      Returns a JSON object with the amount of seconds left until the timer expires. If the timer already expired, returns 0.

The timer uses a background task as dramatiq and caches the timer_id by using redis. 
The challange here is that this application is fully scalable thanks to using background task and caching. 
This project has been completed in 5 hours. 
## Instructions
This application is fully conteinarized. To run the project go to the project's directory and run ***docker compose up***. This will expose the fastapi app im port 8000.
After that, in the browser hit localhost:8000/docs and try the application. 
## What to improve

This application right now doesn't have any tests. 

Instead of pipm it would be a better aoproach to use poetry as dependency manager. As right now, in the Dockerfile everything is installed explicitly.

No logging implemented. Generally lacks the docs.

A nice frontend could be implemented. 




