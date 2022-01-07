# austin

### *A chatbot that helps you grasp numeric relationships and concepts with conversational ease.*


## How-Tos
### Use existing container
How to launch a docker container with RASA X and the necessary packages in it. (Port 5002 is for RASA X, 5005 is for RASA Core, 5055 is for action server and port 80 for built-in web interface)

Windows:    docker run -d -p 5005:5005 -p 5002:5002 -p 5055:5055 -p 80:80 -p 8888:8888 --name austin -e GRANT_SUDO=yes --user root -e JUPYTER_ENABLE_LAB=yes -v %cd%:/home/jovyan julianweng/austin

Linux/Mac? (untested with mac):  docker run -d -p 5005:5005 -p 5002:5002 -p 5055:5055 -p 80:80 -p 8888:8888 --name austin -e GRANT_SUDO=yes --user root -e JUPYTER_ENABLE_LAB=yes -v $PWD:/home/jovyan julianweng/austin

Run various containers commands (you only need the first three to talk with it and train it)

    docker exec -it austin rasa train --domain ./domain # train RASA model
    docker exec -it austin rasa run actions # run action server
    docker exec -it austin rasa x --domain ./domain # run RASA X
    docker exec -it austin rasa run --enable-api --cors "*" # run RASA core with pretrained model
    docker exec -it austin python -m http.server 80 -d ./web

All the files in this folder will be mounted to the container, and be used by the RASA X.

### EndPoints
#### credentials.yml
For RASA X to talk to RASA Core

    rasa:
        url: "http://localhost:5002/api"
        # url: "http://austinrasa.ngrok.io/api"

#### endpoints.yml
For RASA Core to talk to Action Server

    action_endpoint:
        url: "http://localhost:5055/webhook"
        # url: "https://austinaction.ngrok.io/webhook"

#### constants.js
For RABuilt-in Web Widget to talk to RASA Core and Action Server

    const rasa_server_url = "https://austincore.ngrok.io";
    //const rasa_server_url = "http://localhost:5005";

    const rasa_action_url = "https://austinaction.ngrok.io";
    // const rasa_action_url = "http://localhost:5055";
### Expose RASA online
Run this on host machine.
    ngrok start --all --config=ngrok.yml

## Directories
### domain
### data
### _actions_
Contains all of the custom python code for the quiz.

### Other Directories
You usually don't have to change these directories.
#### bots
Any bot not supported by Rasa's endpoints.
#### web
This contains the static files for the built-in web chatting application.
#### more_data
This is where the unused traning data is stored.
#### models
It's where the models are stored when training is done.
