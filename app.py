"""Flask application and API routes"""
from flask import Flask, jsonify, request, render_template
import threading
import time
import random

from blockchain import Blockchain
from config import Config

# Initialize blockchain
blockchain = Blockchain(
    difficulty=Config.DIFFICULTY,
    mining_reward=Config.MINING_REWARD
)

# Initialize Flask app
app = Flask(__name__)

# Auto-mining control
auto_mining_active = False

# ==================== WEB ROUTES ====================

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/get_chain', methods=['GET'])
def get_chain():
    """Get the entire blockchain with statistics"""
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'stats': blockchain.get_stats(),
        'pending': blockchain.pending_transactions
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """Add a new transaction to the pending pool"""
    data = request.get_json()
    
    # Validate input
    required_fields = ['sender', 'receiver', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    next_block = blockchain.add_transaction(
        sender=data['sender'],
        receiver=data['receiver'],
        amount=amount
    )
    
    return jsonify({
        'message': f'Transaction will be added to block {next_block}',
        'block_index': next_block
    }), 201

@app.route('/mine_block', methods=['POST'])
def mine_block():
    """Mine a new block with pending transactions"""
    data = request.get_json() or {}
    miner_address = data.get('miner', 'DEFAULT_MINER')
    
    if len(blockchain.pending_transactions) == 0:
        return jsonify({
            'message': 'No transactions to mine',
            'block': None
        }), 200
    
    block = blockchain.mine_pending_transactions(miner_address)
    
    return jsonify({
        'message': f'Block {block["index"]} mined successfully!',
        'block': block,
        'transactions': len(block['transactions']),
        'hash': block['hash']
    }), 200

@app.route('/validate_chain', methods=['GET'])
def validate_chain():
    """Validate the entire blockchain"""
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    return jsonify({
        'valid': is_valid,
        'message': 'Blockchain is valid' if is_valid else 'Blockchain is invalid'
    }), 200

@app.route('/get_balance/<address>', methods=['GET'])
def get_balance(address):
    """Get the balance of a specific address"""
    balance = blockchain.get_balance(address)
    return jsonify({
        'address': address,
        'balance': balance
    }), 200

@app.route('/toggle_auto_mine', methods=['POST'])
def toggle_auto_mine():
    """Toggle automatic mining on/off"""
    global auto_mining_active
    auto_mining_active = not auto_mining_active
    
    status = 'enabled' if auto_mining_active else 'disabled'
    print(f"\n🔄 Auto-mining {status}")
    
    return jsonify({
        'auto_mining': auto_mining_active,
        'message': f'Auto-mining {status}'
    }), 200

# ==================== BACKGROUND TASKS ====================

def auto_mine():
    """Automatically mine blocks when there are pending transactions"""
    while True:
        try:
            if auto_mining_active and len(blockchain.pending_transactions) > 0:
                print("\n Auto-mining activated...")
                block = blockchain.mine_pending_transactions('AUTO_MINER')
                print(f"Block #{block['index']} mined with {len(block['transactions'])} transactions")
                print(f"   Hash: {block['hash'][:16]}...")
        except Exception as e:
            print(f"Auto-mining error: {e}")
        
        time.sleep(Config.AUTO_MINE_INTERVAL)

def add_sample_data():
    """Add some sample transactions for demonstration"""
    time.sleep(2)  # Wait for server to start
    
    users = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    
    print("\n📝 Adding sample transactions...")
    for i in range(5):
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u != sender])
        amount = random.randint(5, 50)
        
        blockchain.add_transaction(sender, receiver, amount)
        time.sleep(0.5)
    
    print("✅ Sample transactions added!")

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🔗  EDUCATIONAL BLOCKCHAIN SIMULATOR")
    print("="*70)
    print(f"\n📍 Server starting at: http://localhost:{Config.PORT}")
    print(f"   Open this URL in your browser to interact with the blockchain")
    print("\n✨ Features:")
    print("   • 💸 Create transactions between users")
    print("   • ⛏️  Mine blocks manually or automatically")
    print("   • ✓  Validate blockchain integrity")
    print("   • 📊 View real-time statistics")
    print("   • 💰 Check address balances")
    print("\n🎓 Perfect for learning blockchain concepts!")
    print("="*70 + "\n")
    
    # Start auto-mining thread
    mining_thread = threading.Thread(target=auto_mine, daemon=True)
    mining_thread.start()
    
    # Add sample data thread
    sample_thread = threading.Thread(target=add_sample_data, daemon=True)
    sample_thread.start()
    
    # Start Flask server
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )