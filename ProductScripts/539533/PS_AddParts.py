def setAtvQty(Product,AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=False
            av.Quantity = 0
            if qty > 0:
                av.IsSelected=True
                av.Quantity=qty
                Trace.Write('Selected ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break

EP_COAW21_qty= 0
MZ_PCWT01_qty = 0
MZ_PCWR01_qty = 0
MZ_PCWS86_qty = 0
MZ_PCWS15_qty = 0
MZ_PCSR03_qty = 0
MZ_PCWS94_qty = 0
MZ_PCSR05_qty = 0
MZ_PCSR06_qty = 0
MZ_PCST03_qty = 0
MZ_PCST04_qty = 0
MZ_PCSR04_qty = 0
EP_COAS19_qty = 0

SR = Product.Attr("ES_Experion_PKS_Release").GetValue()
ESSN = Product.Attr("ES_eServer_Staton_Node").GetValue()
NS = Product.Attr("ES_Node_Supplier_station").GetValue()
Add_Station = Product.Attr("ES_Additional_Stations_for_eServer").GetValue()


if SR in ['R520','R511'] and ESSN =='STN_PER_DELL_Tower_RAID1' and NS == "Honeywell" and int(Add_Station)  > 0:
    MZ_PCWS94_qty += int(Add_Station)
if SR == 'R530' and ESSN in ['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1'] and NS == "Honeywell" and int(Add_Station)  > 0:
    EP_COAW21_qty += int(Add_Station)
if SR == 'R530' and NS == "Honeywell" and int(Add_Station)  > 0:
    if ESSN == 'STN_PER_DELL_Tower_RAID1':
        MZ_PCWT01_qty += int(Add_Station)
    elif ESSN == "STN_PER_DELL_Rack_RAID1":
        MZ_PCWR01_qty += int(Add_Station)
    elif ESSN == "STN_PER_HP_Tower_RAID1":
         MZ_PCWS86_qty += int(Add_Station)
    elif ESSN == "STN_STD_DELL_Tower_NonRAID":
        MZ_PCWS15_qty += int(Add_Station)

MSN = Product.Attr("ES_Mobile_Server_Nodes_required").GetValue()
MSN_TPM = Product.Attr("ES_Trusted_Platform_Module_Mobile_Server").GetValue()
MSN_NS = Product.Attr("ES_Node_Supplier_Mobile_Server").GetValue()
if SR in ["R530","R520"] and MSN == 'Yes' and MSN_NS =='Honeywell' and MSN_TPM:
    HwSel = Product.Attr("ES_Hardware_Selection").GetValue()
    Trace.Write(HwSel)
    if  HwSel == 'SVR_PER_DELL_Rack_RAID1_XE'  and MSN_TPM == 'Yes':
        MZ_PCSR03_qty += 1
    elif  HwSel == 'SVR_STD_DELL_Rack_RAID1':
        MZ_PCSR05_qty += 1
    elif  HwSel == 'SVR_PER_DELL_Rack_RAID1':
        MZ_PCSR06_qty += 1
    elif  HwSel == 'SVR_STD_DELL_Tower_RAID1':
        MZ_PCST03_qty += 1
    elif  HwSel == 'SVR_PER_DELL_Tower_RAID1':
        MZ_PCST04_qty += 1
    elif HwSel == 'SVR_PER_DELL_Rack_RAID5'  and MSN_TPM == 'Yes':
        MZ_PCSR04_qty += 1

eServerNode = Product.Attr("ES_Server_Node_Type").GetValue()
NS_Server = Product.Attr("ES_Node_Supplier_Server").GetValue()
tpm_Server = Product.Attr("ES_Trusted_Platform_Module").GetValue()

if  SR in ["R530","R520"]  and NS_Server =='Honeywell' and tpm_Server :
    if eServerNode == 'SVR_PER_DELL_Rack_RAID1_XE'  and tpm_Server == 'Yes':
        MZ_PCSR03_qty += 1
    elif eServerNode == 'SVR_STD_DELL_Rack_RAID1':
        MZ_PCSR05_qty += 1
    elif eServerNode == 'SVR_PER_DELL_Rack_RAID1':
        MZ_PCSR06_qty += 1
    elif eServerNode == 'SVR_STD_DELL_Tower_RAID1':
        MZ_PCST03_qty += 1
    elif eServerNode == 'SVR_PER_DELL_Tower_RAID1':
        MZ_PCST04_qty += 1
    elif eServerNode == 'SVR_PER_DELL_Rack_RAID5'  and tpm_Server == 'Yes':
        MZ_PCSR04_qty += 1

if SR=='R520':
    if NS == "Honeywell":
        EP_COAS19_qty =1
    if MSN == 'Yes' and MSN_NS == "Honeywell":
        EP_COAS19_qty +=1
    if Add_Station >0:
        EP_COAS19_qty = EP_COAS19_qty + int(Add_Station)

setAtvQty(Product,"eServer_BOM_parts","EP-COAW21",EP_COAW21_qty)
setAtvQty(Product,"eServer_BOM_parts","EP-COAS19",EP_COAS19_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCWT01",MZ_PCWT01_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCWR01",MZ_PCWR01_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCWS86",MZ_PCWS86_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCWS15",MZ_PCWS15_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCSR03",MZ_PCSR03_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCWS94",MZ_PCWS94_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCSR05",MZ_PCSR05_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCSR06",MZ_PCSR06_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCST03",MZ_PCST03_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCST04",MZ_PCST04_qty)
setAtvQty(Product,"eServer_BOM_parts","MZ-PCSR04",MZ_PCSR04_qty)