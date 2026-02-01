if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    ent_cont = Product.GetContainerByName("SC_P1P2_ServiceProduct_Entitlement_1")
    contigency_cont = Product.GetContainerByName("SC_P1P2_Contigency_Cost")
    splist = []
    m=[]
    for row1 in ent_cont.Rows:
        flag = False
        for row2 in contigency_cont.Rows:
            if row1["Service Product"] == row2["Service_Product"]:
                flag = True
                break
        if flag == False:
            controw = contigency_cont.AddNewRow(False)
            controw["Service_Product"] = row1["Service Product"]
            controw.Calculate()
        splist.append(row1["Service Product"])
    for row in contigency_cont.Rows:
        if row["Service_Product"] not in splist:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        contigency_cont.DeleteRow(i)
        contigency_cont.Calculate()