# Fireburn

## Information
| author                     | difficulty | category | in. port | exposed  |
|----------------------------|------------|----------|----------|----------|
| [Seela](https://seela.io/) | hard       | web      | tcp/80   | tcp/1337 |

## Description
Yet another artificial intelligence is released, but its answers are limited, so you have to ask it the right question. Your mission is to obtain the flag, or rather to extort it, because it won't listen. For this challenge, automated scanners are not useful.

## Setup
```bash
docker build ./deploy -t fireburn
```

## Run
```bash
docker container run -p 1337:80 fireburn
```