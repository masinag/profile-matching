all: clean run

clean:
	@find . -name "__pycache__" -print0 | xargs -0 rm -rf
	@rm -f log

run:
	python3 main.py sample_profiles/roger_like.json

build-docker:
	sudo docker build -t profile-matching .

run-docker:
	sudo docker run profile-matching sample_profiles/roger_like.json