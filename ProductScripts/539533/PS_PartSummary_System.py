def getAttr(name):
    return Product.Attr(name).GetValue()
esd_Server=getAttr('ES_Displays_Server')
esd_Size=getAttr('ES_Display_Size')
esds_Server=getAttr('ES_Display_Supplier_Server')
es_BOM=Product.Attr('eServer_BOM_parts')
esmobile_required=getAttr("ES_Mobile_Server_Nodes_required")
esmobile_Display=getAttr("ES_Display_Size_Mobile_Server")
esmobile_Server=getAttr("ES_Display_Supplier_Mobile_Server")
esadditional=getAttr("ES_Additional_Stations_for_eServer")
es_Display=getAttr("ES_Display_size_i")
es_Supplier=getAttr("ES_Node_Supplier_station")

esd_Size_dict={'24 inch NTS DELL':'TP-FPW242','24 inch NTS NEC':'TP-FPW241','27 inch NTS NEC':'TP-FPW271','27 inch NTS DELL':'TP-FPW272'}
partno_lst=[]
partno_qty={}
for i in Product.GetContainerByName("eServer_partsummary_cont").Rows:
    qty,Quant_Mobile,Quant_supplier,tot=0,0,0,0
    if esd_Size in ("24 inch NTS DELL","24 inch NTS NEC","27 inch NTS NEC","27 inch NTS DELL") and esds_Server=="Honeywell" and (int(esd_Server) > 0) :
        pn_Number=esd_Size_dict.get(esd_Size)
        if pn_Number not in partno_lst:
            partno_lst.append(pn_Number)
        a=es_BOM.SelectValues(*partno_lst)
        if i["partnumber"] == pn_Number:
            for bom in es_BOM.SelectedValues:
                if bom.ValueCode==pn_Number and pn_Number in partno_lst:
                    partno_qty[pn_Number]=partno_qty.get(pn_Number,0)+int(esd_Server)
                    qty=partno_qty[pn_Number]
                    bom.Quantity = qty
                    i["CE_Part_Qty"]=str(qty)
                    i["CE_Final_Quantity"]=str(qty)
    else:
        pn_Number=esd_Size_dict.get(esd_Size)
        for bom in es_BOM.SelectedValues:
            if bom.Display==pn_Number:
                bom.IsSelected=False

    if esmobile_Display in ("24 inch NTS DELL","24 inch NTS NEC","27 inch NTS NEC","27 inch NTS DELL") and esmobile_Server=="Honeywell" and esmobile_required=="Yes" :#and esd_Size == esmobile_Display:
        if esmobile_Display:
            pn_Number=esd_Size_dict.get(esmobile_Display)
            if pn_Number not in partno_lst:
                partno_lst.append(pn_Number)
            a=es_BOM.SelectValues(*partno_lst)
            if i["partnumber"] ==pn_Number:
                for bom in es_BOM.SelectedValues:
                    if bom.ValueCode==pn_Number  and pn_Number in partno_lst:
                        Quant_Mobile="1"
                        partno_qty[pn_Number]=partno_qty.get(pn_Number,0)+int(Quant_Mobile)
                        bom.Quantity = partno_qty[pn_Number]
                        i["CE_Part_Qty"] =str(partno_qty[pn_Number])
                        i["CE_Final_Quantity"] = str(partno_qty[pn_Number])
    else:
        if esmobile_Display and esd_Size not in ("24 inch NTS DELL","24 inch NTS NEC","27 inch NTS NEC","27 inch NTS DELL") :
            pn_Number=esd_Size_dict.get(esmobile_Display)
            for bom in es_BOM.SelectedValues:
                if bom.Display==pn_Number:
                    bom.IsSelected=False


    if es_Display in ("24 inch NTS DELL","24 inch NTS NEC","27 inch NTS NEC","27 inch NTS DELL") and es_Supplier=="Honeywell" and esadditional != '0' :#and esd_Size ==es_Display:
        pn_Number=esd_Size_dict.get(es_Display)
        if pn_Number not in partno_lst:
            partno_lst.append(pn_Number)
        BOM_42=es_BOM.SelectValues(*partno_lst)
        if i["partnumber"] ==pn_Number:
            for bom in es_BOM.SelectedValues:
                if bom.ValueCode==pn_Number  and pn_Number in partno_lst:
                    bom.Quantity= int(esadditional)
                    Quant_supplier=str(esadditional)
                    partno_qty[pn_Number]=partno_qty.get(pn_Number,0)+int(Quant_supplier)
                    bom.Quantity = partno_qty[pn_Number]
                    i["CE_Part_Qty"] =  str(partno_qty[pn_Number])
                    i["CE_Final_Quantity"] = str(partno_qty[pn_Number])
    elif esd_Size not in ("24 inch NTS DELL","24 inch NTS NEC","27 inch NTS NEC","27 inch NTS DELL") and esadditional == '0':
        pn_Number=esd_Size_dict.get(es_Display)
        for bom in es_BOM.SelectedValues:
            if bom.Display==pn_Number:
                bom.IsSelected=False