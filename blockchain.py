#  Creating my first blockchain

#Libraries Needed 
import datetime                  #This will be needed to keep track of exact date and time when each block is mined as each block has its own timestamp
import hashlib                   #This is used to hash the block
import json                      #This is used to encode the block
from flask import Flask,jsonify  #Flask is udes to build the web app and jsonify is used to communicate with Postman

#Building the Blockchain

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,prev_hash='0')
    
    # Function to create a new block     
    def create_block(self,proof,prev_hash):
        block={'index':len(self.chain)+1,
               'time_stamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':prev_hash}
        self.chain.append(block)
        return block
    
    #function to get the value of the last block in the chain   
    def get_previous_blocK(self):
        return self.chain[-1];
    
    #function to give the miners a task to get the reward
    def proof_of_work(self,previous_proof):
       new_proof=1
       check_proof=False
       while check_proof is False:
           hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
           if hash_operation[:4]=='0000':
               check_proof=True
           else:
               new_proof+=1
       return new_proof
    
    # function to get the hash of any block
    def hash(self,block):
        encoded_block=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def check_is_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            block=chain[block_index]
            if block['previous_hash']!=self.hash(previous_block):
                return False
            previous_proof=previous_block['proof'] 
            proof=block[proof]
            hash_operation=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block=block
            block_index+=1
    
# Creating a web app
app=Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=False
# Building the Blockchain    
blockchain=Blockchain()

# Function to Mine Block
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_blocK()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    new_block=blockchain.create_block(proof, previous_hash)
    response={'message':'Congrats! you have mined a block',
              'index ':new_block['index'],
              'time_stamp':new_block['time_stamp'],
              'proof':new_block['proof'],
               'previous_hash':new_block['previous_hash']}
    return jsonify(response),200

#Function to get the full Chain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)} 
    return jsonify(response),200

#Function to check validity of the Chain
@app.route('/is_valid',methods=['GET'])
def is_valid():
    if blockchain.check_is_valid(blockchain.chain)==True:
        response={'message':'It is valid'}
    else:
        response={'message':'We have a problem'}
    return jsonify(response),200
#running the app
app.run('0.0.0.0',port=5000)
    
    
    
    
    
    
    