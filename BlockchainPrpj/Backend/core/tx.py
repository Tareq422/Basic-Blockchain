from BlockchainPrpj.Backend.core.Script import Script
from BlockchainPrpj.Backend.Util.util import int_to_little_endian, bytes_needed, decode_base58, little_endian_to_int

ZERO_HASH = b'\0' * 32
REWARD = 50
PRIVATE_KEY = "52511314197086284439605037603880996155243946729953061227855904766200054912807"
MINER_ADDRESS = "1LcBX7NxqCB84pNPyznQTAhzgMSqUjMH8G"

class CoinbaseTx:
    def __init__(self, BlockHeight): 
            self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight, bytes_needed(BlockHeight))
    
    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff
        tx_ins = []
        tx_ins.append(txIn(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)
        tx_outs = []
        target_amount = 100000000 * REWARD
        target_h160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(txOut(amount = target_amount, script_pubkey=target_script))

        return tx(1,tx_ins, tx_outs, 0)

class tx: 
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version 
        self.tx_ins = tx_ins 
        self.tx_outs= tx_outs
        self.locktime = locktime

    def is_coinbase(self):
        """""
        # Check that there is exactly one input 
        # Grab the first input and check if the prev_tx is b'\x00' * 32 
        # Check that the first input prev_index is 0xffffffff
        """""
        if len(self.tx_ins) != 1: 
            return False 
        
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32: 
            return False 
        
        if first_input.prev_index != 0xffffffff: 
            return False 
        
        return True
        
    
    def to_dict(self):
        """""
        Convert Coinbase Transaction 
        #Convert prev_tx hash in hex from bytes 
        # Conver Blockheight in hex which is stored in Script Signature
        """""

        if self.is_coinbase(): 
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_endian_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__

        
        self.tx_ins[0]= self.tx_ins[0].__dict__

        """""
        Convert Transaction Output to dict 
            # If there are numbers we dont need to do anything 
            # If values is in bytes, convert it to hex 
            # Loop through all the TxOut Objects and convert them into dict
        """""

        self.tx_outs[0].script_pubkey.cmds[2] = self.tx_outs[0].script_pubkey.cmds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__

        return self.__dict__


class txIn: 
    def __init__(self, prev_tx, prev_index, script_sig = None, sequence = 0xffffffff): 
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig is None: 
            self.script_sig = Script()
        else: 
            self.script_sig = script_sig 
        self.sequence = sequence 

class txOut: 
    def __init__(self, amount, script_pubkey): 
        self.amount =amount
        self.script_pubkey = script_pubkey