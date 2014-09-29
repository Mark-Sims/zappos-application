import json
from urllib2 import Request, urlopen, URLError
import locale #For 2 decimal format numbers

key_file = open("key.txt", 'r')
key = key_file.read()

# Facet Table
# request = Request("http://api.zappos.com/Search?list=facetFields&type=facetable&key=" + key)

#Unnecessary information
# excludes = ["colorId", "originalPrice", "percentOff", "productId", "styleId"]

# Term: Boots
# request = Request('http://api.zappos.com/Search/term/boots?excludes=["colorId", "originalPrice", "percentOff", "productId", "styleId"]&sort={"price":"asc"}&limit=100' + '&key=' + key)

# dollars_left is a double - the total dollar amount we want to reach in the shopping cart
# num_items is an int - the total number of items we want in the shopping cart
# shopping_cart is a list of JSON objects - will be populated with $(num_items) items form the Zappos Catalog
# catalog is the list of items from the Zappos Catalog.

def populateCatalog(ideal_cost_per_item):
	# No Term
	offset =  0
	request = Request('http://api.zappos.com/Search?excludes=["colorId", "originalPrice", "percentOff", "productId", "styleId", "thumbnailImageUrl"]&sort={"price":"asc"}&limit=100&filters={"price":["' 
		+ str(round(ideal_cost_per_item + .00 +  offset,2)) + '", "' # When offset == 0, this is the exact ideal_cost_per_item price
		+ str(round(ideal_cost_per_item + .01 +  offset,2)) + '", "' 
		+ str(round(ideal_cost_per_item + .02 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .03 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .04 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .05 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .06 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .07 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .08 +  offset,2)) + '", "' 		
		+ str(round(ideal_cost_per_item + .09 +  offset,2)) + '"]}' + '&key=' + key)

	# I want to get a range of the prices of items. I can't use a range call from the Search API, so I have to manually check each $0.01. To
	# simulate a range.

	try:
		response = urlopen(request)
		plain_text = response.read()
		parsed = json.loads(plain_text)
		print json.dumps(parsed, indent=4, sort_keys=True)
	except URLError, e:
   		print 'Got an error code:', e


	while(parsed['currentResultCount'] == "0" and offset < 2.00): #Max out at 20 API requests, don't want to max out my key!
		#this means that there were no items in the catalog which were in the price range ideal_cost_per_item + $0.09
		#I'll offset the prices checked by $0.10 and check again.
		offset = round((offset + 0.10), 2)
		request = Request('http://api.zappos.com/Search?excludes=["colorId", "originalPrice", "percentOff", "productId", "styleId", "thumbnailImageUrl"]&sort={"price":"asc"}&limit=100&filters={"price":["' 
			+ str(round(ideal_cost_per_item + .00 +  offset,2)) + '", "' # When offset == 0, this is the exact ideal_cost_per_item price
			+ str(round(ideal_cost_per_item + .01 +  offset,2)) + '", "' 
			+ str(round(ideal_cost_per_item + .02 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .03 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .04 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .05 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .06 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .07 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .08 +  offset,2)) + '", "' 		
			+ str(round(ideal_cost_per_item + .09 +  offset,2)) + '"]}' + '&key=' + key)

		try:
			response = urlopen(request)
			plain_text = response.read()
			parsed = json.loads(plain_text)
			print json.dumps(parsed, indent=4, sort_keys=True)
		except URLError, e:
	   		print 'Got an error code:', e
			


def getCombosWrapper(dollars_left, num_items, shopping_cart):
	if(num_items <= 0 or dollars_left <= 0):
		return
	elif(num_items > 0 and dollars_left > 0):
		pass		

# catalog = [1.34, 1.63, 3.01, 4.02, 4.99, 4.99, 4.99, 7.34, 11.23, 14.62, 15.59, 16.88]


def getIndexOfMostExpensiveItemWhichCostsLessThanOrEqualTo(cost):
	i = binary_search(catalog, cost, 0, len(catalog))
	if(catalog[i] < cost and i + 1 < len(catalog) and catalog[i + 1] <= cost):
		while(i + 1 < len(catalog) and catalog[i + 1] <= cost):
			i = i + 1
		return i - 1
	if(i < 0):
		return -1
	else:
		return i


def binary_search(catalog, cost, left, right):
	mid = left + ((right - left) / 2)	
	if(catalog[mid] == cost or left >= right):
		return mid
	elif(catalog[mid] > cost): # Search LEFT half
		return binary_search(catalog, cost, left, mid)
	else: # Search RIGHT half
		return binary_search(catalog, cost, mid + 1, right)


# Approach: I plan on selecting items whose price is as close as possible to dollar_amount/num_items, (the ideal_cost_per_item.)
# I will calculate the ideal_cost_per_item and then try to find items whose price is as close as possible to this cost.

def getCombos(dollars_left, num_items):
	ideal_cost_per_item = round((dollars_left / num_items),2)
	print ideal_cost_per_item
	catalog = populateCatalog(ideal_cost_per_item)
	shopping_cart = []
#	getCombosWrapper(dollars_left, num_items, shopping_cart)

getCombos(152.00, 7)