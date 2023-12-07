import os
import json
"""
this class will be responsbile for writing the block into
the blockchain and reading the blockchain
one we create the class instance and start having block
a file will be created to register all blocks
"""

class db:
    def __init__(self):
        #creating file to store the blocks on disk
        self.path = "data"
        self.filepath = "/".join([self.path, self.filename])
    
    """
    this method read the entire blockchain and convert it
    to python dictanry to then send  the data to write method
    """
    def read(self):
        if not os.path.exists(self.filepath):
            print("file does not exists")
            return False
        
        with open(self.filepath,"r") as file:
            raw = file.readline()

        if len(raw)>0:
            data = json.loads(raw) 

       #first block in the blockchain
        else:
            data = []
        return data           
    # method to add new block to the blockchain
    def write(self, block):
        data = self.read()

        if data:
            #adding the block to the blockchain
            data = data + block  

        else:
            data = block    

        with open(self.filepath, "w+") as file:

            file.write(json.dumps(data))

#inherting the db class
class Blockchaindb(db):

    def __init__(self):
        self.filename = "blockchain"
        super().__init__()

    def last_block(self):
        data = self.read()

        if data:
            return data[-1]    
