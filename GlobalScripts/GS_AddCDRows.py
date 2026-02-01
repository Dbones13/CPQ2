def AddRows(rowCount, container):
    for i in range(rowCount):
        container.AddNewRow(False)

if Product.Name == "Experion MX System":

    MX_CD_Group_Count= Product.Attr('MX_CD_Group_Count').GetValue()
    MX_CD_Group_Count = int(MX_CD_Group_Count) if MX_CD_Group_Count else 0
    MX_CD_group = Product.GetContainerByName('MX_CD_group')
    try:
        AddRows(MX_CD_Group_Count,MX_CD_group)
    except:
        Product.Attr('ExceededLimitCD').AssignValue('True')
        pass

if Product.Name == "MXProLine System":

    MXP_CD_Group_Count= Product.Attr('MXP_CD_Group_Count').GetValue()
    MXP_CD_Group_Count = int(MXP_CD_Group_Count) if MXP_CD_Group_Count else 0
    MXP_CD_group = Product.GetContainerByName('MXP_CD_group')
    try:
        AddRows(MXP_CD_Group_Count,MXP_CD_group)
    except:
        Product.Attr('ExceededLimitCD').AssignValue('True')
        pass