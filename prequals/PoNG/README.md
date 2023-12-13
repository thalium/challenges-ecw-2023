# PoNG

## Information
| author                              | difficulty | category | in. port | exposed  |
|-------------------------------------|------------|----------|----------|----------|
| [Diateam](https://www.diateam.net/) | medium     | pwn      | tcp/80   | tcp/1337 |

## Description
You retrieved the source code of the AI's image recognition system. Exploit it and steal the secrets.

## Setup
```bash
docker build ./deploy -t pong
```

## Run
```bash
docker container run -p 1337:80 pong
```