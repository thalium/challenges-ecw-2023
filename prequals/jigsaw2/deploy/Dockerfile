FROM python:3.8-slim-buster

WORKDIR /jigsaw2
# Install Supervisor
RUN apt-get update && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/log/supervisor

COPY files/server/ .

RUN pip install --no-cache-dir virtualenv && \
    virtualenv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Create virtual environment
RUN python -m venv /jigsaw2/venv

RUN useradd -s /bin/bash -m John_Kramer && \
    chmod a-w /jigsaw2/* -R && \
    chmod 777 /jigsaw2/jigsaw.log && \
    chmod a+wx /jigsaw2



# Add Supervisor configuration file
COPY files/supervisor/supervisord.conf /etc/supervisor/


RUN echo "ECW{1NC0RR3CT_S4N1T1Z4T10N}" > /jigsaw2/flag.txt

ENV LOG_LEVEL=CRITICAL

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]


