def setAtvQty(Product,AttrName,PartNumber,qty):
    Cont=Product.Attr(AttrName).Values
    for Parts in Cont:
        if Parts.Display == PartNumber:
            Parts.IsSelected=False
            Parts.Quantity = 0
            if qty > 0:
                Parts.IsSelected=True
                Parts.Quantity=qty
                Trace.Write('Selected ' + PartNumber + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break



qty_server = int(Product.Attr("ESDC_Red_nonRed_Check").GetValue())
ESDC_Release = Product.Attr('ESDC_Software_Release').GetValue()
Server_NodeSupplier = Product.Attr('ESDC_Node_Supplier_Server').GetValue()
Station_NS = Product.Attr('ESDC_Node_Supplier').GetValue()
Server_NodeType = Product.Attr('ESDC_Server_Node_Type').GetValue()
Station_NodeType = Product.Attr('ESDC_Station_Node_Type').GetValue()
TPM = Product.Attr('ESDC_Trusted_Platform_Module').GetValue()
qty_station = Product.Attr("ESDC_Client_Station_Qty").GetValue()

qty_MZ_SQLCL4 = qty_server
qty_MZ_PCSV85 = 0
qty_MZ_PCWT01 = 0
qty_MZ_PCWR01 = 0
qty_MZ_PCWS86 = 0
qty_MZ_PCWS15 = 0
qty_EP_COAW21 = 0
qty_MZ_PCSR05 = 0
qty_MZ_PCSR06 = 0
qty_MZ_PCST03 = 0
qty_MZ_PCST04 = 0
qty_MZ_PCSR03 = 0
qty_MZ_PCSR04 = 0
qty_EP_COAS22 = 0
qty_MZ_PCWT02 = 0
qty_COAS19 = 0
if TPM and Server_NodeSupplier == 'Honeywell':
    if ESDC_Release == 'R530':
        qty_EP_COAS22 = qty_server
    if ESDC_Release in ('R520','R530'):
        if Server_NodeType == 'SVR_PER_HP_Rack_RAID5' and TPM == 'Yes':
            qty_MZ_PCSV85 = qty_server
        elif Server_NodeType == 'SVR_STD_DELL_Rack_RAID1':
            qty_MZ_PCSR05 = qty_server
        elif Server_NodeType == 'SVR_PER_DELL_Rack_RAID1':
            qty_MZ_PCSR06 = qty_server
        elif Server_NodeType == 'SVR_STD_DELL_Tower_RAID1':
            qty_MZ_PCST03 = qty_server
        elif Server_NodeType == 'SVR_PER_DELL_Tower_RAID1':
            qty_MZ_PCST04 = qty_server
        elif Server_NodeType == 'SVR_PER_DELL_Rack_RAID1_XE' and TPM == 'Yes':
            qty_MZ_PCSR03 = qty_server
        elif Server_NodeType == 'SVR_PER_DELL_Rack_RAID5' and TPM == 'Yes':
            qty_MZ_PCSR04 = qty_server

if Station_NS == 'Honeywell':
    if ESDC_Release == 'R520':
        if Station_NodeType == 'STN_PER_DELL_Tower_RAID2':
            qty_MZ_PCWT02 = int(qty_station)
            qty_COAS19= qty_server + int(qty_station)
    if ESDC_Release == 'R530':
        qty_MZ_SQLCL4 = qty_server + int(qty_station)
        if Station_NodeType != 'STN_STD_DELL_Tower_NonRAID':
            qty_EP_COAW21 = int(qty_station)
        if Station_NodeType == 'STN_PER_DELL_Tower_RAID1':
            qty_MZ_PCWT01 = int(qty_station)
        if Station_NodeType == 'STN_PER_DELL_Rack_RAID1':
            qty_MZ_PCWR01 = int(qty_station)
        if Station_NodeType == 'STN_PER_HP_Tower_RAID1':
            qty_MZ_PCWS86 = int(qty_station)
        if Station_NodeType == 'STN_STD_DELL_Tower_NonRAID':
            qty_MZ_PCWS15 = int(qty_station)
    if ESDC_Release == 'R520':
        qty_MZ_SQLCL4 = qty_server + int(qty_station)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-SQLCL4",qty_MZ_SQLCL4)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCSV85",qty_MZ_PCSV85)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCWT01",qty_MZ_PCWT01)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCWS86",qty_MZ_PCWS86)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCWS15",qty_MZ_PCWS15)
setAtvQty(Product,"ESDC_BOM_Parts","EP-COAW21",qty_EP_COAW21)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCSR05",qty_MZ_PCSR05)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCSR06",qty_MZ_PCSR06)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCST03",qty_MZ_PCST03)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCST04",qty_MZ_PCST04)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCSR03",qty_MZ_PCSR03)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCSR04",qty_MZ_PCSR04)
setAtvQty(Product,"ESDC_BOM_Parts","EP-COAS22",qty_EP_COAS22)
setAtvQty(Product,"ESDC_BOM_Parts","MZ-PCWT02",qty_MZ_PCWT02)
setAtvQty(Product,"ESDC_BOM_Parts","EP-COAS19",qty_COAS19)
