# Your third file
import sys
sys.path.append("/Users/tariq/Desktop/ICS440-Project")
import time
from BlockchainPrpj.Backend.core.block import Block
from BlockchainPrpj.Backend.core.block_Header import BlockHeader
from BlockchainPrpj.Backend.Util.util import hash256, merkle_root,target_to_bits
from BlockchainPrpj.Backend.core.Database.database import Blockchaindb
from BlockchainPrpj.Backend.core.tx import CoinbaseTx
from multiprocessing import Process, Manager
from BlockchainPrpj.Frontend.run import main
ZERO_HASH = "0" * 64
VERSION = 0
INITIAL_TARGET = 0x0000FFFF00000000000000000000000000000000000000000000000000000000


class Blockchain:
    def __init__(self, utxos, MemPool):
       self.utxos = utxos
       self.MemPool = MemPool
       self.current_target = INITIAL_TARGET
       self.bits = target_to_bits(INITIAL_TARGET)

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
       self.Blocksize = 80
       self.TxIds = []
       self.addTransactionsInBlock = []
       self.remove_spent_transactions = []

       for Tx in self.MemPool:
          self.TxIds.append(bytes.fromhex(Tx))
          self.addTransactionsInBlock.append(self.MemPool[Tx])
          self.Blocksize += len(self.MemPool[tx].serialize())

          for spent in self.MemPool[Tx].tx_ins:
             self.remove_spent_transactions.append([spent.prev_tx, spent.prev_index])
    
    def convert_to_json(self):
       self.TxJson = []
       for Tx in self.addTransactionsInBlock:
          self.TxJson.append(Tx.to_dict())

    
    def remove_transections_from_memopool(self):
       for tx in self.TxIds:
          if tx.hex() in self.MemPool:
             del self.MemPool[tx.gex()]
     

    def calculate_fee(self):
        self.input_amount = 0
        self.output_amount = 0
        """ Calculate Input Amount """
        for TxId_index in self.remove_spent_transactions:
            if TxId_index[0].hex() in self.utxos:
                self.input_amount += (
                    self.utxos[TxId_index[0].hex()].tx_outs[TxId_index[1]].amount
                )

        """ Calculate Output Amount """
        for tx in self.addTransactionsInBlock:
            for tx_out in tx.tx_outs:
                self.output_amount += tx_out.amount

        self.fee = self.input_amount - self.output_amount

    def add_block(self, block_height, prev_block_hash):
        self.read_transaction_from_memorypool()
        self.calculate_fee()
        timestamp = int(time.time())
        coinbaseInstance = CoinbaseTx(block_height) #BlockHeight
        coinbaseTx = coinbaseInstance.CoinbaseTransaction()
        self.Blocksize += len(coinbaseTx.serialize())
        coinbaseTx.tx_outs[0].amount = coinbaseTx.tx_outs[0].amount + self.fee
        self.TxIds.insert(0, bytes.fromhex(coinbaseTx.id()))
        self.addTransactionsInBlock.insert(0, coinbaseTx)


        merkleRoot = merkle_root(self.TxIds)[::-1].hex()
        
        block_header = BlockHeader(VERSION, prev_block_hash, merkleRoot, timestamp, self.bits)
        block_header.mine(self.current_target)
        self.remove_spent_Transactions()
        self.remove_transections_from_memopool()
        self.store_utxos_in_cache()
        self.convert_to_json()
        self.write_to_disk([Block(block_height, self.Blocksize, block_header.__dict__, 1, self.TxJson).__dict__])



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