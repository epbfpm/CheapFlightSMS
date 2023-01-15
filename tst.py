import pandas

data = pandas.read_csv('Flight Deals - prices.csv')
data = data.to_dict(orient='records')
new_entry = {
    'City': 'Ciudad Del Mexico',
    'IATA Code': 'AJU',
    'Lowest Price': 5000
}
data.append(new_entry)
x = pandas.DataFrame(data)
x.to_csv('Flight Deals - prices.csv')
print(x)


