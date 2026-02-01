MultiYear = Product.Attr('LCM_MultiYear_Project').GetValue()
if MultiYear == "No":
    Product.DisallowAttr('LCM_Multiyear_Selection')