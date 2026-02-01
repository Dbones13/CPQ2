if Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows.Count:
    UOC_CG_RT = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_IO_Rack_Type')
    UOC_CG_PS = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_Power_Supply')
    UOC_Power_Status = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_Power_Status_Mod_Redundant_Supply')
    if ((Quote.GetCustomField('IsR2QRequest').Content == 'Yes') or (Quote.GetCustomField('R2QFlag').Content == 'Yes')):
        control_cont = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows
        checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
        if control_cont.Count > 0:
            if checkproduct == 'Migration':
                control_cont[0].Product.Attr('UOC_IO_Rack_Type').SelectDisplayValue('4 I/O Rack')
                control_cont[0].Product.Attr('UOC_Power_Supply').SelectDisplayValue('Non Redundant')
            else:
                control_cont[0].Product.Attr('UOC_IO_Rack_Type').SelectDisplayValue('Optimum Mixed I/O Rack')
                control_cont[0].Product.Attr('UOC_Power_Supply').SelectDisplayValue('Non Redundant')

    power_status = UOC_Power_Status.ReferencingAttribute.Values
    UOC_CG_PS_List = UOC_CG_PS.ReferencingAttribute.Values
    UOC_CG_RT_List = UOC_CG_RT.ReferencingAttribute.Values
    if Quote.GetCustomField("isR2QRequest").Content != 'Yes':
        if UOC_CG_RT.Value == '4Rack':
            for i in UOC_CG_PS_List:
                if i.ValueCode == 'Redundant':
                    i.Allowed = False

        if UOC_CG_PS.Value == 'Redundant':
            for j in UOC_CG_RT_List:
                if j.ValueCode == '4Rack':
                    j.Allowed = False

        elif UOC_CG_PS.Value == 'NonRedundant':
            for yes in power_status:
                if yes.ValueCode == 'Yes':
                    yes.Allowed = False
        if not UOC_CG_PS.Value:
            UOC_CG_PS.Value == 'Non Redundant'
    UOC_CG_CT = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_Controller_Type')
    if UOC_CG_CT.Value == 'NonRedundant':
        UOC_CG_CT.SetAttributeValue('Non Redundant')
    if UOC_CG_CT.Value == 'Redundant':
        UOC_CG_CT.SetAttributeValue('Redundant')
#No Needed below code
#UOC_Power_Supply = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_Power_Supply')
#selectedValue = UOC_Power_Supply.DisplayValue
#UOC_Power_Supply.ReferencingAttribute.Product.Attr('UOC_Power_Supply').SelectDisplayValue(selectedValue)
#
#UOC_IO_Rack_Type = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_IO_Rack_Type')
#selected = UOC_IO_Rack_Type.DisplayValue
#UOC_IO_Rack_Type.ReferencingAttribute.Product.Attr('UOC_IO_Rack_Type').SelectDisplayValue(selected)

UOC_RemoteGroup_Cont = Product.GetContainerByName('UOC_RemoteGroup_Cont')

if UOC_RemoteGroup_Cont.Rows.Count > 0:
    for row in UOC_RemoteGroup_Cont.Rows:
        UOC_RG_Name = row.Product.Attr('UOC_RG_Name').GetValue()
        if str(row["Remote Group Name"]) != UOC_RG_Name:
            row.Product.Attr('UOC_RG_Name').AssignValue(str(row["Remote Group Name"]))
            row.ApplyProductChanges()
UOC_RemoteGroup_Cont.Calculate()

hidden = True if TagParserProduct.ParseString('<*CTX( Container(UOC_CG_Controller_Rack_Cont).Column(UOC_Redundant_Controller_Physical_Seperation).GetPermission )*>') == 'Hidden' else False
if  hidden:
    if Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows.Count:
        Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].SetColumnValue('UOC_Redundant_Controller_Physical_Seperation', "No")

hide_columns = ['UOC_Fiber_Optic_Converter_Single', 'UOC_Fiber_Optic_Converter_Multi']
for hide in hide_columns:
    hidden = True if TagParserProduct.ParseString('<*CTX( Container(UOC_CG_Additional_Controller_Cont).Column("'+str(hide)+'").GetPermission )*>') == 'Hidden' else False
    if  hidden:
        if Product.GetContainerByName('UOC_CG_Additional_Controller_Cont').Rows.Count:
            Product.GetContainerByName('UOC_CG_Additional_Controller_Cont').Rows[0].SetColumnValue(hide, '0')