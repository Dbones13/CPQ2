groups_count=Product.Attr('TL_Number_of_Travel_Expense_Groups').GetValue()
if groups_count != '' and groups_count != str(1):
    groups_count=int(groups_count)
    query = SqlHelper.GetList("select Column_1,Column_2  from TRAVEL_LIVING_CONT where Condition ='Expense'")
    for i in range(2,groups_count+1):
        cont_name='TL_Expense_Calculation_Cont_'+str(i)
        cont=Product.GetContainerByName(cont_name)
        if cont.Rows.Count == 0:
            cont.Clear()
            for j in query:
                newRow=cont.AddNewRow(False)
                newRow['Expense_Type'] = j.Column_1
                newRow['Unit'] = j.Column_2
                Trace.Write(newRow['Expense_Type'])
                #cont.Calculate()
        input_cont_name='TL_Inputs_'+str(i)
        input_cont=Product.GetContainerByName(input_cont_name)
        var1= float(input_cont.Rows[0]['Value']) if input_cont.Rows[0]['Value'] != '' else 0
        var2= float(input_cont.Rows[1]['Value']) if input_cont.Rows[1]['Value'] != '' else 0
        var3= float(input_cont.Rows[2]['Value']) if input_cont.Rows[2]['Value'] != '' else 0
        var4= float(input_cont.Rows[3]['Value']) if input_cont.Rows[3]['Value'] != '' else 0
        var5= float(input_cont.Rows[4]['Value']) if input_cont.Rows[4]['Value'] != '' else 0
        var6= float(input_cont.Rows[5]['Value']) if input_cont.Rows[5]['Value'] != '' else 0
        Trace.Write(cont.Rows.Count)
        for newRow in cont.Rows:
            if newRow['Expense_Type'] == 'Air or Rail Travel Expense':
                newRow['Quantity'] = str(float(var1)*float(var2))
            elif newRow['Expense_Type'] == 'Hotel Lodging Expense':
                newRow['Quantity'] = str(float(var1)*float(var2)*float(var3))
            elif newRow['Expense_Type'] == 'Per-Diem Expense':
                newRow['Quantity'] = str(float(var1)*float(var2)*float(var4))
            elif newRow['Expense_Type'] == 'Local Transport Expense':
                newRow['Quantity'] = str(float(var1)*float(var5))
            elif newRow['Expense_Type'] == 'Guest House Lodging Expense':
                newRow['Quantity'] = str(0)
            else:
                newRow['Quantity'] = str(0)
            if (newRow['Final_Quantity'] == '' or float(newRow['Final_Quantity']) < float(newRow['Quantity'])) and newRow['Expense_Type'] not in ['Guest House Lodging Expense','Local Transport Expense Monthly','Miscellaneous Expense']: newRow['Final_Quantity'] = newRow['Quantity']
            if newRow['Unit_Cost'] == '' or float(newRow['Unit_Cost']) < float(newRow['Final_Quantity']): newRow['Unit_Cost'] = newRow['Final_Quantity']
            newRow['Total_Cost']  = newRow['Unit_Cost']
            newRow['Unit_List_Price'] = str(float(float(newRow['Unit_Cost'])*(float(1)+(float(var6)/100))))
            newRow['Total_List_Price'] = newRow['Unit_List_Price']
        cont.Calculate()