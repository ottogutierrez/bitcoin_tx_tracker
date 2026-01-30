# btc_tracker - Track your BTC stack

This cli tool helps you keep track of your Bitcoin buys, adding information like average cost, transaction details, etc.

## Current status

Right now, this is a simple CLI that interacts with the Blockstream BTC API to download transactions, and extract information. But in the future, I plan to make it more full featured and possibly add tax reports and DCA tracking and combining.

## Installation & Usage

To run the cli, clone this repo and run
`python -m btc_tracker.py`

## Roadmap

In the future, I plan to add support for SQlite3 to persist transactions, add support for the Lightning transactions (DCA) and combining when consolidation happens (and calculation of average cost, etc.)
