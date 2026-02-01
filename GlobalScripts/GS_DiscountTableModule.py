def clearTable(table):
	table.Rows.Clear()
	if table.Rows.Count > 0:
		for rows in table.Rows:
			rowID = rows.rowId
			table.DeleteRow(rowId)

	return table

def getTotalCost(productsList):
	cost = [j.ExtendedCost for j in productsList if not j.IsOptional]
	return sum(cost)

def getTotalListPrice(productsList):
	totalListPrice = [i.QI_ExtendedListPrice.Value for i in productsList if not i.IsOptional]
	return sum(totalListPrice)

def getTotalNonAdhocListPrice(productsList):
	nonAdhoc = [j.QI_ExtendedListPrice.Value for j in productsList if not j.IsOptional and j.ProductName != "WriteIn"]
	return sum(nonAdhoc)

def getTotalAdhocSellPrice(productsList):
	adhoc = [k.ExtendedAmount for k in productsList if not k.IsOptional and k.ProductName == "WriteIn"]
	return sum(adhoc)

def checkStatus(status):
	return status == 32 or status == 39