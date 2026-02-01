safety_IO = {'Control Network Module (CNM)': ['< 4 KM', '>4 KM & <40 KM'], 'Third Party MOXA': ['550m Multi Mode SFP', '2km Multi Mode SFP', '10km Single Mode SFP', '15km Single Mode SFP', '70km Single Mode SFP']}

def disallow(location, dropdownlist):
    if location:
        for i in dropdownlist:
            if i.Display in location:
                Trace.Write(i.Display)
                i.Allowed = False
            elif i.Display not in location:
                i.Allowed = True
if Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows.Count > 0:
    switch_io = str(Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue)
    if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows.Count > 0:
        row = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0]
        list = row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules')
        value_list = list.ReferencingAttribute.Values

        if switch_io !="":
            disallow(safety_IO[switch_io], value_list)

        distance = row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').DisplayValue
        if switch_io == 'Control Network Module (CNM)':
            if distance in ['', '< 4 KM', '>4 KM & <40 KM']:
                row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('70km Single Mode SFP')
                row.ApplyProductChanges()
                #row.ApplyRules() --> it should be "row.Product.ApplyRules"
        elif switch_io == 'Third Party MOXA':
            if distance not in ['< 4 KM', '>4 KM & <40 KM']:
                row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('>4 KM & <40 KM')
                row.ApplyProductChanges()
                #row.ApplyRules() --> it should be "row.Product.ApplyRules"
        row.Calculate()