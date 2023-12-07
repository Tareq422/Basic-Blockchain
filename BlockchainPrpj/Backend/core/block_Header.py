#\ BlockchainPrpj/Backend/core/block_Header.py
from BlockchainPrpj.Backend.Util.util import hash256

class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.blockHash = ""

    def mine(self):
        while self.blockHash[:4] != '0000':
            data_to_hash = (
                str(self.version)+
                self.prevBlockHash +
                self.merkleRoot +
                str(self.timestamp) +
                self.bits +
                str(self.nonce)
            )
            data_bytes = data_to_hash.encode()
            self.blockHash = hash256(data_bytes).hex()

            self.nonce += 1
        print(f"count till the hsash  {self.nonce}", end='\r')    
