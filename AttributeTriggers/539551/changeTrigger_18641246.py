if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
    if Product.Attr('Sell Price Strategy').SelectedValue.Display == 'Customer Budget':
        Product.Attr('Customer_Budget_TextField').Access = AttributeAccess.Editable
        Product.Attr('Customer_Budget_TextField').Required = True
    else:
        Product.Attr('Customer_Budget_TextField').AssignValue('')
        Product.Attr('Customer_Budget_TextField').Access = AttributeAccess.Hidden
        Product.Attr('Customer_Budget_TextField').Required = False