def getFloat(var):
    try:
        return float(var)
    except:
        return 0

tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Part Summary' in tabs:
    cont = Product.GetContainerByName('Terminal_PartSummary_Cont')
    for row in cont.Rows:
        row.Calculate()
        row['Final_Quantity'] = str(getFloat(row['Part_Qty']) + getFloat(row['Adj_Quantity']))
    cont.Calculate()