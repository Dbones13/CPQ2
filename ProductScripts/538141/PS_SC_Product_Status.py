#Product.Attr('SC_Product_Status').AssignValue("0")
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    Product.Attr('SC_Product_Status').AssignValue("1")
    if "QCS 4.0" not in Product.Attr('SC_ScopeRemoval').GetValue():
        new_value = Product.Attr('SC_QCS_Number of Machines').GetValue()
        Product.Attr('Backup_SC_QCS_Number_of_Machines').AssignValue(new_value)
    if "QCS Support Center" not in Product.Attr('SC_ScopeRemoval').GetValue():
        new_value1 = Product.Attr('SC_QCS_No_Of_Machines').GetValue()
        Product.Attr('Backup_SC_QCS_No_of_Machines').AssignValue(new_value1)