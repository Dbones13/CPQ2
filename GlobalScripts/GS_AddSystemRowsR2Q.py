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
            Session['checkScript'] = 'True'
            container.AddNewRow(False)
            Session['checkScript'] = ''
            Session['ManualcheckScript'] = ''

if Product.Name == "New / Expansion Project":
    SG_cont = Product.GetContainerByName('Number_System_Groups').Rows[0]
    SG_rowCount = SG_cont.GetColumnByName('Number_System_Groups').Value
    SG_rowCount = int(SG_rowCount) if SG_rowCount else 0
    CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
    try:
        AddRows(SG_rowCount, CE_SystemGroup_Cont)
    except:
        Product.Attr('ExceededLimit').AssignValue('True')
        pass

elif Product.Name == "Experion Enterprise Group":

    Experion_Attr_count= Product.Attr('Number of Locations_Clusters_Network').GetValue()
    Experion_Attr_count = int(Experion_Attr_count) if Experion_Attr_count else 0
    Location_cluster = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
    try:
        AddRows(Experion_Attr_count,Location_cluster)
    except:
        Product.Attr('ExceededLimit').AssignValue('True')
        pass

elif Product.Name == "R2Q C300 System":

    group_count= Product.Attr('Number_of_Series_C_Control_Groups').GetValue()
    group_count = int(group_count) if group_count else 0
    cont = Product.GetContainerByName('R2Q_Series_C_Control_Groups_Cont')
    try:
        AddRows(group_count,cont)
    except:
        Product.Attr('ExceededLimit').AssignValue('True')

elif Product.Name == "R2Q Series-C Control Group":

    group_count= Product.Attr('Number_of_Series_C_Remote_Groups').GetValue()
    group_count = int(group_count) if group_count else 0
    cont = Product.GetContainerByName('R2Q_Series_C_Remote_Groups_Cont')
    try:
        AddRows(group_count,cont)
    except:
        Product.Attr('ExceededLimit').AssignValue('True')

elif Product.Name == "R2Q Experion Enterprise System":

    Experion_Attr_count= Product.Attr('Number of Experion Enterprise Groups').GetValue()
    Experion_Attr_count = int(Experion_Attr_count) if Experion_Attr_count else 0
    Experion_Enterprise_Cont = Product.GetContainerByName('R2Q_Experion_Enterprise_Cont')
    try:
        AddRows(Experion_Attr_count,Experion_Enterprise_Cont)
    except:
        Product.Attr('ExceededLimit').AssignValue('True')
        pass