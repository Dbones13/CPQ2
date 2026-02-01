laborCont = Product.GetContainerByName('CE PLC Engineering Labor Container')
for row in laborCont.Rows:
    #Trace.Write(row["GES Eng"])
    #Trace.Write(row.GetColumnByName("FO Eng 1").ReferencingAttribute.Values)
    for val in row.GetColumnByName("FO Eng 1").ReferencingAttribute.Values:
        #Trace.Write(val.ValueCode)
        if val.Display == row["FO Eng 1"]:
            row["FO Eng 1"] = val.ValueCode

    for val in row.GetColumnByName("FO Eng 2").ReferencingAttribute.Values:
        #Trace.Write(val.ValueCode)
        if val.Display == row["FO Eng 2"]:
            row["FO Eng 2"] = val.ValueCode