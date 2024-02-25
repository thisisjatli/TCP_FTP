import socket

HOST = "127.0.0.1"  # localhost
PORT = 8000         # random port
CHUNKSIZE = 1024    # size of one chunk

def downloadFile(clientSocket, savefileName="newDownloadTestFile.pptx"):
    clientSocket.send("0".encode())     # tell the server it's ready
    
    with open(savefileName, 'wb') as fw:
        data = clientSocket.recv(CHUNKSIZE)
        while data and data != b"EOF":
            fw.write(data)
            data = clientSocket.recv(CHUNKSIZE)
        fw.close()
    
    print("Done downloading.")
    return

def uploadFile(clientSocket):
    return

def processServerResponse(clientSocket, clientRequest, serverMsg):
    clientRequestArr = clientRequest.split()
    serverCode = int(serverMsg[0])
    print("Server's response:", serverMsg[2:])
    if serverCode > 0:
        return
    # server code is 0, which means request accepted
    elif clientRequestArr[0] == "get":
        downloadFile(clientSocket)

    elif clientRequestArr[0] == "upload":
        uploadFile(clientSocket)


if __name__ == "__main__":
    # create socket for client side
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    welcomeMsg = clientsocket.recv(CHUNKSIZE)
    print(welcomeMsg.decode())

    while True:
        clientMsg = input("Please enter your request: ")
        if clientMsg == "quit":
            clientsocket.send(clientMsg.encode())
            clientsocket.close()
            break

        clientsocket.send(clientMsg.encode())
        serverMsg = clientsocket.recv(CHUNKSIZE).decode()

        # print("Server's response: ", serverMsg)
        processServerResponse(clientsocket, clientMsg, serverMsg)
