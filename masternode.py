import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request, session
from flask_cors import CORS


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = [
       {"index":1,"previous_hash":"1","proof":100,"timestamp":1640696852.925139,"transactions":[]},{"index":2,"previous_hash":"06fe3ad489fee0a1e004b15f820e3fe2ed39374c296b792b3d9d36bbb754c935","proof":80286,"timestamp":1640696963.556868,"transactions":[{"amount":370000,"message":"Rice","purpose":"Donation Request","recipient":"0","sender":"c274f599a24f41d797a60d63f356e26b"}]},{"index":3,"previous_hash":"605fd958493ae89da3c5a14c2bc9787def2c8c0325ada14e303834dfa5abcd6a","proof":73720,"timestamp":1640696993.744761,"transactions":[{"amount":80000,"message":"Toilet Paper","purpose":"Donation Request","recipient":"0","sender":"5f979dfb57624830a91dd6dda787d12f"}]},{"index":4,"previous_hash":"fb76f2969558bde748f63c7f978ec5dad9f7fbdbf0e833df4bc5dedf7f46063a","proof":21774,"timestamp":1657267195.9840703,"transactions":[{"amount":20000,"message":"Donation","purpose":"Donation Response","recipient":"5f979dfb57624830a91dd6dda787d12f","sender":"5c354ad8f4484fb3a39273b1587b1080"}]},{"index":5,"previous_hash":"d4596a8734cc8b03e15ba99daacc025f3d80cd956da8495d4952613a6493fe4a","proof":110529,"timestamp":1657267231.2532568,"transactions":[{"amount":20000,"message":"Donation","purpose":"Donation Response","recipient":"5f979dfb57624830a91dd6dda787d12f","sender":"5d354ad8f4484fb3a39273b1587b1080"}]},{"index":6,"previous_hash":"a00804c4a6cf15dbccdd1cb93e7493053c3eed1dbc77882f0346269c0fbc4ace","proof":46206,"timestamp":1657267251.3818402,"transactions":[{"amount":40000,"message":"Donation","purpose":"Donation Response","recipient":"5f979dfb57624830a91dd6dda787d12f","sender":"5v354ad8f4484fb3a39273b1587b1080"}]},{"index":7,"previous_hash":"36ea883a5818fc468ef121b94fc0994bcecfb04e5370c0506f90d26c3b6703b6","proof":90894,"timestamp":1657268284.0423017,"transactions":[{"amount":80000,"message":"Toilet Paper","purpose":"Buy","recipient":"e4408ab6fdd1443ca5b099afd32588d1","sender":"5f979dfb57624830a91dd6dda787d12f"}]},{"index":8,"previous_hash":"c8a3e7c9f23a2e641665993626cfc2683aab85a40333ec312915d00b6fc6eaa1","proof":17797,"timestamp":1657287943.854492,"transactions":[{"amount":150000,"message":"Printer at Amazon","purpose":"Donation Request","recipient":"0","sender":"064283fdf86a44e9bfade12b5f136151"}]}
    ]
        self.nodes = set()
        self.wallets = []
        # Create the genesis block
        #self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        print(self.current_transactions)
        for transaction in self.current_transactions:
            for tmp in self.wallets:
                if tmp['addr'] == transaction['sender'] and transaction['purpose'] != "Donation Request":
                    tmp['coin'] -= transaction['amount']

                if tmp['addr'] == transaction['recipient'] and transaction['purpose'] != "Donation Request":
                    tmp['coin'] += transaction['amount']
        print(self.wallets)
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, purpose, message, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'purpose' : purpose,
            'message' : message,
            'sender': sender,
            'recipient': recipient,
            'amount': int(amount),
        })

        return self.last_block['index'] + 1


    def register_wallet(self, address):
        tmp = {'addr' : address, 'coin' : 0}
        chk = next((item for item in self.wallets if item['addr'] == tmp['addr']), None)
        if chk == None:
            self.wallets.append(tmp)
            return True
        return False

    def check_wallet(self, address):
        wallet = next((item for item in self.wallets if item['addr'] == address), None)
        if wallet == None:
            return "fail"
        return wallet

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
blockchain.register_wallet(node_identifier)

@app.route('/mine', methods=['GET'])
def mine():
    if blockchain.current_transactions == []:
        return "No new transactions", 201
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    # blockchain.new_transaction(
    #     sender="0",
    #     recipient=node_identifier,
    #     amount=1,
    # )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print(values)
    # Check that the required fields are in the POST'ed data
    required = ['purpose', 'message', 'sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['purpose'], values['message'], values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

@app.route('/wallets/register', methods=['POST'])
def register_wallet():
    values = request.get_json()

    new_wallet = values.get('addr')
    print(new_wallet)
    if new_wallet is None:
        return "Error: Please supply a valid list of address", 400

    res = blockchain.register_wallet(new_wallet)
    if res == False:
        response = {
            'message': 'Welcome',
#            'wallets': list(blockchain.wallets),
        }
        return jsonify(response), 201
    response = {
        'message': 'New wallets have been added',
#        'wallets': list(blockchain.wallets),
    }
    return jsonify(response), 201

@app.route('/wallets/check', methods=['POST'])
def check_wallet():
    values = request.get_json()

    wallet = values.get('addr')
    if wallet is None:
        return "Error: Please supply a valid list of address", 400

    res = blockchain.check_wallet(wallet)
    return jsonify(res), 201

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=1000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
