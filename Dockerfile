FROM ubuntu AS base

RUN apt-get update && \
    apt-get install -y python3-pip python3-venv libglib2.0-0 libgl1-mesa-dev

WORKDIR /app

COPY . .

RUN python3 -m venv venv && \
    . venv/bin/activate && pip3 install -r requirements.txt

EXPOSE 5000

FROM gcr.io/distroless/python3 AS final

COPY --from=base /app /

ENTRYPOINT [ "python3" , "app.py" ] 
