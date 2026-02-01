def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00

con = Product.GetContainerByName('UOC_PartSummary_Cont')
for row in con.Rows:
    if row["CE_Final_Quantity"] == '':
        row["CE_Final_Quantity"] = row["CE_Part_Qty"]
    else:
        val = int(getFloat(row["CE_Part_Qty"]) + getFloat(row["CE_Adj_Quantity"]))
        row["CE_Final_Quantity"] =str(val)