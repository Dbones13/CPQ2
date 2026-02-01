marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
from math import ceil
qty1_R = Marshal_Qty_R = int(0)
uoc_remote_cont = Product.GetContainerByName('UOC_RG_PartSummary_Cont')

for r in uoc_remote_cont.Rows:
    if r['CE_Part_Number'] == 'CC-CBDD01':
        qty1_R += int(r['CE_Part_Qty'])
    elif r['CE_Part_Number'] == 'CC-CBDS01':
        qty1_R += int(ceil(float(r['CE_Part_Qty'])/2.0))
    elif  r['CE_Part_Number'] in marshal_parts:
        Marshal_Qty_R += int(r['CE_Part_Qty'])
Product.Attr('staging_Num_of_System_cabinet_UOC_remote_group').AssignValue(str(qty1_R))
Product.Attr('staging_Num_of_marshal_cabinet_UOC_remote_group').AssignValue(str(Marshal_Qty_R))
#https://honeywell.atlassian.net/browse/CXCPQ-117941
io=0
cont=Product.GetContainerByName("UOC_RG_UIO_Cont")
if cont.Rows.Count >0:
    for col in cont.Rows[0].Columns :
        if col.Value!='':
            io+=int(col.Value)
Product.Attr('C300_Exp_Labor_Uni_qntCG').AssignValue(str(io))