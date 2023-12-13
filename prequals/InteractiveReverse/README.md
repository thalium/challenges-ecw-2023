# InteractiveReverse

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | hard       | reverse  | tcp/42080| tcp/1337 |

## Description
You have laid hands upon a novel kind of chip that runs an unknown architecture. You cannot reverse engineer the chip itself, but you are able to converse with it, and are tasked with finding the secret hidden in an associated sample program.

## Setup
```bash
docker build ./deploy -t interactive_reverse
```

## Run
```bash
docker container run -p 1337:42080 interactive_reverse
```