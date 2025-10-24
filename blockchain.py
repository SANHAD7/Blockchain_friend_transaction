import hashlib, datetime, json, requests

class Block:
    def __init__(self, index, timestamp, name, aadhaar_no, gender, dob, address, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.name = name
        self.aadhaar_no = aadhaar_no
        self.gender = gender
        self.dob = dob
        self.address = address
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "name": self.name,
            "aadhaar_no": self.aadhaar_no,
            "gender": self.gender,
            "dob": self.dob,
            "address": self.address,
            "previous_hash": self.previous_hash
        }
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = set()  # Other node URLs

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0", "None", "None", "None", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, name, aadhaar_no, gender, dob, address):
        prev_block = self.get_latest_block()
        new_block = Block(
            index=prev_block.index + 1,
            timestamp=datetime.datetime.now(),
            name=name,
            aadhaar_no=aadhaar_no,
            gender=gender,
            dob=dob,
            address=address,
            previous_hash=prev_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain
        for i in range(1, len(chain)):
            current = chain[i]
            prev = chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

    def is_aadhaar_registered(self, aadhaar_no):
        for block in self.chain[1:]:
            if str(block.aadhaar_no) == str(aadhaar_no):
                return True
        return False

    # ---------------- Decentralization ----------------
    def register_node(self, node_url):
        """Add a new node URL."""
        self.nodes.add(node_url)

    def resolve_conflicts(self):
        """Consensus algorithm: replace chain with longest valid chain in the network."""
        max_length = len(self.chain)
        new_chain = None

        for node in self.nodes:
            try:
                response = requests.get(f"{node}/chain")
                if response.status_code == 200:
                    data = response.json()
                    length = data['length']
                    chain_data = data['chain']

                    # Convert chain_data back to Block objects
                    temp_chain = []
                    for b in chain_data:
                        temp_block = Block(
                            b['index'], b['timestamp'], b['name'], b['aadhaar_no'],
                            b['gender'], b['dob'], b['address'], b['previous_hash']
                        )
                        temp_block.hash = b['hash']
                        temp_chain.append(temp_block)

                    if length > max_length and self.is_chain_valid(temp_chain):
                        max_length = length
                        new_chain = temp_chain
            except Exception as e:
                print(f"Node {node} unreachable: {e}")

        if new_chain:
            self.chain = new_chain
            return True
        return False
