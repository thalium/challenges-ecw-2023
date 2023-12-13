# CryptoFlow

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | hard       | crypto   | tcp/31337| tcp/1337 |

## Description
You have misconfigured your IA who took the control of your computer. It's now mocking you using its favorite method: an unsolvable challenge. Find the password to take back the control of your system.

## Setup
```bash
docker build ./deploy -t cryptoflow
```

## Run
```bash
docker container run -p 1337:31337 cryptoflow
```