FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3-pip python3-venv libglib2.0-0 libgl1-mesa-dev

WORKDIR /app

COPY . .

RUN python3 -m venv venv && \
    . venv/bin/activate && pip3 install -r requirements.txt

CMD ["./venv/bin/python3", "-m", "flask", "run", "--host=0.0.0.0"]
