import ProductUtil

Product.Attr("Incomplete").AssignValue("")
for attr in Product.Attributes:
    if attr.DisplayType == 'Container' or attr.Name in ["Group Number" , "Release" , "Controller Type" , "ELEPIU Library Required"]:
        continue
    if attr.GetValue() != '':
        break
else:
    ProductUtil.addMessage(Product,'Please enter a valid value in atleast a field')
    Product.Attr("Incomplete").AssignValue("1")