# maze

## Information
| author                          | difficulty | category | in. port | exposed  |
|---------------------------------|------------|----------|----------|----------|
| [Seela](https://seela.com/)     | medium     | web      | tcp/80   | tcp/1337 |


## Description

Calling upon an AI is not always the right solution, especially when it is still in development! 
And it seems that this one didn't quite grasp when you asked for help in understanding the labyrinth of life. 
It turned it into a riddle to better explain it to you! "Remember that `every mistake` is beneficial!" it exclaimed to you.

## Build

```bash
docker build ./deploy -t maze
```

## Run

```bash
docker run -d -p 1337:80 maze
```