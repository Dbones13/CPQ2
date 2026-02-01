def getFloatTPA(v):
    if v == "NA":
        return 0
    if v:
        return float(v)
    return 0

def getContainer(conName):
    return Product.GetContainerByName(conName)
TPAcon = getContainer("TPA_Third_Party_Items_Cont")
for row in TPAcon.Rows:
    if row["WriteIn"] not in ['Large screen display 4K 55" with table mount','Extended warranty for servers']:
        if (int(getFloatTPA(row['Calculated_Qty2']))) == 0:
            row['Adjusted_Qty'] = '0'
        row['Final_Qty'] = str(int(getFloatTPA(row['Calculated_Qty2']) + getFloatTPA(row['Adjusted_Qty'])))
        if (int(row['Final_Qty'])) < 0 :
            row['Adjusted_Qty'] = '0'
            row['Final_Qty'] = str(int(getFloatTPA(row['Calculated_Qty2'])))
        else:
            row['Final_Qty'] = str(int(getFloatTPA(row['Calculated_Qty2']) + getFloatTPA(row['Adjusted_Qty'])))
    else:
        row['Final_Qty'] = str(int(getFloatTPA(row['Calculated_Qty2']) + getFloatTPA(row['Adjusted_Qty'])))
        if (int(row['Final_Qty'])) < 0:
            row['Adjusted_Qty'] = '0'
            row['Final_Qty'] = str(int(getFloatTPA(row['Calculated_Qty2'])))
        else:
            row['Final_Qty'] = str(int(getFloatTPA(row['Calculated_Qty2']) + getFloatTPA(row['Adjusted_Qty'])))