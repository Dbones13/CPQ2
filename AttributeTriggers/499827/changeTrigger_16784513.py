Expense_Cont=Product.GetContainerByName('Staging_and_Integration_Expense_Cont')
center = Product.Attr('Staging_and_Integration_Center').GetValue()
if center == 'None':
    #Expense_Cont.Rows.Clear()
    #b2 = SqlHelper.GetList('Select COLUMN_1 from STAGING_INTEGRATION_CONT where Type='Expense' and COLUMN_1  != 'Integration Floor Space-Sq Feet'')
    for i in Expense_Cont.Rows:
        j['Unit_Cost'] = 0.00
        j['Final_Unit_Cost'] = 0.00
        j['Unit_List_Price'] = 0.00
        j['Final_Unit_List_Price'] = 0.00
        j['Total_Cost'] = 0.00
        j['Total_List_Price'] = 0.00
unit  = SqlHelper.GetFirst('SELECT Floor_Area FROM STAGING_INTEGRATION_DATA WHERE  Integration_Center = ''+center+'' and  Particular = 'Floor Space'')
if center != 'Other':
    values = Product.Attr('Staging_and_Integration_Floor_Area_Unit').Values
    for i in values:
        if i.ValueCode == unit.Floor_Area:
            i.Allowed = True
        else:
            i.Allowed = False
if center == 'Other':
     Product.Attr('Staging_and_Integration_Floor_Area_Unit').SelectValue('Square Meter')
else:
     Product.Attr('Staging_and_Integration_Floor_Area_Unit').SelectValue(unit.Floor_Area)
ScriptExecutor.Execute('PS_Staging_Integration_Expense_Calculation')