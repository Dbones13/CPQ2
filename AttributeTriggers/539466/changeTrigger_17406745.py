attr = Product.Attr("WriteInProductsChoices")
if attr.SelectedValue:
    val = attr.SelectedValue.Display
    Product.Attr("Selected_WriteIn").AssignValue(val)

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
if Product.Attr("Selected_WriteIn").GetValue() == "" or  Product.Attr("Selected_WriteIn").GetValue() == "Product":
    populateMessage('WriteInProducts is not Valid')
elif int(float(itemQuantity)) <= 0:
    populateMessage('Quantity is not Valid')
#elif int(float(price)) < 0:
#populateMessage('Unit List Price is not Valid')
elif unitOfMeasure.strip() == "":
    populateMessage("Unit of Measure is not Valid")
else:
    Product.Attr('Incomplete_Flag').AssignValue('')