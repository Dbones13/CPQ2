Product.Attr('Incomplete_Flag').AssignValue('')
def populateMessage(message):
    if Product.Messages.Contains(message):
        Product.Attr('Incomplete_Flag').AssignValue('1')
        return
    Product.Attr('Incomplete_Flag').AssignValue('1')
    Product.Attr('Product_Message').AssignValue(message)
    Log.Info(message)

try:
	data = Product.Attr("Selected_WriteIn").GetValue()
	itemQuantity = Product.Attr("ItemQuantity").GetValue() if Product.Attr("ItemQuantity").GetValue() else 0
	price = Product.Attr("Price").GetValue() if Product.Attr("Price").GetValue() else 0
	cost = Product.Attr("cost").GetValue() if Product.Attr("cost").GetValue() else 0
	unitOfMeasure = Product.Attr("Unit of Measure").GetValue()
	if data == '' or data == "Product":
		populateMessage("WriteInProducts is not Valid")
	elif int(float(itemQuantity)) <= 0:
		populateMessage("Quantity is not Valid")
	elif int(float(price)) < 0:
		populateMessage("Unit List Price is not Valid")
	elif int(float(cost)) < 0:
		populateMessage("Unit Regional Cost is not Valid")
	elif unitOfMeasure.strip() == "":
		populateMessage("Unit of Measure is not Valid")
except Exception, e:
    Log.Write("WriteIn::ProductMessages::Exception: {}".format(str(e)))