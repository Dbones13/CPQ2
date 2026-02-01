# APPROVAL RULES FOR SPOT LABOR
def isLevel1Spot(total,percent):
	return (total < 25000.00 and (percent>5.00 and percent<=10.00)) or ((total>=25000.00 and total<100000.00) and percent<=5.00)

def isLevel2Spot(total,percent):
	return (total < 25000 and percent>10) or (total >= 25000 and total < 100000 and percent > 5 and percent <= 25) or (total >= 100000 and total < 250000 and percent <= 5)

def isLevel3Spot(total,percent):
	return (total >= 25000 and total < 250000 and percent > 25) or (total >= 100000 and total < 500000 and percent > 5 and percent <= 25) or (total >= 250000 and percent <=5)

def isLevel4Spot(total,percent):
	return (total >=250000 and percent > 25) or (total >= 500000 and percent >5)


# APPROVAL RULES FOR PMC
def isLevel1PMC(total,percent):
	return (total <= 50000.00 and percent <= 60)

def isLevel2PMC(total,percent):
	return (total > 50000 and total <= 1000000 and percent <= 45) or (total > 50000 and total <= 500000 and percent > 45 and percent <= 60) or (total <= 50000 and percent > 60 and percent <= 75)

def isLevel3PMC(total,percent):
	return (total > 1000000 and percent <= 45) or (total > 500000 and total <= 1000000 and percent > 45 and percent <= 60) or (total > 50000 and total <= 1000000 and percent > 60 and percent <= 75) or (total <= 500000 and percent > 75 and percent <= 80) or (total <= 200000 and percent > 80 and percent <= 84)

def isLevel4PMC(total,percent):
	return (total > 1000000 and percent > 45 and percent <= 75) or (total > 500000 and total <= 5000000 and percent > 75 and percent <= 80) or (total > 200000 and total <= 5000000 and percent > 80 and percent <= 84) or (total <= 5000000 and percent > 84)

def isLevel5PMC(total,percent):
	return (total > 5000000 and percent > 75)

# Main function to determine max approval level required
def getMaxApprovalLevel(total,percent,quoteType,lob):
	if quoteType == "Parts and Spot" and lob == "PMC":
		if isLevel1PMC(total,percent):
			return 1
		if isLevel2PMC(total,percent):
			return 2
		if isLevel3PMC(total,percent):
			return 3
		if isLevel4PMC(total,percent):
			return 4
		if isLevel5PMC(total,percent):
			return 5
	elif quoteType == "Parts and Spot" and lob == "LSS":
		if isLevel1Spot(total,percent):
			return 1
		if isLevel2Spot(total,percent):
			return 2
		if isLevel3Spot(total,percent):
			return 3
		if isLevel4Spot(total,percent):
			return 4
	else:
		return 0