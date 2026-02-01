safety_IO = {'Control Network Module (CNM)': ['< 4 KM', '>4 KM & <40 KM'], 'Third Party MOXA': ['550m Multi Mode SFP', '2km Multi Mode SFP', '10km Single Mode SFP', '15km Single Mode SFP', '70km Single Mode SFP']}

def disallow(location, dropdownlist):
    if location:
        for i in dropdownlist:
            if i.Display in location:
                Trace.Write(i.Display)
                i.Allowed = False
            elif i.Display not in location:
                i.Allowed = True

switch_io = 'Control Network Module (CNM)'
SM_CG_Common_Questions_Cont = Product.GetContainerByName('SM_CG_Common_Questions_Cont')
if SM_CG_Common_Questions_Cont.Rows.Count > 0:
    switch_io = SM_CG_Common_Questions_Cont.Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue
    SM_SCController_Architecture = SM_CG_Common_Questions_Cont.Rows[0].GetColumnByName('SM_SCController_Architecture').DisplayValue
Product.Attr('SM_CG_Safety_IO_Link').AssignValue(switch_io)
SM_RemoteGroup_Cont = Product.GetContainerByName('SM_RemoteGroup_Cont')
if SM_RemoteGroup_Cont.Rows.Count > 0:
    for row in SM_RemoteGroup_Cont.Rows:
        SM_RG_Name = row.Product.Attr('SM_RG_Name').GetValue()

        Safety_IO = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue
        Product.Attr('SM_CG_Safety_IO_Link').AssignValue(Safety_IO)
        IOTA = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        Product.Attr('SM_Universal_IOTA_Type').AssignValue(IOTA)

        SM_CG_Safety_IO_Link = row.Product.Attr('SM_CG_Safety_IO_Link').GetValue()
        row.Product.Attr('SM_Universal_IOTA_Type').AssignValue(Product.Attr('SM_Universal_IOTA_Type').GetValue())
        row.SetColumnValue( 'SM_Universal_IOTA_Type', Product.Attr('SM_Universal_IOTA_Type').GetValue())
        row.GetColumnByName('SM_Universal_IOTA_Type').SetAttributeValue(Product.Attr('SM_Universal_IOTA_Type').GetValue())
        row.SetColumnValue( 'SM_CG_Safety_IO_Link', Product.Attr('SM_CG_Safety_IO_Link').GetValue())
        row.GetColumnByName('SM_CG_Safety_IO_Link').SetAttributeValue(Product.Attr('SM_CG_Safety_IO_Link').GetValue())
        #Shivani
        row.Product.Attr('Controller_Architecture').AssignValue(SM_SCController_Architecture)
        if SM_CG_Safety_IO_Link != Product.Attr('SM_CG_Safety_IO_Link').GetValue():
            row.Product.Attr('SM_CG_Safety_IO_Link').AssignValue(Product.Attr('SM_CG_Safety_IO_Link').GetValue())
            cabRow = row.Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0]
            list = cabRow.GetColumnByName('Distance_SM_SC_UIO/DIO_modules')
            value_list = list.ReferencingAttribute.Values
            disallow(safety_IO[switch_io], value_list)
            cabRow.Calculate()
            if switch_io == 'Control Network Module (CNM)':
                cabRow.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('70km Single Mode SFP')
            else:
                cabRow.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('>4 KM & <40 KM')

        if str(row["Remote Group Name"]) != SM_RG_Name:
            row.Product.Attr('SM_RG_Name').AssignValue(str(row["Remote Group Name"]))
        row.ApplyProductChanges()
        row.Product.ApplyRules()
SM_RemoteGroup_Cont.Calculate()