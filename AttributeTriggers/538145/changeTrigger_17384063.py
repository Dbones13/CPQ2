SC_Central_Managed_SQL = Product.Attr('SC_Central_Managed_SQL').GetValue()
if SC_Central_Managed_SQL == "Yes":
    Product.Attr('SC_Standard_User_CALs').Access = AttributeAccess.ReadOnly
else:
    Product.Attr('SC_Standard_User_CALs').Access = AttributeAccess.Editable