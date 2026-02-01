def getFloat(var):
    if var:
        return float(var)
    return 0

def addvalues(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def getCFValue(name):
    return Quote.GetCustomField(name).Content

def getQuoteTable(name):
    return Quote.QuoteTables[name]

salesArea = getCFValue('Sales Area')
projectType = getCFValue('EGAP_Project_Type')
productLineTable = getQuoteTable('Product_Line_Details')
lineIemTable = getQuoteTable('QT_PROJECT_BOOKING_LINE_ITEM_DETAILS')
quoteDetailsTable = getQuoteTable('Quote_Details')
bookingCountry = getCFValue("Booking Country").lower()
bookingLob = getCFValue("Booking LOB")
quoteType = getCFValue("Quote Type")
quoteListPrice = 0
quoteCost = 0
quoteSellPrice = 0
spliFlag = False
lineIemTable.Rows.Clear()

missingListPrice = 0
missingCost = 0
missingSellPrice = 0

for row in quoteDetailsTable.Rows:
    quoteListPrice = row['Quote_List_Price']
    if bookingCountry == 'india' and bookingLob in ('PAS','LSS') and quoteType == 'Projects':
        #quoteCost = row['India_Discounted_TP']
        Trace.Write("Indiadiscounted_tp")
    else:
        quoteCost = row['Quote_Regional_Cost']
    quoteSellPrice = row['Quote_Sell_Price']
    break

query = "Select * from Projects_SalesOrg_Part_Mapping where Project_Type = '{0}' and Sales_Org = '{1}'".format(projectType,salesArea)
res = SqlHelper.GetFirst(query)
if res is not None:
    if res.Split == '':
        addRow = lineIemTable.AddNewRow()
        addRow['Line_Item'] = res.Part
        addRow['List_Price'] = quoteListPrice
        addRow['Cost'] = quoteCost
        addRow['Sell_Price'] = quoteSellPrice
    else:
        spliFlag = True

if spliFlag:
    productLineDict = dict()
    query = SqlHelper.GetList("select * from Projects_PL_Split")
    if query is not None:
        for res in query:
            productLineDict[res.Product_Line] = res.Parent_Part
    if productLineDict:
        for row in productLineTable.Rows:
            if row["Product_Line"] in productLineDict:
                if lineIemTable.Rows.Count>0:
                    for innerrow in lineIemTable.Rows:
                        if innerrow['Line_Item']==str(productLineDict[row["Product_Line"]]):
                            innerrow['List_Price']= innerrow['List_Price']+ row["PL_List_Price"]
                            innerrow['Cost']= innerrow['Cost']+ row["PL_Regional_Cost"]
                            innerrow['Sell_Price']= innerrow['Sell_Price']+ row["PL_Sell_Price"]
                            break
                    else:
                        addRow = lineIemTable.AddNewRow()
                        addRow['Line_Item']=str(productLineDict[row["Product_Line"]])
                        addRow['List_Price'] = row["PL_List_Price"]
                        addRow['Cost'] = row["PL_Regional_Cost"]
                        addRow['Sell_Price'] = row["PL_Sell_Price"]
                else:
                    addRow = lineIemTable.AddNewRow()
                    addRow['Line_Item']=str(productLineDict[row["Product_Line"]])
                    addRow['List_Price'] = row["PL_List_Price"]
                    addRow['Cost'] = row["PL_Regional_Cost"]
                    addRow['Sell_Price'] = row["PL_Sell_Price"]
            else:
                missingListPrice=missingListPrice+row["PL_List_Price"]
                missingCost=missingCost+row["PL_Regional_Cost"]
                missingSellPrice=missingSellPrice+row["PL_Sell_Price"]

if missingListPrice !=0 or missingCost!=0 or missingSellPrice!=0:
    addRow = lineIemTable.AddNewRow()
    addRow['Line_Item']=str("HPS_PL_AMISSING")
    addRow['List_Price'] = missingListPrice
    addRow['Cost'] = missingCost
    addRow['Sell_Price'] = missingSellPrice
lineIemTable.Save()