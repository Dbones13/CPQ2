uoc_cont = Product.GetContainerByName('UOC_CG_PartSummary_Cont')
cab_cont = Product.GetContainerByName('UOC_CG_Cabinet_Cont')
from math import ceil
marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
Marshal_Qty = int(0)
final_qty_R = int(0)
qty1 = int(0)
Marshal_Qty_R = int(0)
qty1_R = int(0)
final_qty = int(0)
for row in uoc_cont.Rows:
    if row['CE_Part_Number'] == 'CC-CBDD01':
        qty1 += int(row['CE_Part_Qty'])
    elif row['CE_Part_Number'] == 'CC-CBDS01':
        qty1 += int(row['CE_Part_Qty'])
    elif  row['CE_Part_Number'] in marshal_parts:
        Marshal_Qty += int(row['CE_Part_Qty'])

for val in cab_cont.Rows:
    if  val['UOC_Cabinet_Type'] == 'One':
        final_qty = int(ceil(float(qty1)/2.0))
    elif val['UOC_Cabinet_Type'] == 'Dual':
        final_qty = int(qty1)    
Product.Attr('UOC_Num_of_Sys_Cabinets').AssignValue(str(final_qty))
Product.Attr('UOC_Marshal_Cabinet_Qty').AssignValue(str(Marshal_Qty))
#Remote Group
'''uocremote_cont = Product.GetContainerByName('UOC_RemoteGroup_Cont')
for row in uocremote_cont.Rows:
    uoc_remote_cont = row.Product.GetContainerByName('UOC_RG_PartSummary_Cont')
    uoc_cab_remote_cont = row.Product.GetContainerByName('UOC_RG_Cabinet_Cont')
    for r in uoc_remote_cont.Rows:
        if r['CE_Part_Number'] == 'CC-CBDD01':
            qty1_R += int(r['CE_Part_Qty'])
        elif r['CE_Part_Number'] == 'CC-CBDS01':
            qty1_R += int(ceil(float(r['CE_Part_Qty'])/2.0))
        elif  r['CE_Part_Number'] in marshal_parts:
            Marshal_Qty_R += int(r['CE_Part_Qty'])
    #for val in uoc_cab_remote_cont.Rows:
        #if  val['UOC_Cabinet_Type'] == 'One':
            #final_qty_R = int(round(qty1_R/2,0)+1)
        #elif val['UOC_Cabinet_Type'] == 'Dual':
            #final_qty_R = int(qty1_R)            
Product.Attr('UOC_Num_of_Sys_Cabinets_RG').AssignValue(str(qty1_R))
Product.Attr('UOC_Marshal_Cabinet_Qty_RG').AssignValue(str(Marshal_Qty_R))'''
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<CTX(Product.RootProduct.PartNumber)>')
if isR2Qquote and Checkproduct == "Migration":
    uocremote_cont = Product.GetContainerByName('UOC_RemoteGroup_Cont')
    for row in uocremote_cont.Rows:
        row.Product.Attr("UOC_RG_Name").AssignValue(row["Remote Group Name"])
#https://honeywell.atlassian.net/browse/CXCPQ-117941
io=iorg=0
cont=Product.GetContainerByName("UOC_CG_UIO_Cont")
if cont.Rows.Count >0:
    for col in cont.Rows[0].Columns :
        if col.Value!='':
            io+=int(col.Value)
cont2=Product.GetContainerByName("UOC_RemoteGroup_Cont")
if cont2.Rows.Count >0:
    for row in cont2.Rows:
        if row['C300_Exp_Labor_Uni_qntCG'] !='':
            iorg+=int(row['C300_Exp_Labor_Uni_qntCG'])
Product.Attr('C300_Exp_Labor_Uni_qntCG').AssignValue(str(io+iorg))