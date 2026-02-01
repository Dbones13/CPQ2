if Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows.Count > 0:
    PLC_PS_RG = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Supply')
    PLC_RT_RG = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type')
    PLC_Power_Status = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply')


    #psupply.ReferencingAttribute.AssignValue('Non Redundant')
    #cell1.ReferencingAttribute.AssignValue('12 I/O Rack')
    power_status = PLC_Power_Status.ReferencingAttribute.Values
    PLC_PS_RG_List = PLC_PS_RG.ReferencingAttribute.Values
    PLC_RT_RG_List = PLC_RT_RG.ReferencingAttribute.Values

    if PLC_RT_RG.Value == '4Rack':
        for i in PLC_PS_RG_List:
            if i.ValueCode == 'Redundant':
                i.Allowed = False

    if PLC_PS_RG.Value == 'Redundant':
        for j in PLC_RT_RG_List:
            if j.ValueCode == '4Rack':
                j.Allowed = False
                
    if PLC_PS_RG.Value == 'NonRedundant':
        Trace.Write("333")
        for j in power_status:
            Trace.Write("4444"+str(j.ValueCode))
            if j.ValueCode == 'Yes':
                Trace.Write("55555"+str(j.ValueCode))
                j.Allowed = False
    elif PLC_PS_RG.Value == 'NonRedundant':
        for yes in power_status:
            if yes.ValueCode == 'Yes':
                yes.Allowed = False


    PLC_Power_Supply = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Supply')
    selectedValue = PLC_Power_Supply.DisplayValue
    PLC_Power_Supply.ReferencingAttribute.Product.Attr('PLC_Power_Supply').SelectDisplayValue(selectedValue)

    PLC_IO_Rack_Type = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type')
    selected = PLC_IO_Rack_Type.DisplayValue
    PLC_IO_Rack_Type.ReferencingAttribute.Product.Attr('PLC_IO_Rack_Type').SelectDisplayValue(selected)
    
    PLC_Power_Supply = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply')
    selectedValue = PLC_Power_Supply.DisplayValue
    PLC_Power_Supply.ReferencingAttribute.Product.Attr('PLC_Power_Status_Mod_Redudant_Supply').SelectDisplayValue(selectedValue)