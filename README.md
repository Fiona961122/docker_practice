# Docker Assignment Solutions

To build the image:  
`docker build -t ner .`  
To run the docker container:  
`docker run --rm --detach --publish 5000:5000 ner`  
To access the ner website point your browser at http://0.0.0.0:5000/.  
To access the entities point your browser at http://0.0.0.0:5000/entities  
