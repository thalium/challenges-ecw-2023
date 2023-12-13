FROM node

RUN adduser ctf

COPY ./emulator /home/ctf

RUN chown -R root:ctf /home/ctf
RUN chmod -R 550 /home/ctf

WORKDIR /home/ctf/emulator

RUN npm install

EXPOSE 1337

CMD [ "npm", "start" ]