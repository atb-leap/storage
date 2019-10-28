FROM python:onbuild
COPY requirements.txt .
ENTRYPOINT ["pytest"]
