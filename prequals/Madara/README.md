# Madara

## Information
| author                          | difficulty | category | in. port | exposed  |
|---------------------------------|------------|----------|----------|----------|
| [Yogosha](https://yogosha.com/) | medium     | web      | tcp/80   | tcp/1337 |

## Description
This is an easy task for such a good hacker, go get me the flag.

## Setup
```bash
docker build ./deploy -t madara
```

## Run
```bash
docker container run -p 1337:80 madara
```