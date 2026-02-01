if Product.Attr('isProductLoaded').GetValue() == 'True':
    psupply = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Supply')
    cell1 = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type')
    PLC_Power_Status = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply')

    #psupply.ReferencingAttribute.AssignValue('Non Redundant')
    #cell1.ReferencingAttribute.AssignValue('12 I/O Rack')

    value_list = psupply.ReferencingAttribute.Values
    value_list1 = cell1.ReferencingAttribute.Values
    power_status = PLC_Power_Status.ReferencingAttribute.Values

    if cell1.Value == '4Rack':
        for i in value_list:
            if i.ValueCode == 'Redundant':
                i.Allowed = False

    if psupply.Value == 'Redundant':
        for j in value_list1:
            if j.ValueCode == '4Rack':
                j.Allowed = False

    elif psupply.Value == 'NonRedundant':
        for yes in power_status:
            if yes.ValueCode == 'Yes':
                yes.Allowed = False



    PLC_Power_Supply = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Supply')
    selectedValue = PLC_Power_Supply.DisplayValue
    PLC_Power_Supply.ReferencingAttribute.Product.Attr('PLC_Power_Supply').SelectDisplayValue(selectedValue)

    PLC_IO_Rack_Type = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type')
    selected = PLC_IO_Rack_Type.DisplayValue
    PLC_IO_Rack_Type.ReferencingAttribute.Product.Attr('PLC_IO_Rack_Type').SelectDisplayValue(selected)

    PLC = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply')
    sel = PLC.DisplayValue
    PLC.ReferencingAttribute.Product.Attr('PLC_Power_Status_Mod_Redudant_Supply').SelectDisplayValue(sel)

    PLC_RemoteGroup_Cont = Product.GetContainerByName('PLC_RemoteGroup_Cont')

    if PLC_RemoteGroup_Cont.Rows.Count > 0:
        for row in PLC_RemoteGroup_Cont.Rows:
            PLC_RG_Name = row.Product.Attr('PLC_RG_Name').GetValue()
            if str(row["Remote Group Name"]) != PLC_RG_Name:
                row.Product.Attr('PLC_RG_Name').AssignValue(str(row["Remote Group Name"]))
                row.ApplyProductChanges()
    PLC_RemoteGroup_Cont.Calculate()


    hide_columns = ['PLC_Fiber_Optic_Converter_Single', 'PLC_Fiber_Optic_Converter_Multi_G3', 'PLC_Fiber_Optic_Converter_Multi']
    for hide in hide_columns:
        hidden = True if TagParserProduct.ParseString('<*CTX( Container(PLC_CG_Additional_Controller_Cont).Column("'+str(hide)+'").GetPermission )*>') == 'Hidden' else False
        if  hidden:
            Product.GetContainerByName('PLC_CG_Additional_Controller_Cont').Rows[0].SetColumnValue(hide, '0')