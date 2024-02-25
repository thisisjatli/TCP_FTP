# TCP_FTP

## Set up
* download zip file project1.zip
* unzip the zip file
* must include files for downloading and uploading in the directory

## Run
* open two terminals in project1/ directory, one for server and the other one for client
* server side:
```
python server.py
```
* client side:
```
python client.py 8000
```

## Requests
### get file
Client can get a file from the server by sending request
```
get [filename]
```
* Server's responses
    * Get command format incorrect. - request format incorrect
    * The file does not exist. - the file client requests does not exist

### upload file
Client can upload a file to the server by sending request
```
upload [filename]
```
* Server's responses
    * Upload command format incorrect. - request format incorrect

* Local error handling
    * Please enter an existing file - the file client attempts to upload does not exist
