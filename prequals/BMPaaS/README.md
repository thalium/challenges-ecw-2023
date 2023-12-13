# BMPaaS

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | easy       | crypto   | tcp/31337| tcp/1337 |

## Description
Just a baby encryption scheme for you. It features `os.urandom`, therefore it is perfectly safe.

## Setup
```bash
docker build ./deploy -t bmpaas
```

## Run
```bash
docker container run -p 1337:31337 bmpaas
```