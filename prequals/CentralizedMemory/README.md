# CentralizedMemory

## Information
| author                       | difficulty | category | in. port | exposed  |
|------------------------------|------------|----------|----------|----------|
| [Thales](https://thalium.re) | hard       | pwn      | tcp/1337 | tcp/1337 |

## Description
The GreenShard group came up with a revolutionary idea to reduce the maintenance costs of its IT equipment: dematerialize RAM! The company bought its employees PCs with as little RAM as possible and installed a client to exchange data with the centralized RAM server.

Obviously, the company jealously guards its secrets and divulges nothing about the communication protocol between the clients and the RAM server. Nevertheless, a recent leak has enabled you to get your hands on the RAM server binary and the libc used. Prove that this company is on the wrong track by retrieving the flag from the server.

For the record, we know for a fact that this company uses ncat for its other services.

## Setup
```bash
docker build ./deploy -t centralized_memory
```

## Run
```bash
docker container run -p 1337:1337 centralized_memory
```