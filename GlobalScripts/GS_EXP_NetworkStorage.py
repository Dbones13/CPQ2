def getebrvalues(Product):
    ebr="No"
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Experion Server)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (ACE)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Simulation PC)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Mobile Terminal Server)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Flex Station ES-F)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Console Station ES-C)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore ConsoleStation Extension").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Console)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (ACE)1").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Simulation PC)1").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if Product.Attributes.GetByName("Experion Backup & Restore (Flex Station ES-F)1").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass

    Trace.Write(ebr)


    NSD=Product.Attributes.GetByName("Number of Network Storage Device - Standard(0-100)").GetValue()
    if NSD=="":
        NSD=Product.Attributes.GetByName("Number of Network Storage Device Standard").GetValue()
    Trace.Write(NSD)

    NSDP=Product.Attributes.GetByName("Number of Network Storage Device - Performance(0-100)").GetValue()
    if NSDP=="":
        NSDP=Product.Attributes.GetByName("Number of Network Storage Device Performance").GetValue()
    Trace.Write(NSDP)

    '''if ebr=="Yes":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-NWSTR4",int(NSD))
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-NWSTR5",int(NSDP))'''

    return ebr,NSD,NSDP