#import json
#from urllib2 import Request, urlopen, URLError

#key_file = open("key.txt", 'r')
#key = key_file.read()

#request = Request('http://api.zappos.com/Search?list=facetFields&type=facetable&key=' + key)

#try:
#	response = urlopen(request)
#	plain_text = response.read()
#	parsed = json.loads(plain_text)
#	print json.dumps(parsed, indent=4, sort_keys=True)

#except URLError, e:
#    print 'Got an error code:', e

# dollars_left is a double - the total dollar amount we want to reach in the shopping cart
# num_items is an int - the total number of items we want in the shopping cart
# shopping_cart is a list of JSON objects - will be populated with $(num_items) items form the Zappos Catalog

# catalog - a list of all the items in the Zappos Catalog whose cost is less than dollar_amount
#	  - sorted according to cost - ascending.

def getCombos(dollars_left, num_items):
	shopping_cart = []
	getCombosWrapper(dollars_left, num_items, shopping_cart)

def getCombosWrapper(dollars_left, num_items, shopping_cart):
	if(num_items <= 0 or dollars_left <= 0):
		return
	elif(num_items > 0 and dollars_left > 0):
		pass		

catalog = [1.34, 1.63, 3.00, 4.00, 4.99, 4.99, 4.99, 7.34, 11.23, 14.62, 15.59, 16.88]


def getIndexOfMostExpensiveItemWhichCostsLessThan(cost):
	i = binary_search(catalog, cost, 0, len(catalog))
	while(i < len(catalog) and catalog[i] < cost):
		i = i + 1
#	if(i == len(catalog)):
	return i - 1
#	else:
#		return i


def binary_search(catalog, cost, left, right):
	#print("Searching:", catalog[left:right])
	mid = left + ((right - left) / 2)
	if(catalog[mid] == cost or left == mid):
#		i = len(catalog)/2
#		while(i + 1 < len(catalot) and catalog[i + 1] == cost): #There can be multiple items with the same cost. Therefore, I need to still
									#still consider ALL items whose cost is				
		#if(catalog[len(catalog)/2] == cost):
		return mid
	elif(catalog[mid] > cost): # Search LEFT half
		return binary_search(catalog, cost, left, mid)
	else: # Search RIGHT half
		return binary_search(catalog, cost, mid, right)
a = 1.00
while(a < 18.00):
	print a, "   ", getIndexOfMostExpensiveItemWhichCostsLessThan(a)
	a = a + 0.01
