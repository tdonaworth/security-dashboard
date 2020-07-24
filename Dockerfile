# Dockerfile
FROM python:3.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Set FLASK variable 
ENV FLASK_APP secdash.py
ENV FLASK_RUN_PORT 5050
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5050

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
# Switch to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

COPY . .

CMD ["flask", "run"]