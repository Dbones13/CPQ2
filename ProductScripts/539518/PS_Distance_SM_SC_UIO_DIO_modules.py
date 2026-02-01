cont = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
if cont.Rows.Count > 0:
    import GS_Populate_SM_IO_Modules
    safety_IO = {'Control Network Module (CNM)': ['< 4 KM', '>4 KM & <40 KM'], 'Third Party MOXA': ['550m Multi Mode SFP', '2km Multi Mode SFP', '10km Single Mode SFP', '15km Single Mode SFP', '70km Single Mode SFP']}

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.Display in location:
                    Trace.Write(i.Display)
                    i.Allowed = False
                elif i.Display not in location:
                    i.Allowed = True

    row = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0]
    list = row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules')
    value_list = list.ReferencingAttribute.Values
    try:
        switch_io = Product.Attr('SM_CG_Safety_IO_Link').GetValue()
        disallow(safety_IO[switch_io], value_list)
    except:
        Trace.Write("Error in line 19..")
        switch_io='Null'
    row.Calculate()

    cab_cont = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
    cab_cont_row = cab_cont.Rows[0]
    if cab_cont_row['Distance_SM_SC_UIO/DIO_modules'].strip() == '':
        if switch_io == 'Control Network Module (CNM)':
            cab_cont_row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('70km Single Mode SFP')
        else:
            cab_cont_row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('>4 KM & <40 KM')
        cab_cont_row.ApplyProductChanges()
    #cab_cont.Calculate()