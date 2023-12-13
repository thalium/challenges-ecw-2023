FROM python:3.10.12

RUN useradd -d /home/ssti/ -m -s /bin/bash ssti
RUN echo 'ssti:ssti' | chpasswd

WORKDIR /app

COPY src .

RUN chown -R root:ssti .
RUN chmod 750 -R .
RUN chmod 640 flag.txt

USER ssti

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
EXPOSE 8080
