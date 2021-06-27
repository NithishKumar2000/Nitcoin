#  Creating my first Crypto Currecny

#Libraries Needed 
import datetime                          #This will be needed to keep track of exact date and time when each block is mined as each block has its own timestamp
import hashlib                           #This is used to hash the block
import json                              #This is used to encode the block
from flask import Flask,jsonify,request  #Flask is used to build the web app and jsonify is used to communicate with Postman
import requests
from uuid import uuid4
from urllib.parse import urlparse

#Building the Blockchain

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.create_block(proof=1,prev_hash='0')
        self.nodes=set()
    
    # Function to create a new block     
    def create_block(self,proof,prev_hash):
        block={'index':len(self.chain)+1,
               'time_stamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':prev_hash,
               'transactions':self.transactions}
        self.transactions=[]
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
    
    # Function to add new transaction to the list of transactions
    def add_transactions(self,sender,reciever,amount):
        transaction={'sender':sender,
                     'reciever':reciever,
                     'amount':amount}
        self.transactions.append(transaction)
        previous_block=self.get_previous_blocK()
        return previous_block['index']+1
    
    # Function to add new nodes
    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url)
        
    #Function to replace the original chain with the new longest chain that has been mined
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
            response=requests.get(f'http://{node}/get_chain')
            if response.status_code==200:
                chain=response.json()['chain']
                length=response.json()['length']
                if length>max_length and self.check_is_valid(chain):
                    longest_chain=chain
                    max_length=length
                if longest_chain: #This checks if the longest_chain is not none          
                    self.chain=longest_chain
                    return True
                return False
        
    
# Creating a web app
app=Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=False

# Creating an address for the node on port 5000 
node_address=str(uuid4()).replace('-'.'')

# Building the Blockchain    
blockchain=Blockchain()

# Function to Mine Block
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_blocK()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    blockchain.add_transactions(sender=node_address, reciever='Nithish', amount=1)
    new_block=blockchain.create_block(proof, previous_hash)
    response={'message':'Congrats! you have mined a block',
              'index ':new_block['index'],
              'time_stamp':new_block['time_stamp'],
              'proof':new_block['proof'],
               'previous_hash':new_block['previous_hash'],
               'transaction':new_block['transactions']}
    return jsonify(response),200

#Function to get the full Chain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)} 
    return jsonify(response),200

# Function to add transaction to the blockchain
@app.route('/add_transaction',methods=['POST'])
def add_transaction():
    json=request.get_json()
    transaction_keys=['sender','reciever'.'amount']
    for key in transaction_keys:
        if not all key in json:
            return 'Some elements are missing',400
    index=blockchain.add_transactions(json['sender'], json['reciever'], json['amount'])
    response={'message': f'This transaction will be added to the block {index}'}
    return jsonify(response),201

# Function to decentralize the system by adding nodes
@app.route('/connect_node',methods=['POST'])
def connnect_node():
    json=request.get_json()
    address=json.get('nodes')
    nodes=blockchain.add_node(address)
    if nodes is None:
        return 'The node is empty',400
    for node in nodes:
        blockchain.add_node(node)
    response={'message':'The node has been successfully added','Total nodes':list(blockchain.nodes)}
    return jsonify(message),201

# Function to replace the chain with the longest chain
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    valid_chain=blockchain.replace_chain()
    if valid_chain:
        response={'message':'The old chain has been replaced by the new longest chain','new chain':blockchain.chain}
    else:
        response={'message':'The existing chain is the longest chain','current chain':blockchain.chain}
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