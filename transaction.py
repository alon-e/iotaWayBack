import datetime

all_nines = '999999999999999999999999999999999999999999999999999999999999999999999999999999999'


class transaction:
    def __init__(self,tryte_string, hash_string):
        self.hash = hash_string
        self.signature_message_fragment = tryte_string[0:2187]
        self.address = tryte_string[2187:2268]
        self.value = tryte_string[2268:2295]
        self.tag = tryte_string[2295:2322]
        self.timestamp = tryte_string[2322:2331]
        self.current_index = tryte_string[2331:2340]
        self.last_index = tryte_string[2340:2349]
        self.bundle_hash = tryte_string[2349:2430]
        self.trunk_transaction_hash = tryte_string[2430:2511]
        self.branch_transaction_hash = tryte_string[2511:2592]
        self.nonce = tryte_string[2592:2673]
        self.format()


    def format(self):
        # convert tryte values to numbers:
        self.value = transaction.trytes_to_number(self.value)
        self.timestamp = transaction.trytes_to_number(self.timestamp)
        self.current_index = transaction.trytes_to_number(self.current_index)
        self.last_index = transaction.trytes_to_number(self.last_index)

        #clean up edge values:
        self.tagIndex = transaction.trytes_to_number(self.tag)
        if self.tagIndex > 150354 or self.tagIndex < 0:
            self.tagIndex = 0
        #remove redundant all9 signatures
        if self.signature_message_fragment[:81] == all_nines:
            self.signature_message_fragment = ""

        #format timestamp as date:
        if self.timestamp > 1262304000000L:
            self.timestamp /= 1000L
        if self.timestamp > 0:
            self.timestampDate = datetime.datetime.fromtimestamp(self.timestamp)


    # Helpers

    tryte_table = {
        '9': [0, 0, 0],  # 0
        'A': [1, 0, 0],  # 1
        'B': [-1, 1, 0],  # 2
        'C': [0, 1, 0],  # 3
        'D': [1, 1, 0],  # 4
        'E': [-1, -1, 1],  # 5
        'F': [0, -1, 1],  # 6
        'G': [1, -1, 1],  # 7
        'H': [-1, 0, 1],  # 8
        'I': [0, 0, 1],  # 9
        'J': [1, 0, 1],  # 10
        'K': [-1, 1, 1],  # 11
        'L': [0, 1, 1],  # 12
        'M': [1, 1, 1],  # 13
        'N': [-1, -1, -1],  # -13
        'O': [0, -1, -1],  # -12
        'P': [1, -1, -1],  # -11
        'Q': [-1, 0, -1],  # -10
        'R': [0, 0, -1],  # -9
        'S': [1, 0, -1],  # -8
        'T': [-1, 1, -1],  # -7
        'U': [0, 1, -1],  # -6
        'V': [1, 1, -1],  # -5
        'W': [-1, -1, 0],  # -4
        'X': [0, -1, 0],  # -3
        'Y': [1, -1, 0],  # -2
        'Z': [-1, 0, 0],  # -1
    }


    @staticmethod
    def trytes_to_number(trytes):
        return transaction.convertBaseToBigint(transaction.trytes_to_trits(trytes))

    @staticmethod
    def trytes_to_trits(trytes):
        trits = []
        for tryte in trytes:
            trits.extend(transaction.tryte_table[tryte])
        return trits

    @staticmethod
    def convertBaseToBigint(array, base=3):
        bigint = 0
        for i in range(len(array)):
            bigint += array[i] * (base ** i)
        return bigint
