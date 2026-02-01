def getContainer(Name):
    return Product.GetContainerByName(Name)

Session["Scope"] = Product.Attr('MIgration_Scope_Choices').GetValue()
selectedProducts = set()
a = ''
for row in getContainer("CONT_MSID_SUBPRD").Rows:
    selectedProducts.add(row["Selected_Products"])
    a += row["Selected_Products"]
Product.Attr('MSID_Selected_Products').AssignValue(a)