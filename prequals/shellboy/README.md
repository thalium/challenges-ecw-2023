# shellboy

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | medium     | pwn      | tcp/1337 | tcp/1337 |

## Description
While packing to go to the ECW finals, one of your friends found an old Gameboy cartridge in a box, along with a booklet. Curious, he ran it on his console. Unfortunately, he never managed to win. He knows you're much better than he is. That's why he challenged you to win the game by displaying the victory flag.

In his generosity, he gives you the dump of the gameboy cartridge, as well as the contents of the booklet (apparently the source code). He also provides you with an emulator (Wasmboy) to try out the game. Good luck!

## Setup
```bash
docker build ./deploy -t shellboy
```

## Run
```bash
docker container run -p 1337:5000 shellboy
```