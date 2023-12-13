# The Calculator in Shadow

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | hard       | pwn      | tcp/5000 | tcp/1337 |

## Description
ALICE has a secret: it is not really good at mental calculations. However, fret not, since ALICE solved the issue by emulating a RISCV 64-bit processor, and running a custom calculator on top of it.

We think that we may gain some way to fight ALICE by exploiting its calculator, so we secured an access to it! We also got a leak of the source, you will therefore find it attached. Hey, aren't we efficient? Now's your turn to act! However it seems ALICE doesn't emulate a standard RISCV 64-bit processor, but added an obscure thing to it. There are, consequently, custom instuctions in the calculator code. Well, now that seems very shady...

## Setup
```bash
docker build ./deploy -t the_calculator_in_shadow
```

## Run
```bash
docker container run -p 1337:5000 the_calculator_in_shadow
```