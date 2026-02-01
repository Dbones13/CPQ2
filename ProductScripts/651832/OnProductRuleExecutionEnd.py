from GS_R2Q_SafetyManagerContainerColumns import SafetyManagerContainerColumns as SMCC
SM_ControlGroup_Cont = Product.GetContainerByName('SM_ControlGroup_Cont')
if SM_ControlGroup_Cont.Rows.Count > 0:
    contCal = False
    for row in SM_ControlGroup_Cont.Rows:
        SM_CG_Name = row.Product.Attr('SM_CG_Name').GetValue()
        if str(row["Control Group Name"]) != SM_CG_Name:
            row.Product.Attr('SM_CG_Name').AssignValue(str(row["Control Group Name"]))
            row.ApplyProductChanges()
            contCal = True
    if contCal:
        SM_ControlGroup_Cont.Calculate()
if Product.GetContainerByName('Number_SM_Control_Groups_Cont').Rows.Count > 0:
    label = Product.GetContainerByName('Number_SM_Control_Groups_Cont').Rows[0]
    label.GetColumnByName('Number_SM_Control_Groups').HeaderLabel = "Number of Safety Manager System Control Groups (1-10)"

for cont in SMCC.safetyManagerContainer:
    if Product.GetContainerByName(cont) and Product.GetContainerByName(cont).Rows and Product.GetContainerByName(cont).Rows.Count > 0:
        colmns = Product.GetContainerByName(cont).Rows[0].GetColumnByName('Station_Type').ReferencingAttribute
        for val in colmns.Values:
            if val.Display in ('None'):
                val.Allowed = False
if Product.Name == 'R2Q Safety Manager ESD':
    Product.Attr('ProductLine').AssignValue('ESD')
else:
    Product.Attr('ProductLine').AssignValue('FGS')