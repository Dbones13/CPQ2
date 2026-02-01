SM_remote_cont = Product.GetContainerByName('SM_RG_PartSummary_Cont')
SM_rem_cab_cont = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
from math import ceil
marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
parts=['CC-CBDS01','CC-CBDD01','FS-BCU-0036','FS-BCU-0038']
final_qty_R = qty1_R = int(0)
Marshal_Qty_R = int(0)
for r in SM_remote_cont.Rows:
    if r['CE_Part_Number'] in ['CC-CBDS01','FS-BCU-0038']:
        qty1_R += int(ceil(float(r['CE_Part_Qty'])/2.0))
    elif r['CE_Part_Number'] in ['CC-CBDD01','FS-BCU-0036']:
        qty1_R += int(r['CE_Part_Qty'])
    elif r['CE_Part_Number'] in marshal_parts:
        Marshal_Qty_R += int(r['CE_Part_Qty'])

Product.Attr('staging_Num_of_marshal_cabinet_SM_remote_group').AssignValue(str(Marshal_Qty_R))
Product.Attr('staging_Num_of_System_cabinet_SM_remote_group').AssignValue(str(qty1_R))