from System.Collections.Specialized import OrderedDictionary
import GS_GetPriceFromCPS

def checkingChangeinP1P2(cont,Pole,flag,serProd,itemsToBeDeleted,elementsList):
    if cont.Rows.Count:
        for row in cont.Rows:
            query = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(row["Part_Number"],Pole))
            if query is not None:
                if query.PartStatus != row["Part_Status"] or query.Replacement_Status != row["Replacement_Status"] or query.Replacement_Part != row["Replacement_Part"]:
                    flag = True
                    itemsToBeDeleted.append(row.RowIndex)
                    serProd[row["Service_Product"]+"|"+row["Part_Number"]] = {}
                    for col in row.Columns:
                        serProd[row["Service_Product"]+"|"+row["Part_Number"]][col.Name] = row[col.Name]
            else:
                if row["Part_Status"] != "" or row["Replacement_Status"] != "" or row["Replacement_Part"] != "":
                    flag = True
                    itemsToBeDeleted.append(row.RowIndex)
                    serProd[row["Service_Product"]+"|"+row["Part_Number"]] = {}
                    for col in row.Columns:
                        serProd[row["Service_Product"]+"|"+row["Part_Number"]][col.Name] = row[col.Name]
            elementsList.append(row["Service_Product"]+"|"+row["Part_Number"])
    return flag,serProd,itemsToBeDeleted,elementsList

def addNewLineItem(newrow,cont,replacementPart):
    if str(newrow["Service_Product"]+"|"+replacementPart) not in elementsList:
        Trace.Write(replacementPart)
        query = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(str(replacementPart),Pole))
        Trace.Write(query.PartStatus)
        if query is not None:
            if query.PartStatus == "Active":
                newrowadded = cont.AddNewRow(False)
                newrowadded.GetColumnByName("Service_Product").SetAttributeValue(newrow["Service_Product"])
                newrowadded["Service_Product"] = newrow["Service_Product"]
                newrowadded["Part_Number"] = replacementPart
                newrowadded["Part_Status"] = query.PartStatus
                desc = SqlHelper.GetFirst("SELECT PRODUCT_NAME FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE = '{}'".format(replacementPart))
                newrowadded["Description"] = desc.PRODUCT_NAME if desc is not None else ""
                newrowadded["Qty"] = newrow["Hidden_Quantity"]
                newrowadded["Replacement_Status"] = query.Replacement_Status
                newrowadded["Replacement_Part"] = query.Replacement_Part
                newrowadded["PY_Quantity"] = '0'
                newrowadded["CY_Quantity"] = newrow["Hidden_Quantity"]
                newrowadded["PY_UnitPrice"] = '0'
                newrowadded["PY_ExtPrice"] = '0'
                newrowadded["Hidden_Quantity"] = newrow["Hidden_Quantity"]
                priceDict = GS_GetPriceFromCPS.getPrice(Quote,{},[replacementPart],TagParserQuote,Session)
                newrowadded["Unit_Price"] = priceDict[replacementPart] if len(priceDict)>0 else '0'
                newrowadded["Ext_Price"] = str(float(newrow["Hidden_Quantity"])*float(newrowadded["Unit_Price"])) if newrow["Hidden_Quantity"] else '0'
                newrowadded["Hidden_ListPrice"] = newrowadded["Ext_Price"]
                newrowadded["CY_ExtPrice"] = newrowadded["Ext_Price"]
                newrowadded["Comments"] = "Scope Addition" if float(newrow["Hidden_Quantity"])>0 else "No Scope Change"
                newrowadded.Calculate()


def writeContainer(cont,serProd,elementsList,key,Pole):
    if True:
        newlineItem = False
        query = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(serProd[key]["Part_Number"],Pole))
        if query is not None:
            if query.Replacement_Status == "Direct replacement" and serProd[key]["Service_Product"] == "Parts Holding P2":
                newlineItem = True
        newrow = cont.AddNewRow(False)
        for col in newrow.Columns:
            if col.Name == "Part_Status":
                newrow[col.Name] = query.PartStatus if query is not None else ""
            elif col.Name == "Replacement_Status":
                newrow[col.Name] = query.Replacement_Status if query is not None else ""
            elif col.Name == "Replacement_Part":
                newrow[col.Name] = query.Replacement_Part if query is not None else ""
            elif col.DisplayType == "DropDown":
                newrow.GetColumnByName(col.Name).SetAttributeValue(serProd[key][col.Name])
                newrow[col.Name] = serProd[key][col.Name]
            else:
                newrow[col.Name] = serProd[key][col.Name]
        if newlineItem == True:
            addNewLineItem(newrow,cont,query.Replacement_Part)
            newrow["Qty"] = '0'
            newrow["CY_Quantity"] = "0"
            newrow["Hidden_Quantity"] = "0"
        newrow.Calculate()

try:
    Pole = Quote.GetCustomField("Pole").Content
    BookingCountry = Quote.GetCustomField("Booking Country").Content
except:
    BookingCountry = ""
    Pole = ""
if Pole == "APAC":
    if BookingCountry == "japan":
        Pole = "JP"
    elif BookingCountry != "":
        Pole = "SG"
flag = False
cont = Product.GetContainerByName("SC_P1P2_Parts_Details")
serProd = OrderedDictionary()
elementsList = []
itemsToBeDeleted = []

checker,serProd,itemsToBeDeleted,elementsList = checkingChangeinP1P2(cont,Pole,flag,serProd,itemsToBeDeleted,elementsList)
itemsToBeDeleted.reverse()
for i in itemsToBeDeleted:
    cont.DeleteRow(i)
if checker == True:
    for key in serProd.Keys:
        writeContainer(cont,serProd,elementsList,key,Pole)

Product.Attr('SC_Product_Status').AssignValue("0")
ScriptExecutor.Execute('P1P2_Part_Details_ErrorMessage')