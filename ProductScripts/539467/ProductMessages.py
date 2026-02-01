m = []
Product.Attr('Incomplete_Flag').AssignValue('')
Product.Attr('Product_Message').AssignValue('')
def populateMessage(row,i,message):
    if Product.Messages.Contains(message):
        Product.Attr('Incomplete_Flag').AssignValue('1')
        row.Product.Attr('Incomplete_Flag').AssignValue('1')
        return
    Product.Attr('Incomplete_Flag').AssignValue('1')
    m.append("Row[{}]: {}".format(i,message))
    #Product.Attr('Product_Message').AssignValue("Row[{}], {}".format(i,message))
    row.Product.Attr('Incomplete_Flag').AssignValue('1')
    row.Product.Attr('Product_Message').AssignValue(message)
    #Log.Info(message)

packageContainerName = "WriteInProduct"
packageContainer = Product.GetContainerByName(packageContainerName)
i=0
try:
    for row in packageContainer.Rows:
        i +=1
        data = row.Product.Attr("Selected_WriteIn").GetValue()
        data_quantity = row.Product.Attr("ItemQuantity").GetValue() if row.Product.Attr("ItemQuantity").GetValue() else 0
        data_price = row.Product.Attr("Price").GetValue() if row.Product.Attr("Price").GetValue() else 0
        data_unit = row.Product.Attr("Unit of Measure").GetValue()
        WriteIn_LP_Valid = SqlHelper.GetFirst("Select * From WriteIn_ListPriceValidation Where Product = '"+data+"'")
        if data == '' or data == "Product":
            populateMessage(row, i,"WriteInProducts is not Valid")
        elif int(float(data_quantity)) <= 0:
            populateMessage(row, i,"Quantity is not Valid")
        elif int(float(data_price)) < 0:
            populateMessage(row, i,"Unit List Price is not Valid")
        elif WriteIn_LP_Valid is not None:
            if float(data_price) <= float(WriteIn_LP_Valid.MinimumListPrice) or float(data_price) > float(WriteIn_LP_Valid.MaximumListPrice):
                populateMessage(row, i,"List Price not in range")
        elif data.strip() == "":
            populateMessage(row, i,"Unit of Measure is not Valid")
        else:
            row.Product.Attr('Incomplete_Flag').AssignValue('')
            row.Product.Attr('Product_Message').AssignValue('')
except Exception, e:
    Log.Write("WriteIn::ProductMessages::Exception: {}".format(str(e)))
j = ""
for n in m:
    j+= str(n)+ " , "
j = j[0:len(j)-2]
Product.Attr('Product_Message').AssignValue(j)