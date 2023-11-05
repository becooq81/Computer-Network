# Computer-Network

This is a simple socket programming project in Python. 

1. Producer connects to server and relays any input message by the user.
2. Each character of the message is considered an event.
3. Server stores events in a queue.
4. Customer takes an event from the queue every one second and 'processes' it.
