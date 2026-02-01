Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Checkproduct != "PRJT R2Q":
    import GS_PLC_UOC_IO_Calcs
    import GS_PLC_UOC_Racks_Calcs
    import GS_PLC_UOC_Processor_Calcs
    import GS_PLC_UOC_PSU_Calcs
    import GS_PLC_UOC_Software_Calcs
    import GS_PLC_UOC_Terminal_Calcs
    import GS_PLC_UOC_Auxilary_Calcs
    import GS_PLC_UOC_Network_Calcs
    import GS_PLC_UOC_Cabinet_Calcs
    import GS_PLC_ReadAttrs
    import GS_PLC_UOC_PartUpdate

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0
	
    try:
        attrs = GS_PLC_ReadAttrs.AttrStorage(Product)
        Product.Messages.Clear()
    except Exception, e:
        attrs = None
        Product.Messages.Add("Error when Reading PLC CG Attributes: " + str(e) )
        Trace.Write("Error when Reading PLC CG Attributes: " + str(e) )
        Log.Error("Error when Reading PLC CG Attributes: " + str(e) )
    parts_dict = {}

    if attrs:
        try:
            parts_dict,IO_mods = GS_PLC_UOC_IO_Calcs.calc_io_modules(attrs, parts_dict)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_IO_Calcs: " + str(e) )

        try:
            parts_dict,io_racks = GS_PLC_UOC_Racks_Calcs.calc_racks(attrs, parts_dict, IO_mods)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Racks_Calcs: " + str(e) )

        try:
            parts_dict,io_racks = GS_PLC_UOC_Processor_Calcs.calc_processor_modules(attrs, parts_dict, io_racks, IO_mods, Product)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Processor_Calcs: " + str(e) )

        try:
            parts_dict = GS_PLC_UOC_PSU_Calcs.calc_power_supplies(attrs, parts_dict, io_racks)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_PSU_Calcs: " + str(e) )

        try:
            parts_dict = GS_PLC_UOC_Software_Calcs.calc_software_plc_cg(attrs, parts_dict)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Software_Calcs: " + str(e) )

        try:
            parts_dict = GS_PLC_UOC_Cabinet_Calcs.calc_cabinets(attrs, parts_dict, io_racks)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Cabinet_Calcs: " + str(e) )

        try:
            parts_dict = GS_PLC_UOC_Terminal_Calcs.calc_terminals(attrs, parts_dict, IO_mods)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Terminal_Calcs: " + str(e) )

        try:
            parts_dict = GS_PLC_UOC_Auxilary_Calcs.calc_auxilary(attrs, parts_dict)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Auxilary_Calcs: " + str(e) )

        try:
            parts_dict = GS_PLC_UOC_Network_Calcs.calc_network(attrs, parts_dict, io_racks, Product)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Network_Calcs: " + str(e) )

        #parts_dict['900CP1-0200'] += attrs.addl_ctrlr_addl_ctrlr
        """if parts_dict.get('900CP2-0100',0):
            parts_dict['900CP2-0100'] += attrs.addl_ctrlr_addl_ctrlr

            Trace.Write("Parts Dict: {0}".format(parts_dict))

            Trace.Write("Parts Dict: {0}".format(parts_dict))"""
        if Product.Attr('MIgration_Scope_Choices').GetValue() == 'LABOR':
            parts_dict= dict()
        GS_PLC_UOC_PartUpdate.execute(Product, 'PLC_CG_PartSummary_Cont', parts_dict, attrs)

    plc_cont = Product.GetContainerByName('PLC_CG_PartSummary_Cont')
    cab_cont = Product.GetContainerByName('PLC_CG_Cabinet_Cont')
    from math import ceil
    marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
    Marshal_Qty = int(0)
    final_qty_R = int(0)
    qty1 = int(0)
    Marshal_Qty_R = int(0)
    qty1_R = int(0)
    final_qty = int(0)
    for row in plc_cont.Rows:
        if row['CE_Part_Number'] == 'CC-CBDD01':
            qty1 = int(row['CE_Part_Qty'])
        elif row['CE_Part_Number'] == 'CC-CBDS01':
            qty1 = int(row['CE_Part_Qty'])
        elif  row['CE_Part_Number'] in marshal_parts:
            Marshal_Qty += int(row['CE_Part_Qty'])
        if row["CE_Final_Quantity"] == '':
            row["CE_Final_Quantity"] = row["CE_Part_Qty"]
        else:
            val = int(getFloat(row["CE_Part_Qty"]) + getFloat(row["CE_Adj_Quantity"]))
            row["CE_Final_Quantity"] =str(val)

    for val in cab_cont.Rows:
        if  val['PLC_Cabinet_Type'] == 'One':
            final_qty = int(ceil(float(qty1)/2.0))
        elif val['PLC_Cabinet_Type'] == 'Dual':
            final_qty = int(qty1)    
    Product.Attr('PLC_Num_of_Sys_Cabinets').AssignValue(str(final_qty))
    Product.Attr('PLC_Marshal_Cabinet_Qty').AssignValue(str(Marshal_Qty))

    Log.Info('IN PS_PLC_CG_LI_Part_Summary')

    plc_cont_rows = Product.GetContainerByName('PLC_CG_PartSummary_Cont').Rows
    #Product.Messages.Clear()
    errorFlag = False
    for row in plc_cont_rows:
        row['CE_Final_Quantity'] = str(int(getFloat(row["CE_Adj_Quantity"]) + getFloat(row["CE_Part_Qty"])))
    for row in plc_cont_rows:
        finalQuantity = int(row['CE_Final_Quantity'])
        if finalQuantity < 0:
            errorFlag = True
            break
    Trace.Write("Error Flag: " + str(errorFlag))
    if errorFlag:
        #Product.Messages.Add("Please check part number with -ve qty in Final Quantity Column and update value in '+/- Adj Quantity' column")
        Product.Attr('PartSummaryErrorMsg').AssignValue('True')
        Trace.Write('Error Flag True: ' + str(errorFlag))
    else:
        Trace.Write('Error Flag False: ' + str(errorFlag))
        Product.Attr('PartSummaryErrorMsg').AssignValue('False')
        #Product.Messages.Clear()
        plc_cont_rows = Product.GetContainerByName('PLC_CG_PartSummary_Cont').Rows
        plc_li_cont = Product.GetContainerByName('PLC_CG_PartSummary_LI_Cont')
        plc_li_cont.Rows.Clear()
        for row in plc_cont_rows:
            part = row['CE_Part_Number']
            quantity = row['CE_Part_Qty']
            #part_description = row['CE_Part_Description']
            adjQuantity = row['CE_Adj_Quantity'] if row['CE_Adj_Quantity'] else 0
            comments = row['CE_Comments']
            finalQuantity = int(row['CE_Final_Quantity'])
            row.Calculate()
            if finalQuantity > 0:
                row = plc_li_cont.AddNewRow(part, False)
                row.GetColumnByName("CE_Part_Qty").Value = quantity
                #row.GetColumnByName("CE_Part_Description").Value = part_description
                row.GetColumnByName("CE_Adj_Quantity").Value = str(adjQuantity)
                row.GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(finalQuantity))
                row.GetColumnByName("CE_Comments").Value = comments
                row.Calculate()    
    Product.ApplyRules()