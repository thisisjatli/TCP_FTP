import socket
import os

HOST = "127.0.0.1"  # localhost
PORT = 8000         # random port
CHUNKSIZE = 1024    # size of one chunk

def sendToClient(conn, filename="downloadTestFile.pptx"):
    clientCode = conn.recv(CHUNKSIZE).decode()  # make sure the client is ready
    if int(clientCode) == 0:
        print("Start downloading...")
        with open(filename, 'rb') as fr:
            data = fr.read(CHUNKSIZE)   # read and send file in chunks
            while data:
                conn.send(data)
                data = fr.read(CHUNKSIZE)
            fr.close()
        
        conn.send(b"EOF")   # the end of the file
        print("Finish downloading.")
    
    else:
        print("Some exceptions happen")
    return

def clientUpload(conn, filename="newUploadTestFile.pptx"):
    with open(filename, 'wb') as fw:
        data = conn.recv(CHUNKSIZE)
        while data and data != b"EOF":
            # receive data from client and save to local disk
            fw.write(data)
            data = conn.recv(CHUNKSIZE)

            # need a condition to stop loop
            # if (EOF): break
        fw.close()

    print("Finish uploading.")
    return

def requestHandling(conn, msg):
    msgArr = msg.split()
    if msgArr[0] == "get":
        if len(msgArr) != 2:
            serverResponse = "1:Get command format incorrect."
            conn.send(serverResponse.encode())
        elif msgArr[1] not in os.listdir():
            serverResponse = "1:The file does not exist."
            conn.send(serverResponse.encode())
        else:
            serverResponse = "0:Request accepted. Start downloading."
            conn.send(serverResponse.encode())
            sendToClient(conn, filename=msgArr[1])

    elif msgArr[0] == "upload":
        if len(msgArr) != 2:
            serverResponse = "1:Upload command format incorrect."
            conn.send(serverResponse.encode())
        else:
            serverResponse = "0:Request accepted. Start uploading."
            conn.send(serverResponse.encode())
            clientUpload(conn)

    else:
        serverResponse = "2:This request is invalid, please input again."
        conn.send(serverResponse.encode())

if __name__ == "__main__":
    # create socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))

    # server listening
    serversocket.listen(5)
    print("Server listening...")

    # connection with client
    # conn: socket object
    # addr: client ip
    conn, addr = serversocket.accept()
    print(f"Client {addr[0]}:{addr[1]} connected.")

    # sending welcome message to client
    conn.send(f"Greetings from the server.".encode())

    while True:
        clientMsg = conn.recv(CHUNKSIZE).decode()
        print("Client says", clientMsg)

        if clientMsg == "quit":
            conn.close()
            print("A client has left.")
            break

        requestHandling(conn, clientMsg)

