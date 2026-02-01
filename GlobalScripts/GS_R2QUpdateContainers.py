def AddRows(rowCount, container):
    for i in range(rowCount):
        if container.Name == 'CE_SystemGroup_Cont':
            row = container.AddNewRow(False)
            row.Product.Attr("CE_System_Index").AssignValue(str(row.RowIndex + 1))
            row.Product.Attr('CE_Scope_Choices').SelectDisplayValue('HW/SW + LABOR')
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
        else:
            container.AddNewRow(False)

if Product.Name in ["C300 System", 'R2Q Projects','R2Q New / Expansion Project']:
    if(Quote.GetCustomField('isR2QRequest').Content == 'Yes'):
		CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
		row = Product.GetContainerByName('CE_SystemGroup_Cont').Rows[0]
		productContainer = row.Product.GetContainerByName('CE_System_Cont')
		group_count= Product.Attr('Number_of_Series_C_Control_Groups').GetValue()
		group_count = int(group_count) if group_count else 0
		cont = productContainer.Rows[0].Product.GetContainerByName('Series_C_Control_Groups_Cont')
		try:
			AddRows(group_count,cont)
		except:
			Product.Attr('ExceededLimit').AssignValue('True')