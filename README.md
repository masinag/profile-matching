# profile-matching

API which allows to evaluate the similarity of a user profile against a set of existing ones.

A profile is represented by a dictionary where each topic is associated with the number of times the user has discussed about that topic. Topics are urls of Wikipedia categories.

## The matching

There are two algorithms to find the most similar profile. Let `cmp_profiles` be the set of existing profiles, and let `profile` be the profile of which we want to find the most similar one.

In both algorithms each `cmp_profile` is assigned a `match_value` representing the similarity with `profile`, and the one with the highest value is said the most similar. Both are based on the percentage of discussion of each topic on the total of discussions.

In the `algorithm1`, when confronting two profiles, each topic discussed by both profiles contributes to the `match_value` with a score proportional to the similarity of the discussion percentages of the topic in the two profiles. This value is multiplied by the lowest of the two percentages, so that if the two percentages are very similar but they are very low, this does not contribute much to the `match_value`.

The `algorithm2`, when confronting two profiles, builds a ranking of topics for each profile, where the score is represented by the percentage with which the topic has been discussed. Topics with a similar score belong to the same position in the ranking. The `match_value` of two profiles is computed by confronting the similarity of the positions of each topic discussed by both in the rankings of the two profiles. This value is multiplied by the lowest of the two percentages, so that if the two positions are very similar but the corresponding percentages are low, this does not contribute much to the `match_value`.

## Project structure

### Modules and packages

* `main.py` is the runnable script which takes the path to the `profile`'s json-file and the path to the directory containing the json-files of the `cmp_profiles`. It calls the API functions to do the matching and prints their result. It offers also the possibility to translate the topics from foreign languages to English when possible by setting a flag.
* `parser.py` contains functions to clean-up topic names for a profile and translate them if requested. Topic names are translated using the Wikipedia API.
* `matcher.py` contains functions to do the comparison between the `profile` and the `cmp_profiles` and to get the most similar one. It uses functions defined in the `matching` package.
* package `matching`:
  * `matcher1.py`: contains the implementation of the `algorithm1`.
  * `matcher2.py`: contains the implementation of the `algorithm2`.

### Other resources

* Directory `tapoi_models/`: is the default directory in which the profiles with which doing the comparison are stored.
  * `translated/`: contains a version of default profiles where topics not in English for which the translation is available are translated to English.
* Directory `sample_profiles/`: contains some examples of profiles for which the most similar can be found.

## Installation and run

To run the project simply clone the repository and run the main script by running the command

```bash
python3 main.py path_to_the_json_profile
```

For further options run

```bash
python3 main.py --help
```

Example:

```bash
python3 main.py sample_profiles/roger_like.json --cmp_profiles_dir tapoi_models/translated/
```
will compare the profile `sample_profiles/roger_like.json` to all profiles in directory `tapoi_models/translated/`

## Dockerize

There is also the possibility to dockerize the project by running the command

```bash
docker build -t profile-matching
```

Then you can run it with the command

```bash
docker run profile-matching profile path_to_the_json_profile [optional_arguments]
```

If you use docker, to add a file or a directory to the docker image, modify the Dockerfile by adding another line like

```docker
COPY path_to_your_file_or_dir path_where_to_copy_it_on_docker_image
```

where the second parameter always starts with a `/`

For more infos see [Docker documentations](https://docs.docker.com/engine/reference/builder/)
