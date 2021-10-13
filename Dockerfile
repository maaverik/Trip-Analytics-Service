FROM continuumio/miniconda3

COPY "requirements.txt" /
RUN ["pip", "install", "-r", "requirements.txt"]

COPY /src /src
RUN ["python", "-m", "src.prepare_data"]

COPY /tests /tests
RUN ["python", "-m", "pytest", "-v", "tests"]

EXPOSE 8000
ENTRYPOINT ["python", "-m", "src.services"]
