# Jigsaw2

## Information
| author                     | difficulty | category | in. port | exposed  |
|----------------------------|------------|----------|----------|----------|
| [Seela](https://seela.io/) | hard       | misc     | tcp/1337 | tcp/1337 |

## Description
To get the flags, you will have to answer to all questions in a limited time. Don't forget to check the leaderboard.

## Setup
```bash
docker build ./deploy -t jigsaw2
```

## Run
```bash
docker container run -p 1337:1337 jigsaw2
```