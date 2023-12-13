FROM debian:stable-slim

RUN apt update -y && \
    apt install git curl python3 python3-pip supervisor -y && \
    curl -L https://foundry.paradigm.xyz | bash && \
    bash -c "source /root/.bashrc && foundryup" && \
    python3 -m pip install eth_account flask requests web3 gunicorn --break-system-packages && \
    echo 'alias ll="ls -lah"' >> /root/.bashrc && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY ./src/supervisor/supervisord.conf /etc/supervisor/conf.d/
COPY ./src/blockchain/ /blockchain/
COPY ./src/app/ /app/

RUN cd /blockchain && \
    /root/.foundry/bin/forge test

EXPOSE 80

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]
