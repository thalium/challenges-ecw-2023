# watermelons

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | easy       | pwn      | tcp/5000 | tcp/1337 |

## Description
You stumble across a peculiar-looking shop... Get the flag in `flag.txt`.

## Setup
```bash
docker build ./deploy -t watermelons
```

## Run
```bash
docker container run --privileged=true -p 1337:5000 watermelons
```