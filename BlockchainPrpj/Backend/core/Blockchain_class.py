# Your third file
import sys
sys.path.append("/Work/Development/Web/Github/ICS440/Basic-Blockchain")
import time
from BlockchainPrpj.Backend.core.block import Block
from BlockchainPrpj.Backend.core.block_Header import BlockHeader
from BlockchainPrpj.Backend.Util.util import hash256, merkle_root
from BlockchainPrpj.Backend.core.Database.database import Blockchaindb
from BlockchainPrpj.Backend.core.tx import CoinbaseTx
from multiprocessing import Process, Manager
from BlockchainPrpj.Frontend.run import main
import json
ZERO_HASH = "0" * 64
VERSION = 0

class Blockchain:
    def __init__(self, utxos, MemPool):
       self.utxos = utxos
       self.MemPool = MemPool


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
    
    """Keep Track of all the unspent Transaction in cache memory for fast retival"""
    def store_utxos_in_cache(self):
       for Tx in self.addTransactionsInBlock:
          print(f"Transcation added {Tx.TxId} ")
          self.utxos[Tx.TxId] = Tx
    
    def remove_spent_Transactions(self):
       for txId_index in self.remove_spent_transactions:
          if txId_index[0].hex() in self.utxos:
             if len(self.utxos[txId_index[0].hex()].tx_outs) < 2:
                print(f"Spent Transcation removed {txId_index[0].hex()} ")
                del self.utxos[txId_index[0].hex()]
             else:
                prev_trans = self.utxos[txId_index[0].hex()]
                self.utxos[txId_index[0].hex()] = prev_trans.tx_outs.pop(txId_index[1])

            
    
    """Read Transactions from Memory Pool"""
    def read_transaction_from_memorypool(self):
       self.TxIds = []
       self.addTransactionsInBlock = []
       self.remove_spent_transactions = []

       for Tx in self.MemPool:
          self.TxIds.append(bytes.fromhex(Tx))
          self.addTransactionsInBlock.append(self.MemPool[Tx])

          for spent in self.MemPool[Tx].tx_ins:
             self.remove_spent_transactions.append([spent.prev_tx, spent.prev_index])
    
    def convert_to_json(self):
       self.TxJson = []
       for Tx in self.addTransactionsInBlock:
          self.TxJson.append(Tx.to_dict())


    def add_block(self, block_height, prev_block_hash):
        self.read_transaction_from_memorypool()
        timestamp = int(time.time())
        coinbaseInstance = CoinbaseTx(block_height) #BlockHeight
        coinbaseTx = coinbaseInstance.CoinbaseTransaction()

        self.TxIds.insert(0, bytes.fromhex(coinbaseTx.TxId))
        self.addTransactionsInBlock.insert(0, coinbaseTx)


        merkleRoot = merkle_root(self.TxIds)[::-1].hex()
        bits = "ffff001f"
        block_header = BlockHeader(VERSION, prev_block_hash, merkleRoot, timestamp, bits)
        block_header.mine()
        self.remove_spent_Transactions()
        self.store_utxos_in_cache()
        self.convert_to_json()
        self.write_to_disk([Block(block_height, 1, block_header.__dict__, 1, self.TxJson).__dict__])



    def main(self):
       lastblock = self.get_last_block()

       if lastblock is None:
        self.genesis_block()

       else:
        while True:
            lastblock = self.get_last_block()
            block_height = lastblock["Height"]+1
            prev_block_hash = lastblock["BlockHeader"]["blockHash"]
            self.add_block(block_height,prev_block_hash)

if __name__ == "__main__":
    with Manager() as manager:
       utxos = manager.dict()
       MemPool = manager.dict()

       webapp = Process(target = main, args = (utxos, MemPool))
       webapp.start()
    
       blockchain = Blockchain(utxos, MemPool)
       blockchain.main()
