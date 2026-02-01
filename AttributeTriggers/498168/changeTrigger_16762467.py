count = 1
def populateInputs(cont):
    Trace.Write('Added 1')
    query = SqlHelper.GetList("select * from TRAVEL_LIVING_CONT where Condition ='Inputs'")
    for j in query:
        newRow=cont.AddNewRow(False)
        newRow['Input'] = j.Column_1
        newRow['Value'] = j.Column_2
    cont.Calculate()
def populateExpense(cont):
    Trace.Write('Added 1')
    query = SqlHelper.GetList("select * from TRAVEL_LIVING_CONT where Condition ='Expense'")
    for j in query:
        newRow=cont.AddNewRow(False)
        newRow['Expense_Type'] = j.Column_1
        newRow['Unit'] = j.Column_2
        newRow['Final_Quantity']= '0'
        newRow['Unit_Cost'] = '0'
        newRow['Total_Cost'] = '0'
        newRow['Unit_List_Price'] = '0'
        newRow['Total_List_Price'] = '0'
        if newRow['Expense_Type'] == 'Guest House Lodging Expense':
            newRow['Quantity'] = str(0)
            newRow['Final_Quantity'] = newRow['Quantity']
        if newRow['Expense_Type'] == 'Total':
            newRow['Quantity'] = str(0)
            newRow['Final_Quantity'] = str(0)
    cont.Calculate()
groups_count=Product.Attr('TL_Number_of_Travel_Expense_Groups').GetValue()
if groups_count != '':
    groups_count=int(groups_count)
    for i in range(1,groups_count+1):
        cont_name='TL_Inputs_'+str(i)
        cont=Product.GetContainerByName(cont_name)
        exp_cont_name='TL_Expense_Calculation_Cont_'+str(i)
        exp_cont=Product.GetContainerByName(exp_cont_name)
        count = i
        if cont.Rows.Count == 0:
            populateInputs(cont)
        if exp_cont.Rows.Count == 0:
            populateExpense(exp_cont)
for i in range(count+1,11):
    cont_name='TL_Inputs_'+str(i)
    cont=Product.GetContainerByName(cont_name)
    exp_cont_name='TL_Expense_Calculation_Cont_'+str(i)
    exp_cont=Product.GetContainerByName(exp_cont_name)
    if cont:
        cont.Clear()
    if exp_cont:
        exp_cont.Clear()