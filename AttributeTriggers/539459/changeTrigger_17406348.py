#Base_SM_Product_Name = "Safety Manager {}".format(Product.GetContainerByName('SM_Application_Hardware_Cont').Rows[0].GetColumnByName('Application').Value)
if Product.Attr('SM_Product_Name').GetValue() != Product.Name:
    Product.GetContainerByName('SM_SSE_Engineering_Labor_Container').Rows.Clear()
    Product.DisallowAttr('SM_SSE_Engineering_Labor_Container')
else:
    Product.AllowAttr('SM_SSE_Engineering_Labor_Container')