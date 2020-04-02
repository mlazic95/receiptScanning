import csv
import random

streetPath = '/Users/markolazic/Desktop/exjobb/project/data/addresses/streetNames.csv'
cities = ['STOCKHOLM', 'MALMO', 'LUND', 'HELSINGBORG', 'HALMSTAD', 'VAXJO', 'KALMAR', 'GOTHENBURG', 'BOROS', 'JONKOPING', 'NORRKOPING', 'ESKILSTUNA', 'KARLSTAD', 'OREBRO', 'VESTEROS', 'GAVLE', 'SUNDSVALL', 'UMEO', 'LULEO', 'UPPSALA']
class AddressGenerator:
    streetNames = []
    with open(streetPath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            streetNames.append(row[1])


    def generateAddress(self):
        street = random.choice(self.streetNames)
        number = str(random.randint(1,120))
        if random.random() < 0.05:
          number += '-' + str(int(number) + 2)
        if random.random() < 0.01:
          return street + ' ' + number
        if random.random() < 0.1:
          number += ','
        postalCode = str(random.randint(100,999)) + ' ' + str(random.randint(10,99))
        if random.random() < 0.1:
          postalCode = postalCode.replace(' ', '')
        city = random.choice(cities)
        return  street + ' ' + number + ' ' + postalCode + ' ' + city


