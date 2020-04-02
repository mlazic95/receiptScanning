import random

class ProductsGenerator:
    productNames = set()

    def __init__(self, receipts):
        for receipt in receipts:
          if 'products' in receipt.groundTruth:
              for product in receipt.groundTruth['products']:
                    self.productNames.add(product['name'])

    def generateProducts(self):
        return random.sample(self.productNames, 1)[0]

