# BitWallet

A python module that provides a wallet that can do P&L

## Installation

Quick install/upgrade with `pip install bitwallet`

## Running

You can get your balances from any number of exchanges by doing:
`bitwallet balances <your name>`. You should have a `<your name>.yaml` file
with the following format:

```
-   name: <exchange name - should be a ccxt module>
    key: <key>
    secret: <secret>
    uid: <uid for exchanges that need it>
```

All the [ccxt exchanges](https://github.com/ccxt/ccxt/tree/master/python/ccxt)
are supported.

`bitwallet` creates temporary files to avoid hitting your exchanges at every
call. The temporary files are called `<your name>_balances.pkl`. Remove them
every time you make some transactions in order to reload them. Unless you do so
the only thing updated between subsequent calls is the coin-USD exchange rate.

## Notes

To run tests: `python setup.py test`

To release, increase version number in setup.py and then `rm -rf dist`, `python
setup.py sdist`, `twine upload dist/*`. Clean install with updates: `pip install
 --no-cache-dir -U bitwallet`
