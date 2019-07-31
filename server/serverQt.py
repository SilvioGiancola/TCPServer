import sys
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
# # from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from PyQt5.QtGui import QPixmap, QImage                                

import pickle
import struct
import argparse

import sys, signal

SIZEOF_UINT32 = 4

class ServerQt(QTcpServer):

    def __init__(self, parent=None, HOST="localhost", PORT=0000):
        super(ServerQt, self).__init__(parent)
        self.parent = parent
        print("HOST", HOST)
        print("PORT", PORT)        
        self.listen(QHostAddress(HOST), PORT)
        self.newConnection.connect(self.addConnection)
        self.connections = []
        self.reply = None
        self.cnt = 0

    def removeDisconnectedConnection(self):
        self.connections = [s for s in self.connections if s.state() > QAbstractSocket.UnconnectedState]
        # print(len(self.connections))

    def addConnection(self):
        clientConnection = self.nextPendingConnection()
        clientConnection.nextBlockSize = 0
        clientConnection.readyRead.connect(self.receiveMessage)
        clientConnection.disconnected.connect(self.removeConnection)
        clientConnection.error.connect(self.socketError)
        self.connections.append(clientConnection)

    def sendMessage(self, text, socket):
        # for s in self.connections:
        self.reply = QByteArray()
        stream = QDataStream(self.reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_9)
        stream.writeUInt32(0)
        stream.writeUInt32(0) # header for QString
        stream.writeQString(f"{text}")
        stream.device().seek(0)
        stream.writeUInt32(self.reply.size() - SIZEOF_UINT32)
        
        socket.write(self.reply)
        self.reply = None
        print(f"sending '{text}' to {socket.socketDescriptor()}")
        socket.waitForBytesWritten(1000)


    def receiveMessage(self):   
        print("received smtg")     

        for s in self.connections:


            if s.bytesAvailable() > 0 :

                stream = QDataStream(s)
                stream.setVersion(QDataStream.Qt_4_9)

                if s.nextBlockSize == 0:
                    if s.bytesAvailable() < SIZEOF_UINT32:
                        return
                    size = stream.readUInt32()
                    print("size", size)
                    s.nextBlockSize = size
                if s.bytesAvailable() < s.nextBlockSize:
                    return


                header = stream.readUInt32()

                print("header", header)

                if header == 0: # QString
                    textFromClient = stream.readQString()
                    print(f"received '{textFromClient}' from {s}")

                    answer = textFromClient + " Back at you!"

                    if "CLOSE" in textFromClient:
                        self.parent.quit()

                if header == 1: # QImage
                    img_bytes = stream.readBytes()
                    img = QImage()
                    img.loadFromData(img_bytes)
                    img.save("serverQt.jpg")
                    print(f"received an image from {s}")

                    answer = "image saved in the server on serverQt.jpg"

                s.nextBlockSize = 0

            # BACK AT CLIENT
                self.sendMessage(answer, s)
                s.nextBlockSize = 0


    def removeConnection(self):
        pass

    def socketError(self):
        pass

