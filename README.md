# LoTR-App

A Flask-based web application that allows users to interact with ‘The One API’ (https://the-one-api.dev/) to retrieve information about characters and quotes from the world of J.R.R. Tolkien. This application provides a dynamic and engaging user experience by randomly selecting and displaying character details and quotes. Have fun and enjoy!

# Communication Contract:
A. Data will be programmatically requested from my microservice using the ZeroMQ(ZMQ) communication pipeline. My partner will import the ZMQ module to their app, and then setup a request socket like such:

(ZeroMQ setup)  
context = zmq.Context()  
socket = context.socket(zmq.REQ)  
(Note: this is an example port - my partner can use whatever port number they wish)  
socket.connect("tcp://127.0.0.1:5555")  
  
They will then send a string to my microservice using socket.send_string().  
Example:  
```
socket.send_string("easy")
```
or
```
socket.send_string("medium")
```
or
```
socket.send_string("hard")
```  
  
My microservice will wait for the incoming string message requesting data using sockect.recv_string(), generate the 2 random numbers of the appropriate length, and send back a response message in the form of a JSON object using socket.send_json().  
  
  
B. Data will be programmatically received by my partner's application from my microservice by reading the response JSON object and assigning it to a variable. Example:  
some_variable = socket.recv_json()  
My partner can then parse this received message as they wish and use the data for their needs in their application.  




  ![UML_Diagram](https://github.com/swanalex/LoTR-App/assets/86210924/39ca04e4-9db9-423e-acd0-42d78dfc84c6)
