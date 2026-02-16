"""Transaction class for blockchain"""
import time

class Transaction:
    """Represents a transaction in the blockchain"""
    
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    def __repr__(self):
        return f"Transaction({self.sender} -> {self.receiver}: {self.amount})"