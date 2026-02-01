def populateRenewalTable(quoteid,product,details,date,quotetype,SystemID,rowID):
    tableInfo = SqlHelper.GetTable("SC_Renewal_Table")
    tablerow = {"QuoteID" : quoteid, "Product" : product, "ProductDetails" : details, "Date" : date, "QuoteType" : quotetype, "SystemID": SystemID, "LaborRowID":rowID}
    tableInfo.AddRow(tablerow)
    SqlHelper.Upsert(tableInfo)

def readContainer(att):
    contList = []
    cont = row.Product.GetContainerByName(str(att.Name))
    if cont.Rows.Count:
        for row1 in cont.Rows:
            insidecont = {}
            for col in row1.Columns:
                if col.DisplayType == "SelectorCheckBox":
                    insidecont[col.Name] = str(row1.IsSelected)
                else:
                    insidecont[col.Name] = row1[col.Name]
            contList.append(insidecont)
    return contList
def readContainerlabor(att):
    contList = []
    cont = row2.Product.GetContainerByName(str(att.Name))
    if cont.Rows.Count:
        for row3 in cont.Rows:
            insidecont = {}
            for col in row3.Columns:
                if col.DisplayType == "SelectorCheckBox":
                    insidecont[col.Name] = str(row3.IsSelected)
                else:
                    insidecont[col.Name] = row3[col.Name]
            contList.append(insidecont)
    return contList

def populateRenewalQuoteLineTable(quoteid,details,date,product,quotetype):
    tableInfo = SqlHelper.GetTable("CT_SC_Renewal_Quote_Table")
    tablerow = {"QuoteID" : quoteid, "QuoteDetails" : details, "Date" : date, "Product" : product, "QuoteType" : quotetype}
    tableInfo.AddRow(tablerow)
    SqlHelper.Upsert(tableInfo)

def quoteLine(item):
    quoteDict = {}
    quoteDict = {"LastChildType" : item.PartNumber, "LastChild" : item.Description, "Escalation" : str(item.QI_SC_Escalation_Percent.Value) , "ListPrice" : str(item.ExtendedListPrice), "MPADiscount" : str(item.QI_MPA_Discount_Percent.Value), "OtherDiscount" : str(item.QI_Additional_Discount_Percent.Value), "TotalDiscount" : str(item.QI_SC_Total_Discount_Percent.Value), "TotalDiscountPrice" : item.QI_SC_Total_Discount_Price.Value, "SellPrice" : str(item.ExtendedAmount), "Margin" : str(item.QI_SC_Margin_Percent.Value), "Cost_Price" : str(item.QI_SC_Cost.Value) ,"CostPrice" : str(item.ExtendedCost), "ScopeImpact" : item.QI_SC_Scope_Impact.Value}
    return quoteDict

def findparentkey(item,guid,xkey):
    parent = Quote.GetItemByUniqueIdentifier(guid)
    if parent.ProductName == "Year":
        xkey = parent.PartNumber + '|' + xkey
        return xkey,item.PartNumber
    else:
        xkey = parent.Description + '|' + xkey
        return findparentkey(parent,parent.ParentItemGuid,xkey)

quoteNumber = "{}{}".format(Quote.CompositeNumber, "-{}".format(Quote.RevisionNumber) if Quote.RevisionNumber>0 else '')
from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')
detailsList = []
StrModcol = ''
quotetype = Quote.GetCustomField("Quote Type").Content

if quotetype in ('Contract New','Contract Renewal'):

    primaryQueryItems = SqlHelper.GetList("select CpqTableEntryId from SC_RENEWAL_TABLE where QuoteID = '{}'".format(quoteNumber))
    tableInfo = SqlHelper.GetTable("SC_RENEWAL_TABLE")
    for primaryItem in primaryQueryItems:
        tableInfo.AddRow(primaryItem)
    SqlHelper.Delete(tableInfo)

    primaryQueryQuoteItems = SqlHelper.GetList("select CpqTableEntryId from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{}'".format(quoteNumber))
    tableQuoteInfo = SqlHelper.GetTable("CT_SC_RENEWAL_QUOTE_TABLE")
    for primaryItem in primaryQueryQuoteItems:
        tableQuoteInfo.AddRow(primaryItem)
    SqlHelper.Delete(tableQuoteInfo)

    selected_attrs_json = {}
    for item in Quote.MainItems:
        if item.QI_SC_ItemFlag.Value == 'Hidden':
            selected_Attrs = []
            for attr in item.SelectedAttributes:
                selected_Attrs.append(attr.Name)
            selected_attrs_json[item.ProductName] = selected_Attrs

    for item in Quote.MainItems:
        if item.ProductName == "Service Contract Products":
            item.EditConfiguration()
            for row in Product.GetContainerByName("Service Contract Modules").Rows:
                detailsList = []
                for att in row.Product.Attributes:
                    if att.Name in selected_attrs_json[row.Product.Name]:
                        try:
                            dis = row.Product.Attributes.GetByName(str(att.Name)).DisplayType
                        except:
                            dis = "Container"
                        if dis in ["DropDown","FreeInputNoMatching","CheckBox","AutoCompleteCustomTable","ListBoxMultipleSelect"]:
                            value = row.Product.Attr(str(att.Name)).GetValue()
                            detailsList.append({"Name":str(att.Name),"Type":dis,"Value":value})
                        elif dis == "Container":
                            value = readContainer(att)
                            detailsList.append({"Name":str(att.Name),"Type":"Container","Value":value})
                StrModcol = str(row["Module"])
                if row["Module"] == 'Generic Module':
                	StrModcol = str(row["Product_Name"])
                #populateRenewalTable(quoteNumber,str(row["Module"]),str(detailsList),date,quotetype,row.Product.SystemId,"")
                populateRenewalTable(quoteNumber,StrModcol,str(detailsList),date,quotetype,row.Product.SystemId,"")
                if row['Module'] == 'Labor':
                    detailsList = []
                    for row2 in row.Product.GetContainerByName("SC_Labor_Summary_Container").Rows:
                        for att in row2.Product.Attributes:
                            if True:   #selected attributes condition to be added
                                try:
                                    dis = row2.Product.Attributes.GetByName(str(att.Name)).DisplayType
                                except:
                                    dis = "Container"
                                if dis in ["DropDown","FreeInputNoMatching","CheckBox","AutoCompleteCustomTable","ListBoxMultipleSelect"]:
                                    value = row2.Product.Attr(str(att.Name)).GetValue()
                                    detailsList.append({"Name":str(att.Name),"Type":dis,"Value":value})
                                elif dis == "Container":
                                    value = readContainerlabor(att)
                                    detailsList.append({"Name":str(att.Name),"Type":"Container","Value":value})
                        populateRenewalTable(quoteNumber,'Labor Deliverables',str(detailsList),date,quotetype,row2.Product.SystemId,row2.RowIndex)


            break

    prodDict = {}

    for item in Quote.MainItems:
        xkey = ""
        if (item.QI_SC_ItemFlag.Value != "0000" and item.QI_SC_ItemFlag.Value != "00000" and item.QI_SC_ItemFlag.Value != "Hidden") or (len(list(item.Children)) == 0 and item.QI_SC_ItemFlag.Value != "Hidden") or item.PartNumber == 'Other cost details':
            xkey = item.Description
            value = quoteLine(item)
            key,product = findparentkey(item,item.ParentItemGuid,xkey)
            if product not in prodDict.keys():
                prodDict[product] = {key:value}
            else:
                prodDict[product][key] = value
    for i in prodDict:
        populateRenewalQuoteLineTable(quoteNumber,str(prodDict[i]),date,i,quotetype)