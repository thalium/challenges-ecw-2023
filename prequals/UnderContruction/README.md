# UnderConstruction

## Information
| author                          | difficulty | category | in. port | exposed  |
|---------------------------------|------------|----------|----------|----------|
| [Yogosha](https://yogosha.com/) | medium     | web      | tcp/8080 | tcp/1337 |

## Description
What is better than hacking a website when it's still under construction!

## Setup
```bash
docker build ./deploy -t under_construction
```

## Run
```bash
docker container run -p 1337:8080 under_construction
```