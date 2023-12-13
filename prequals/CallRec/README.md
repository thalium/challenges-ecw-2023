# CallRec

## Information
| author                       | difficulty | category |
|------------------------------|------------|----------|
| [Thales](https://thalium.re) | medium     | forensics|

## Description
A mobile phone has been discovered during an investigation. Authorities have extracted a dump from the phone, but crucial information is missing.

Your mission is to retrieve the following information:
- The `weight` (in grams, rounded to the nearest unit) of the phone.
- The `serial number` (SNR) of the phone.
- The `time` (hh:mm:ss) of the last call made to the number `023546789`.

The flag is in the following format: `ECW{md5(weight-serialnumber-calltime)}`.

For example, if:
- weight = `92g`
- serial number = `471636`
- calltime = `22h30 and 42 seconds`

the flag will be constructed as follows: `md5(92-471636-22:30:42)`, which gives the flag `ECW{59da29c226c05915b078f6455b2c6a42}`.