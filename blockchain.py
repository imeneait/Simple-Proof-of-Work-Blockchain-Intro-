"""Core blockchain implementation"""
import hashlib
import json
import time
from transaction import Transaction

class Blockchain:
    def __init__(self, difficulty=4, mining_reward=10):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.total_blocks_mined = 0
        self.total_mining_time = 0
        
        # Create genesis block
        self.create_block(proof=1, previous_hash='0', transactions=[])

    def create_block(self, proof, previous_hash, transactions):
        """Creates a new block and adds it to the chain"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': transactions,
            'proof': proof,
            'previous_hash': previous_hash,
            'hash': ''
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """Returns the last block in the chain"""
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        Mining algorithm - finds a valid proof
        Returns: new_proof (int)
        """
        new_proof = 1
        check_proof = False
        attempts = 0
        start_time = time.time()
        
        target = '0' * self.difficulty
        
        while not check_proof:
            attempts += 1
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            if hash_operation[:self.difficulty] == target:
                check_proof = True
            else:
                new_proof += 1
        
        mining_time = time.time() - start_time
        self.total_mining_time += mining_time
        self.total_blocks_mined += 1
        
        print(f"✓ Proof found after {attempts:,} attempts in {mining_time:.2f}s")
        return new_proof

    def hash(self, block):
        """Creates a SHA-256 hash of a block"""
        block_copy = block.copy()
        block_copy.pop('hash', None)
        encoded_block = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """Validates the entire blockchain"""
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            # Check if previous hash matches
            if block['previous_hash'] != self.hash(previous_block):
                print(f"Invalid previous hash at block {block_index}")
                return False
            
            # Check proof of work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            target = '0' * self.difficulty
            if hash_operation[:self.difficulty] != target:
                print(f"Invalid proof of work at block {block_index}")
                return False
            
            previous_block = block
            block_index += 1
        
        return True

    def add_transaction(self, sender, receiver, amount):
        """Adds a new transaction to pending transactions"""
        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction.to_dict())
        next_block = self.get_previous_block()['index'] + 1
        print(f"💸 Transaction added: {sender} -> {receiver}: {amount} (will be in block #{next_block})")
        return next_block

    def mine_pending_transactions(self, miner_address):
        """Mines all pending transactions and rewards the miner"""
        # Add mining reward transaction
        reward_transaction = Transaction(
            sender="NETWORK",
            receiver=miner_address,
            amount=self.mining_reward
        )
        
        transactions_to_mine = self.pending_transactions.copy()
        transactions_to_mine.append(reward_transaction.to_dict())
        
        # Mine the block
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        
        block = self.create_block(proof, previous_hash, transactions_to_mine)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        return block

    def get_balance(self, address):
        """Calculates the balance of an address"""
        balance = 0
        for block in self.chain:
            for transaction in block.get('transactions', []):
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['receiver'] == address:
                    balance += transaction['amount']
        return balance

    def get_stats(self):
        """Returns blockchain statistics"""
        avg_mining_time = (self.total_mining_time / self.total_blocks_mined 
                          if self.total_blocks_mined > 0 else 0)
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': sum(len(block.get('transactions', [])) 
                                     for block in self.chain),
            'pending_transactions': len(self.pending_transactions),
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward,
            'average_mining_time': round(avg_mining_time, 2),
            'is_valid': self.is_chain_valid(self.chain)
        }