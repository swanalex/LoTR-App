import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")

while True:
    message = socket.recv_string()
    if message == "generate_numbers":
        num1 = random.randint(1, 933)
        page_num = random.randint(1, 3)
        num2 = random.randint(1, 1000)
        if page_num == 3:
            num2 = random.randint(1, 384)
        socket.send_json({"num1": num1, "page_num": page_num, "num2": num2})
    else:
        socket.send_string("Invalid request")
