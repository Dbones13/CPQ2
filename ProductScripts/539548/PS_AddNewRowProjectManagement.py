if Session["Product Loading"] != True:
    msid_scope = Product.Attr('MIgration_Scope_Choices').GetValue()
    subprd_container = Product.GetContainerByName('CONT_MSID_SUBPRD')
    deleteRowIndexes = []
    pm_is_exist = False

    for row in subprd_container.Rows:
        if row['Selected_Products'] == 'Project Management':
            pm_is_exist = True
            deleteRowIndexes.append(row.RowIndex)

    '''deleteRowIndexes.reverse()
    for deleteRow in deleteRowIndexes:
        subprd_container.DeleteRow(deleteRow)'''

    if msid_scope in ['LABOR','HW/SW/LABOR'] :
        if  subprd_container.Rows.Count > 0 and pm_is_exist == False:
            newRow = subprd_container.AddNewRow('Project_Management_cpq')
    else:
        deleteRowIndexes.reverse()
        for deleteRow in deleteRowIndexes:
            subprd_container.DeleteRow(deleteRow)