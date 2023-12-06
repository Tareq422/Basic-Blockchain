# Your third file
import sys
sys.path.append("/Users/tariq/Desktop/ICS440-Project")
import time
from BlockchainPrpj.Backend.core.block import Block
from BlockchainPrpj.Backend.core.block_Header import BlockHeader
from BlockchainPrpj.Backend.Util.util import hash256
from BlockchainPrpj.Backend.core.Database.database import Blockchaindb
import json
ZERO_HASH = "0" * 64
VERSION = 0

class Blockchain:
    def __init__(self):
       # self.chain = []
        self.genesis_block()


    #use the database write method
    def write_to_disk(self,block):
        dbObject = Blockchaindb()
        dbObject.write(block)


    #use the database last_block method
    def get_last_block(self):
        dbObject = Blockchaindb()
        return dbObject.last_block()
    

    def genesis_block(self):
        block_height = 0
        prev_block_hash = ZERO_HASH
        self.add_block(block_height, prev_block_hash)


    def add_block(self, block_height, prev_block_hash):
        timestamp = int(time.time())
        transaction = f"Tariq sends {block_height} bitcoin to Ziyad"
        merkle_root = hash256(transaction.encode()).hex()
        bits = "ffff001f"
        block_header = BlockHeader(VERSION, prev_block_hash, merkle_root, timestamp, bits)
        block_header.mine()
        self.write_to_disk([Block(block_height, 1, block_header.__dict__, 1, transaction).__dict__])



    def main(self):
       
        while True:
            lastblock = self.get_last_block()
            block_height = lastblock["Height"]+1
            prev_block_hash = lastblock["BlockHeader"]["blockHash"]
            self.add_block(block_height,prev_block_hash)

if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()
