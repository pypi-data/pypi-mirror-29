# btcsignature
btcsignature is a command line tool for signing bitcoin transaction data offline easily and securely.

# how to use

For now only 2 simple command line tools.

1. Read the contents of a transaction hex with command:

$ read-tx


* you will be prompted for a transaction hex and will receive a json output
* must be online
* always a good idea to read contents before signing something!


2. Sign a Bitcoin Trnasaction offline with your private key. Command:

$ sign-offline 

* must be offline or script will not run
* will be prompted for your private key and a transaction hex
* will succeed and return signed transaction only if private key matches address of all transaction inputs





