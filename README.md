# profile-matching
API which allows to evaluate the similarity of a user profile against a set of existing ones

## Project structure
The project consists of 3 main modules:
* `main.py` is the runnable script which takes the path to the profile json-file and the path to the
            dir containing the json-files of the profiles to compare the profile with. It offers also the
            possibility to translate the topics in foreign languages to english when possible by 
            setting a flag.
* `parser.py` contains functions to read the json files to get a python dictionary with the topic names
            cleaned-up and translated if requested. Topic names are translated usign the Wikipedia API.
* `matcher.py` contains the functions to do the match between the given profile and the files to compare 
            it with and to get the most similar profile.

It contains a directory `/tapoi_models/` which is the default directory in which the profiles with which
doing the comparison are stored.

## Installation and run
To run the project simply clone the repository and run the main script by running the command 
```bash
python3 main.py <path_to_the_json_profile>
```

Type 
```bash
python3 main.py --help
``` 
for further options.


## Dockerize
There is also the possibility to dockerize the project by running the command
```bash
docker build -t profile-matching
```
Then you can run it with the command
```bash
docker run profile-matching [command line arguments]
```

If you use docker, to add a file or a directory to the docker image, modify the Dockerfile
by adding another line like 
```docker
COPY <path_to_your_file_or_dir> <path_where_to_copy_it_on_docker_image>
```
where the second parameter always starts with a `/`

For more infos see [Docker's documentations](https://docs.docker.com/engine/reference/builder/)

#TODO: 
! sample profiles
readme
dockerize