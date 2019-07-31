import socket
import sys
import pickle
import numpy as np
import struct ## new
import zlib
import signal 
import numpy as np

import time


def ServerSocket(HOST="localhost", PORT=0000):
    # HOST='10.68.74.44'
    # PORT=8492
    signal.signal(signal.SIGINT, signal.SIG_DFL)


    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST,PORT))
    print('Socket bind complete')

    cnt = 0
    while True:

        cnt += 1

        s.listen(10)
        print('Socket now listening')

        conn,addr=s.accept()

        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        # while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imwrite("server-" + str(cnt) + ".jpg", frame)


        res = np.array([[10,10,20,20],[10,10,20,20.0]])
        data = res.tobytes()
        # data = bytes(res)
        # data = res.tobytes
        # array_data_type = as_array.dtype.name
        # print(array_data_type)
        # array_shape = as_array.shape
        # print(array_shape)
        time.sleep(10)

        conn.sendall(struct.pack(">L", len(data)) + data)


        conn.close()



    # cv2.imshow('ImageWindow',frame)
    # cv2.waitKey(0)
