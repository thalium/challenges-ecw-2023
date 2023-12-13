FROM pwn.red/jail
COPY --from=ubuntu@sha256:b060fffe8e1561c9c3e6dea6db487b900100fc26830b9ea2ec966c151ab4c020 / /srv
COPY watermelons /srv/app/run
COPY watermelon.txt /srv/app/
COPY flag.txt /srv/app/

RUN chmod +x /srv/app/run
