import random

class VendorGenerator:
    vendors = set()

    def __init__(self, receipts):
        for receipt in receipts:
          if 'vendor' in receipt.groundTruth:
            self.vendors.add(receipt.groundTruth['vendor'])

    def generateVendor(self):
        return random.sample(self.vendors, 1)[0]

