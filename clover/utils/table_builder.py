
def addZero(l,typeOfTable):
	if l is None:
		return None 
	if typeOfTable == "fix":
		amount = "fixedAmt"
	elif typeOfTable == "var":
		amount = "expAmt"
	else:
		amount = ""
		print "Error in param"
		return

	retlist = []
	for d in l:
		print "Dict"
		print d
		print "Dict amount"
		print d[amount]
		d[amount] = '${:,.2f}'.format(float(d[amount]))
		retlist.append(d)
	return retlist