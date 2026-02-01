#Update the Existing Line Items
def importLineItems(Quote,excelValues,writeInObj):
    for key,val in excelValues.items():
        values = val.split('~')
        if str(values[17]) == 'No':
            itemUpdate(Quote,key,values)
        else:
            writeInProductQuery = SqlHelper.GetFirst("SELECT PRODUCT,CATEGORY,DESCRIPTION, PRODUCTLINE, PRODUCTLINEDESCRIPTION, PRODUCTLINESUBGROUPDESCRIPTION, PRODUCTLINESUBGROUP, UNITOFMEASURE, UNITLISTPRICE, UNITREGIONALCOST FROM WRITEINPRODUCTS WHERE CATEGORY='CCC' AND PRODUCT = '{}'".format(str(values[0])))
            if writeInProductQuery is not None:
                WriteInItem = writeInObj[key]
                WriteInItem.Attr('Writein_Category').SelectValue(writeInProductQuery.CATEGORY)
                WriteInItem.Attr('WriteInProductsChoices').SelectValue(writeInProductQuery.PRODUCT)
                WriteInItem.Attr('Selected_WriteIn').AssignValue(writeInProductQuery.PRODUCT)
                WriteInItem.Attr('Description').AssignValue(writeInProductQuery.DESCRIPTION)
                WriteInItem.Attr('Product Line').AssignValue(writeInProductQuery.PRODUCTLINE)
                WriteInItem.Attr('Product Line Description').AssignValue(writeInProductQuery.PRODUCTLINEDESCRIPTION)
                WriteInItem.Attr('Product line sub group').AssignValue(writeInProductQuery.PRODUCTLINESUBGROUP)
                WriteInItem.Attr('PLSG description').AssignValue(writeInProductQuery.PRODUCTLINESUBGROUPDESCRIPTION)
                WriteInItem.Attr('Unit of Measure').AssignValue(writeInProductQuery.UNITOFMEASURE)
                WriteInItem.Attr('ItemQuantity').AssignValue(str(values[1]))
                WriteInItem.Attr('Price').AssignValue(str(values[5]))
                WriteInItem.Attr('cost').AssignValue(str(values[4]))
                #WriteInItem.Attr('Extended Description').AssignValue(str(values[14]))
                WriteInItem.AddToQuote(int(values[1]))
                itemUpdate(Quote,key,values)

#Delete the existing line items for CCC
def deleteLineItems(Quote):
    for item in Quote.MainItems:
        item.Delete()

#Trigger RePrice function
def reprice(Quote):
    for action in Quote.Actions:
        if action.Name == "Reprice" and action.IsPrimaryAction:
            Quote.ExecuteAction(action.Id)
            break

#Item Update Function
def itemUpdate(Quote,key,values):
    item = Quote.GetItemByQuoteItem(key)
    item.MrcCost = float(values[3])
    item['QI_Project_Price_Adjustment_Percent'].Value = float(values[5])
    item['QI_Frame_Discount_Percent'].Value = float(values[6])
    item['QI_Service_Discount_Percent'].Value = float(values[7])
    item['QI_Regional_Discount_Percent'].Value = float(values[8])
    item['QI_Business_Discount_Percent'].Value = float(values[9])
    item['QI_Application_Discount_Percent'].Value = float(values[10])
    item['QI_Defect_Discount_Percent'].Value = float(values[11])
    item['QI_Competitive_Discount_Percent'].Value = float(values[12])
    item['QI_Other_Discount_Percent'].Value = float(values[13])
    item['QI_Additional_Discount_Percent'].Value = float(values[13])
    item['QI_Solution_CCC'].Value = str(values[14])
    item['QI_Package_CCC'].Value = str(values[15])