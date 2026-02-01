attr = Product.Attr("WriteInProductsChoices")
if attr.SelectedValue:
    val = attr.SelectedValue.Display
    Product.Attr("Selected_WriteIn").AssignValue(val)

Product.Attr('Incomplete_Flag').AssignValue('')
Product.Attr('Product_Message').AssignValue('')

def populateMessage(message):
    if Product.Messages.Contains(message):
        Product.Attr('Incomplete_Flag').AssignValue('1')
        return
    Product.Attr('Incomplete_Flag').AssignValue('1')
    Product.Attr('Product_Message').AssignValue(message)
    #Log.Info(message)

itemQuantity = Product.Attr("ItemQuantity").GetValue() if Product.Attr("ItemQuantity").GetValue() else 0
price = Product.Attr("Price").GetValue() if Product.Attr("Price").GetValue() else 0
#cost = Product.Attr("cost").GetValue() if Product.Attr("cost").GetValue() else 0
unitOfMeasure = Product.Attr("Unit of Measure").GetValue()
data = Product.Attr("Selected_WriteIn").GetValue()
WriteIn_LP_Valid = SqlHelper.GetFirst("Select * From WriteIn_ListPriceValidation Where Product ='"+data+"'")

if Product.Attr("Selected_WriteIn").GetValue() == "" or  Product.Attr("Selected_WriteIn").GetValue() == "Product":
    populateMessage('WriteInProducts is not Valid')
elif int(float(itemQuantity)) <= 0:
    populateMessage('Quantity is not Valid')
elif int(float(price)) < 0:
	populateMessage('Unit List Price is not Valid')
elif WriteIn_LP_Valid is not None:
    if float(price)<float(WriteIn_LP_Valid.MinimumListPrice) or float(price)>float(WriteIn_LP_Valid.MaximumListPrice):
         populateMessage("Unit List Price not in Range")
elif unitOfMeasure.strip() == "":
    populateMessage("Unit of Measure is not Valid")
else:
    Product.Attr('Incomplete_Flag').AssignValue('')
    Product.Attr('Product_Message').AssignValue('')