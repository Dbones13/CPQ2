Devices_Container =  Product.GetContainerByName('Terminal_Devices_Scope')


for row in Devices_Container.Rows:
    row.Product.Attr('TM Elements').AssignValue(row['Element'])
    Terminal_Type_Devices = SqlHelper.GetList("select RestrictValue from TM_DEVICES_RULES where Element = '{}'".format(row['Element']))
    c= row.Product.Attr('Terminal_Type_Devices').Values
    for v in Terminal_Type_Devices:
        for av in c:
            if av.ValueCode == v.RestrictValue:
                av.Allowed = False
                #Trace.Write(row['Element'] + 'check ' + av.ValueCode)
                break
    row.ApplyProductChanges()