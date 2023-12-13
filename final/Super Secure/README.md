# Super Secure

## Information
| author                          | difficulty | category | in. port | exposed  |
|---------------------------------|------------|----------|----------|----------|
| [Yogosha](https://yogosha.com/) | easy       | reverse  | tcp/1234 | tcp/1337 |

## Description
My program is super secure, can you crack the licence?

## Setup
```bash
docker build ./deploy -t super_secure
```

## Run
```bash
docker container run -p 1337:1234 super_secure
```