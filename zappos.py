import json
from urllib2 import Request, urlopen, URLError

key_file = open("key.txt", 'r')
key = key_file.read()

DESIRED_DOLLAR_AMOUNT = 120.00
NUMBER_OF_DESIRED_PRODUCTS = 4

NUMBER_OF_COMBOS_TO_PRINT = 5

# Facet Table
# request = Request("http://api.zappos.com/Search?list=facetFields&type=facetable&key=" + key)

#Unnecessary information
# excludes = ["originalPrice", "percentOff", "productId", "styleId"]

# Term: Boots
# request = Request('http://api.zappos.com/Search/term/boots?excludes=["colorId", "originalPrice", "percentOff", "productId", "styleId"]&sort={"price":"asc"}&limit=100' + '&key=' + key)

# dollars_left is a double - the total dollar amount we want to reach in the shopping cart
# num_items is an int - the total number of items we want in the shopping cart
# shopping_cart is a list of JSON objects - will be populated with $(num_items) items form the Zappos Catalog

# catalog is the list of items from the Zappos Catalog.
# catalog is a JSON object which can be accessed as a dictionary. The 'requests' entry in the dictionary, contains a 
# list of all of the products I retrieved from the Zappos API. Each object in the 'requests' list is another dictionary
# containing information about each particular item. For viewability, I filter out (exclude) a lot of information that I don't think
# the user needs to see about each item/product in the 'requests' list.

def populateCatalog(ideal_cost_per_item):
	# No Term
	offset =  0
	request = Request('http://api.zappos.com/Search?excludes=["originalPrice", "percentOff", "productId", "styleId", "thumbnailImageUrl"]&sort={"price":"asc"}&limit=100&filters={"price":["' 
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
		if(parsed['currentResultCount'] != "0"):
			#print json.dumps(parsed, indent=4, sort_keys=True)
			pass
		else:
			print ("No items found in the range " 
			+ str(round(ideal_cost_per_item + .00 +  offset,2))
			+ " - "
			+ str(round(ideal_cost_per_item + .09 +  offset,2)))

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
			if(parsed['currentResultCount'] != "0"):
				#print json.dumps(parsed, indent=4, sort_keys=True)
				return parsed
			else:
				print ("No items found in the range " 
				+ str(round(ideal_cost_per_item + .00 +  offset,2))
				+ " - "
				+ str(round(ideal_cost_per_item + .09 +  offset,2)))		
		except URLError, e:
	   		print 'Got an error code:', e
	return parsed #Should only return here if parsed has "0" for currentResultsCount
			
# catalog = [1.34, 1.63, 3.01, 4.02, 4.99, 4.99, 4.99, 7.34, 11.23, 14.62, 15.59, 16.88]


def printCart(shopping_cart):
	print("============================")
	i = 0
	total = 0
	while(i < len(shopping_cart)):
		print("Product " + str(i+1) + "/" + str(len(shopping_cart)) + " - "
			+ "	Name: " + shopping_cart[i]['productName'] + '\n'
			+ "		ColorID: " + shopping_cart[i]['colorId'] + '\n'
			+ "		Price: " + shopping_cart[i]['price'] + '\n')
		total = round(total + float(str(shopping_cart[i]['price'])[1:]), 2)
		i = i + 1
	print("=============================")
	print("Total Cost = " + str(total))
	print("=============================")

# Approach: I plan on selecting items whose price is as close as possible to dollar_amount/num_items, (the ideal_cost_per_item.)
# I will calculate the ideal_cost_per_item and then try to find items whose price is as close as possible to this cost.

def getCombos(dollars_left, num_items):
	ideal_cost_per_item = round((dollars_left / num_items),2)
#	print ideal_cost_per_item
	catalog = populateCatalog(ideal_cost_per_item)
	if(catalog['currentResultCount'] == "0"):	#Note: This case should be extremely rare, but is still a possibility.
		print ("FAILURE: Couldn't find items within price range." 
			+ "\n"
			+ "I looked through the entire Zappos Catalog and couldn't find any items within $2.00 of "
			+ str(ideal_cost_per_item)
			+ ". I stopped looking after $2.00 because the API Key I am using is rate limited and I don't want to run out of requests!")

	# By default, I will print 5 combinations of 
	combos_printed = 0
	
	while(combos_printed < NUMBER_OF_COMBOS_TO_PRINT):
		shopping_cart = []
		temp = num_items # Keep track of how many items left to add to shopping_cart
		#Populate the shopping cart.
		while(temp > 0):
			if (len(catalog['results']) == 1):
				shopping_cart.append(catalog['results'][0])
			elif(len(catalog['results']) > 1):
				shopping_cart.append(catalog['results'][0])
				del catalog['results'][0]
			temp = temp - 1
		# Print the cart so it looks nice :D			
		printCart(shopping_cart)
		combos_printed = combos_printed + 1


# ENTRY POINT
getCombos(DESIRED_DOLLAR_AMOUNT, NUMBER_OF_DESIRED_PRODUCTS)

#Unused:
# def binary_search(catalog, cost, left, right):
# 	mid = left + ((right - left) / 2)	
# 	if(catalog[mid] == cost or left >= right):
# 		return mid
# 	elif(catalog[mid] > cost): # Search LEFT half
# 		return binary_search(catalog, cost, left, mid)
# 	else: # Search RIGHT half
# 		return binary_search(catalog, cost, mid + 1, right)

