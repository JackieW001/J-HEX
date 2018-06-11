


# entertainment = {}, eatOut = {}, shop = {}, misc = {}, grocery = {}, event
def addZero(l,typeOfTable):
	retlist = []


	if l is None:
		return None 

	if typeOfTable == "fix":
		amount = "fixedAmt"
		for d in l:
			tempd = {}
			for key in d:
				if key == amount:
					tempd[amount] = '${:,.2f}'.format(float(d[amount]))
				elif key == 'fixedType':
					tempd['fixedType'] = d['fixedType'].title()

				else:
					tempd[key] = d[key]

			#print tempd
			retlist.append(tempd)

	elif typeOfTable == "var":
		amount = "expAmt"
		for d in l:
			tempd = {}
			for key in d:
				if key == amount:
					tempd[amount] = '${:,.2f}'.format(float(d[amount]))
				elif key == 'expType':
					if d['expType'] == 'eatOut':
						tempd['expType'] = 'Dining Out'
					elif d['expType'] == 'entertainment':
						tempd['expType'] = 'Entertainment'
					elif d['expType'] == 'shop':
						tempd['expType'] = 'Shopping'
					elif d['expType'] == 'misc':
						tempd['expType'] = 'Miscellaneous'	
					elif d['expType'] == 'grocery':
						tempd['expType'] = 'Grocery'
					elif d['expType'] == 'event':
						tempd['expType'] = 'Event'
				else:
					tempd[key] = d[key]

			#print tempd
			retlist.append(tempd)





	else:
		amount = ""
		print "Error in param"
		return

	return retlist