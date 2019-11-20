# profile-matching
API which allows to evaluate the similarity of a user profile against a set of existing ones

## Project structure
The project consists of 3 main modules:
* `main.py` is the runnable script which takes the path to the profile json-file and the path to the
            dir containing the json-files of the profiles to compare the profile to. It allows also the
            possibility to translate the topics in foreign languages to english when possible by 
            setting a flag.
* `parser.py` contains functions to read the json files to get a python dictionary with the topic names
            cleaned-up and translated if requested. Topic names are translated usign the Wikipedia API.
* `matcher.py` contains the functions to do the match between the given profile and the files to compare
            and to get the most similar profile.

It contains a directory `/tapoi_models/` which is the default directory in which the profiles with which
doing the comparison are stored.

## Installation and run
To run the project simply clone the repository and run the main script by running the command 
```python3 main.py <path_to_the_json_profile>```


Type ```python3 main.py --help``` for further options.

