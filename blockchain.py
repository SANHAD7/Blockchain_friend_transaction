import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, sender, receiver, amount, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis", "Genesis", 0, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, sender, receiver, amount):
        prev_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=str(datetime.datetime.now()),
            sender=sender,
            receiver=receiver,
            amount=amount,
            previous_hash=prev_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
