---
author: chainsquad
title: "[pybitshares.com] New python library for BitShares: pybitshares - brother of pysteem"
category: chainsquad
tags:
 - bitshares
 - python
 - blockchain
percent_steem_dollars: 0
---

[![](https://bitshares.org/images/transparent_b.png)](http://pybitshares.com)

We are pleased to announce our first public release of [pybitshares](http://pybitshares.com) in version 0.1.0! This library has been built following the success of [pysteem](http://pysteem.com).

## What is BitShares

BitShares is a **blockchain-based autonomous company** (i.e. a DAC) that offers decentralized exchanging as well as sophisticated financial instruments as *products*.

It is based on *Graphene* (tm), a blockchain technology stack (i.e. software) that allows for fast transactions and ascalable blockchain solution. In case of BitShares, it comes with decentralized trading of assets as well as customized on-chain smart contracts.

## What is pybitshares

The purpose of *pybitshares* is to simplify development of products and services that use the BitShares blockchain. It comes with

* it's own (bip32-encrypted) wallet
* RPC interface for the Blockchain backend
* JSON-based blockchain objects (accounts, blocks, prices, markets, etc)
* a simple to use yet powerful API
* transaction construction and signing
* push notification API
* *and more*

## Quickstart/Demo

Transfers:

    from bitshares import BitShares
    bitshares = BitShares()
    bitshares.transfer("<to>", "<amount>", "<asset>", "[<memo>]", account="<from>")

Monitoring the Blockchain:

    from bitshares.blockchain import Blockchain
    blockchain = Blockchain()
    for op in Blockchain.ops():
        print(op)

Obtaining a Block:

    from bitshares.block import Block
    print(Block(1))

Obtaining an Account:

    from bitshares.account import Account
    account = Account("init0")
    print(account.balances)
    print(account.openorders)
    for h in account.history():
        print(h)

Dealing with the markets:

    from bitshares.market import Market
    market = Market("USD:BTS")
    print(market.ticker())
    print(market.sell(300, 100)  # sell 100 USD for 300 BTS/USD

Dealing with call positions/collateral:

    from bitshares.dex import Dex
    dex = Dex()
    dex.adjust_collateral_ratio("SILVER", 3.5)

## Uptick

Keep in mind that this library is tightly connected to [uptick](http://uptick.rocks), which is a command line tool similar to `piston`. Even though the library can be used without uptick, it still makes your live easier when it comes to dealing with your wallet. There will be a separate announcement for uptick shortly.

---

## ChainSquad Witness

If you like the services offered by [ChainSquad GmbH](http://chainsquad.com), please consider [approving our new witness](https://steemit.com/steem/@chainsquad/chainsquad-com-for-witness): `chainsquad.com`

Thanks you!
