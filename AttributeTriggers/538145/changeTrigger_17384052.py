SC_Central_Managed_SQL_PY = Product.Attr('SC_Central_Managed_SQL_PY').GetValue()
if SC_Central_Managed_SQL_PY == "Yes":
    Product.Attr('SC_Standard_User_CALs_PY').Access = AttributeAccess.ReadOnly
else:
    Product.Attr('SC_Standard_User_CALs_PY').Access = AttributeAccess.Editable