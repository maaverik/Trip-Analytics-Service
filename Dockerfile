FROM continuumio/miniconda3

# to run as non-root
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY "requirements.txt" .
RUN ["pip", "install", "-r", "requirements.txt"]

COPY "config.json" .
COPY /src ./src
RUN ["python", "-m", "src.prepare_data"]

COPY /tests ./tests
RUN ["python", "-m", "pytest", "-v", "tests", "--cov=src"]

EXPOSE 8000
ENTRYPOINT ["python", "-m", "src.services"]
