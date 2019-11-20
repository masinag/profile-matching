FROM python:3
ADD main.py matcher.py parser.py /
COPY tapoi_models /tapoi_models/
RUN pip install requests
ENTRYPOINT [ "python3", "./main.py" ]