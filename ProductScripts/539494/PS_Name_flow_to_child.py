qcs_check = Product.Attr('MXP_What_QCS_System_is_required').GetValue()

if qcs_check == "QCS MD" or qcs_check == "QCS MD & CD":
    scanner_cont = Product.GetContainerByName('MXP_Scanner_group')
    if scanner_cont.Rows.Count > 0:
        for row in scanner_cont.Rows:
            scanner_name = row.Product.Attr('Scanner_Group_Name').GetValue()
            if str(row['Scanner_Group_Name']) != scanner_name:
                row.Product.Attr('Scanner_Group_Name').AssignValue(str(row["Scanner_Group_Name"]))
                row.ApplyProductChanges()

if qcs_check == "QCS CD" or qcs_check == "QCS MD & CD":
    cd_cont = Product.GetContainerByName('MXP_CD_group')
    if cd_cont.Rows.Count > 0:
        for row in cd_cont.Rows:
            cd_name = row.Product.Attr('CD_Control_group_Name').GetValue()
            if str(row['CD_Control_Name']) != cd_name:
                row.Product.Attr('CD_Control_group_Name').AssignValue(str(row["CD_Control_Name"]))
                row.ApplyProductChanges()