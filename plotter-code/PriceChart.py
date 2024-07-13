products = ['beauty', 'clothe', 'toys and kids', 'book & stationary & art', 'rural goods', 'travel']
prices = [1513533580, 1299180990, 722506910, 393028650, 316228250, 60227550]

total = sum(prices)

percentages = [(price / total) * 100 for price in prices]

plt.figure(figsize=(8, 8))
plt.pie(percentages, labels=products, autopct='%1.1f%%', startangle=140)
plt.title('Category Price Distribution')
plt.show()