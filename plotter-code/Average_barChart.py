
products = ['beauty', 'clothe', 'toys and kids', 'book & stationary & art', 'rural goods', 'travel']
prices = [int(1513533580 / 13279), int(1299180990 / 5439), int(722506910 / 2935), int(393028650 / 3893),
          int(316228250 / 636), int(60227550 / 504)]


# function to add value labels
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])



plt.figure(figsize=(10, 6))
plt.bar(products, prices, color='skyblue')
# Adding title and labels
addlabels(products, prices)
plt.title('Average Price Of Product in Category')
plt.xlabel('Category')
plt.ylabel('Average Price')

plt.show()