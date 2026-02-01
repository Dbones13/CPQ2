UOC_RG_Controller_Rack_Cont = Product.GetContainerByName('UOC_RG_Controller_Rack_Cont')

if UOC_RG_Controller_Rack_Cont.Rows and UOC_RG_Controller_Rack_Cont.Rows.Count > 0:
    UOC_RG_PS = UOC_RG_Controller_Rack_Cont.Rows[0].GetColumnByName('UOC_Power_Supply')
    UOC_RG_RT = UOC_RG_Controller_Rack_Cont.Rows[0].GetColumnByName('UOC_IO_Rack_Type')
    UOC_Power_Status = UOC_RG_Controller_Rack_Cont.Rows[0].GetColumnByName('UOC_Power_Status_Mod_Redundant_Supply')

    power_status = UOC_Power_Status.ReferencingAttribute.Values
    UOC_RG_PS_List = UOC_RG_PS.ReferencingAttribute.Values
    UOC_RG_RT_List = UOC_RG_RT.ReferencingAttribute.Values

    if UOC_RG_RT.Value == '4Rack':
        for i in UOC_RG_PS_List:
            if i.ValueCode == 'Redundant':
                i.Allowed = False

    if UOC_RG_PS.Value == 'Redundant':
        for j in UOC_RG_RT_List:
            if j.ValueCode == '4Rack':
                j.Allowed = False
    elif UOC_RG_PS.Value == 'NonRedundant':
        for yes in power_status:
            if yes.ValueCode == 'Yes':
                yes.Allowed = False
    if not UOC_RG_PS.Value:
        UOC_RG_PS.Value = 'Non Redundant'