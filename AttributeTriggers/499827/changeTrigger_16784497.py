Expense_Cont=Product.GetContainerByName('Staging_and_Integration_Expense_Cont')
Expense_Cont.Rows.Clear()
a = Product.Attr('Staging_and_Integration_Floor_Area_Unit').GetValue()
if a == 'Square Feet':
    b1 = SqlHelper.GetList('Select COLUMN_1 from STAGING_INTEGRATION_CONT where Type='Expense' and COLUMN_1  != 'Integration Floor Space-Sq Meter'')

    for i in b1:
        j = Expense_Cont.AddNewRow()
        j['Expense_Type'] = i.COLUMN_1
elif a == 'Square Meter':
    b2 = SqlHelper.GetList('Select COLUMN_1 from STAGING_INTEGRATION_CONT where Type='Expense' and COLUMN_1  != 'Integration Floor Space-Sq Feet'')
    for i in b2:
        j = Expense_Cont.AddNewRow()
        j['Expense_Type'] = i.COLUMN_1
ScriptExecutor.Execute('PS_Staging_Integration_Expense_Calculation')