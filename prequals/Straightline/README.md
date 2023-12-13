# Straightline

## Information
| author                             | difficulty | category | in. port | exposed  |
|------------------------------------|------------|----------|----------|----------|
| [Amossys](https://www.amossys.fr/) | hard       | crypto   | tcp/8000 | tcp/1337 |

## Description
You got access to a web site created by ALICE, the artificial intelligence. Your goal is to find an administrator access in order to obtain information to stop ALICE. To your disposal is the source of the cryptographic algorithm used for the authenfication.

## Setup
```bash
docker build ./deploy -t straightline
```

## Run
```bash
docker container run -p 1337:8000 straightline
```