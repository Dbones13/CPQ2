from math import ceil
Sm_cont = Product.GetContainerByName('SM_CG_PartSummary_Cont')  
sm_cab_cont = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
Marshal_Qty = int(0)
final_qty_R = int(0)
Marshal_Qty_R = int(0)
qty1 = int(0)
final_qty = int(0)
qty1_R = int(0)
parts=['CC-CBDD01','FS-BCU-0036']
for row in Sm_cont.Rows:
    if row['CE_Part_Number'] in ['CC-CBDS01','FS-BCU-0038']:
        qty1 += int(ceil(float(row['CE_Part_Qty'])/2.0))
    if row['CE_Part_Number'] in parts:
        qty1 += int(row['CE_Part_Qty'])
    elif  row['CE_Part_Number'] in  marshal_parts:
        Marshal_Qty += int(row['CE_Part_Qty'])
'''
for val in sm_cab_cont.Rows:
    if val['Cabinet_Access'] == 'Dual_Access':
        final_qty = int(qty1)
    elif val['Cabinet_Access'] == 'Single_Access':
        final_qty = int(round(qty1/2,0)+1)
'''
Product.Attr('SM_Sys_Cabinets').AssignValue(str(qty1))
Product.Attr('SM_Marshal_Cabinets').AssignValue(str(Marshal_Qty))
#Remote Group:
'''
SMremote_cont = Product.GetContainerByName('SM_RemoteGroup_Cont')
for row in SMremote_cont.Rows:
    SM_remote_cont = row.Product.GetContainerByName('SM_RG_PartSummary_Cont')
    SM_rem_cab_cont = row.Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')

    for r in SM_remote_cont.Rows:
        if r['CE_Part_Number'] in parts:
            qty1_R += int(r['CE_Part_Qty'])
        elif r['CE_Part_Number'] in marshal_parts:
            Marshal_Qty_R += int(r['CE_Part_Qty'])
    for valRG in  SM_rem_cab_cont.Rows:       
        if  valRG['Cabinet_Access'] == 'Single_Access':
            final_qty_R = int(round(qty1_R/2,0)+1)
        elif  valRG['Cabinet_Access'] == 'Dual_Access':
            final_qty_R = int(qty1_R)      
Product.Attr('SM_Sys_Cabinets_RG').AssignValue(str(final_qty_R))
Product.Attr('SM_Marshal_Cabinets_RG').AssignValue(str(Marshal_Qty_R))
'''