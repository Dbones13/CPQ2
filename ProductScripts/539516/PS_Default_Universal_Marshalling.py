con = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
if con.Rows.Count == 1:
    check_1 = con.Rows[0]
    check = check_1.GetColumnByName("Marshalling_Option").DisplayValue
    cab_cont = Product.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details')
    if check in ("Universal Marshalling"):
        if cab_cont.Rows.Count == 0:
            row = cab_cont.AddNewRow(False)
            row.GetColumnByName('IP_Rating').SetAttributeValue('IP20')
            row.GetColumnByName('Cabinet').SetAttributeValue('Dual Access')
            row.GetColumnByName('Cabinet Layout').ReferencingAttribute.SelectDisplayValue('3 Column')
            row.GetColumnByName('Mounting Option').SetAttributeValue('Bracket Mounting')
            row.GetColumnByName('Supply Vendor').SetAttributeValue('Honeywell')
            row.GetColumnByName('Cabinet Power').SetAttributeValue('120/230VAC')
            row.GetColumnByName('AC Input Voltage').SetAttributeValue('230VAC')
            row.GetColumnByName('Cabinet Fan').SetAttributeValue('No')
            row.GetColumnByName('Cabinet Thermostat').SetAttributeValue('No')
            row.GetColumnByName('Cabinet Light (LED)').SetAttributeValue('No')
            row.GetColumnByName('Utility Socket (230/115 VAC)').SetAttributeValue('No')
            row.GetColumnByName('Wiring & Ducts').SetAttributeValue('Standard PVC FRLS(Fire Retard +Low Smoke)')
            row.GetColumnByName('Termination of Spare Wires in Field Cabinets').SetAttributeValue('Not Terminated')
            row.GetColumnByName('Percentage of Spare Space').SetAttributeValue('0')
            row.GetColumnByName('SIC cable length for RUSIO/PUIO/ PDIO').SetAttributeValue('6M')
            #cab_cont.Rows[0].Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
    else:
        if cab_cont.Rows.Count > 0:
            cab_cont.Rows.Clear()
            cab_cont.Calculate()