Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Checkproduct != "PRJT R2Q":
    FDMCont = Product.GetContainerByName('DVM_System_Group_Cont')
    if FDMCont.Rows.Count > 0:
        total_value = 0
        for attr_value in ("Numbers_of_FIXED_Type_Camera_at_Hazardous_Area", "Numbers_of_PTZ_Type_Camera_at_Hazardous_Area", "Numbers_of_FIXED_Type_Camera_at_Safe_Area", "Numbers_of_PTZ_Type_Camera_at_Safe_Area", "Numbers_of_FIXED_Type_Camera_Indoor", "Numbers_of_PTZ_Type_Camera_Indoor"):
            value = Product.Attr(attr_value).GetValue()
            if value and value.isdigit():
                total_value += int(value)
        for row in FDMCont.Rows:
            Sys_Group_Name = row.Product.Attr('DVM_System_Group_Name').GetValue()
            if str(row["DVM_System_Group_Name"]) != Sys_Group_Name:
                row.Product.Attr('DVM_System_Group_Name').AssignValue(str(row["DVM_System_Group_Name"]))
            #row.Product.Attr('DVM_4_Camera_Interface').AssignValue(str(total_value))
            row.ApplyProductChanges()
            row.Calculate()