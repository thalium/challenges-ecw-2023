# Snitch

## Information
| author                          | difficulty | category      |
|---------------------------------|------------|---------------|
| [Seela](https://seela.com/)     | medium     | Web3          |

## Description

ALICE has become more human than we predicted. Money has become her number one priority and plans to become the richest individual on the planet. The easiest way she found to acheive her goal is to steal it from human beings. With the growing interest for cryptocurrencies, the AI deployed a smart contract on the blockchain to snitch funds from her victims.

Recover everything that has been stolen and send it to the relevant authorities at address : `0xCaffE305b3Cc9A39028393D3F338f2a70966Cb85`

## Setup
```bash
docker build ./deploy -t snitch
```

## Run
```bash
docker container run -p 1337:80 snitch
```