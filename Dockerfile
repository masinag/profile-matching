FROM python:3
ADD main.py /
COPY matcher.py parser.py matcher.py /
COPY matching/ /matching/
COPY tapoi_models/ /tapoi_models/ 
RUN pip install requests
ENTRYPOINT [ "python3", "./main.py" ]