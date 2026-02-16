# Introductory Educational Blockchain Simulator with UI

A simple, visual blockchain simulator designed to help learnning how cryptocurrency and blockchain technology works.

---

## Overview

This beginner-friendly blockchain application runs on your local computer. It demonstrates:

- How transactions work between users
- How mining creates new blocks
- How the blockchain maintains security and immutability
- How miners receive rewards for their work

---

## Installation and Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Access the interface at: http://localhost:5000

---

## User Interface Guide

### Dashboard Metrics

The dashboard displays six key metrics:

- **Total Blocks**: Number of blocks in the chain
- **Total Transactions**: All transactions ever processed
- **Pending**: Transactions waiting to be mined
- **Difficulty**: Mining difficulty level (4 = medium)
- **Avg Mine Time**: Average time required to mine a block
- **Chain Valid**: Indicates if the blockchain is secure and unaltered

### Creating a Transaction

Transactions represent the transfer of coins from one user to another.

**Steps:**

1. Enter the sender name (example: Ahmed)
2. Enter the receiver name (example: Imene)
3. Enter the amount (example: 1000)
4. Click "Send Transaction"

**Result:**

- Transaction is created and added to pending transactions
- Transaction is not yet confirmed
- Confirmation requires mining

### Pending Transactions

This section displays all transactions awaiting processing. Transactions become permanent only after they are included in a mined block.

### Mining Blocks

Mining converts pending transactions into permanent blockchain records.

**Manual Mining:**

Click "Mine Block Now" (creates a block for pending transactions that are validated)

**Process:**

1. The system solves a computational puzzle
2. A new block is created containing all pending transactions
3. The miner receives 10 coins as a reward
4. All transactions in the block become permanent

**Automatic Mining:**

Click "Start Auto-Mining" to enable continuous mining

### Blockchain Explorer

The explorer displays all blocks in the chain. Each block shows:

**Block Information:**

- Block number
- Number of transactions
- Transaction details (sender, receiver, amount)
- Proof of work value
- Block hash
- Previous block hash

![Alt text](path/to/Demonstration.png "New transactions added!")


**Component Definitions:**

- **Transactions**: List of all coin transfers in the block
- **Proof**: Special number discovered during mining
- **Hash**: Unique identifier for the block
- **Previous Hash**: Link to the preceding block in the chain

### Balance Checker

To check any user's balance:

1. Click "Check Balance"
2. Enter a username

**Calculation:**

Balance = Total coins received - Total coins sent

### Blockchain Validation

Click "Validate Blockchain" to verify chain integrity.

**Validation checks:**

- Hash accuracy for each block
- Proper linking between blocks
- Valid proof of work for each block
- Detection of any tampering

---

## Example Walkthrough

Follow these steps to see the blockchain in action:

**Create transactions:**

1. Alice -> Bob: 20 coins
2. Hadj -> Wassim: 150 coins
3. Wassim -> Warda: 300 coins

**Mine a block:**

Click "Mine Block Now" to process all pending transactions

**Verify results:**

- Check user balances
- Observe how transactions become permanent
- Review the new block in the blockchain explorer

---

## Core Concepts

### Transaction

A transfer of coins from one user to another. Transactions remain pending until included in a mined block. Once mined, they become permanent and irreversible.

### Mining

The process of finding a specific number (proof) that, when combined with block data and hashed using SHA-256, produces a hash beginning with the required number of zeros. This computational work secures the blockchain and prevents tampering.

### Block

A container that stores:

- A list of transactions
- Timestamp of creation
- Proof of work value
- Hash of the previous block

### Blockchain

A chain of blocks linked together through cryptographic hashes. Each block contains the hash of the previous block. Modifying any block invalidates all subsequent blocks, making the chain tamper-evident and secure.

---

## Technical Notes

- Uses SHA-256 cryptographic hashing
- Implements proof-of-work consensus mechanism
- Mining difficulty is adjustable
- Miner reward: 10 coins per block
- All transactions are public and transparent

# Additional Bonus:

---

### How to calculate the proof

**Goal:** Find a number where `hash(number² - previous_proof²)` starts with `0000`

```python
previous_proof = 100  # From last block

# Try numbers until hash starts with 0000
new_proof = 1
hash = SHA256(1² - 100²) = SHA256(-9999) = "a7f8..."  ❌ No

new_proof = 2  
hash = SHA256(4 - 10000) = SHA256(-9996) = "b2e4..."  ❌ No

new_proof = 3
hash = SHA256(9 - 10000) = SHA256(-9991) = "c1d9..."  ❌ No

... keep trying ...

new_proof = 45293
hash = SHA256(2051455849 - 10000) = "0000d8..."  ✅ YES!

PROOF = 45293  ← This is what we store

