all: clean run

clean:
	@rm -rf __pycache__
	@rm -f log

run:
	python3 main.py tapoi_models/roger.json