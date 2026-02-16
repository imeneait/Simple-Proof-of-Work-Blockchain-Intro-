class Config:
    # Blockchain settings
    DIFFICULTY = 4  # Number of leading zeros required in hash
    MINING_REWARD = 10  # Reward for mining a block
    
    # Flask settings
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = False
    
    # Mining settings
    AUTO_MINE_INTERVAL = 3  # seconds between auto-mining attempts
    MANUAL_MINE_DELAY = 2  # seconds delay for manual mining