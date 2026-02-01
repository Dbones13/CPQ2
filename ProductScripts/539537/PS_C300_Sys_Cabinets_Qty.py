from math import ceil
C300_cont = Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')    
a = Product.Attr('SerC_CG_Cabinet_Access').GetValue()
#qty1 = int(0)
parts=['CC-CBDD01','51454314-300','51454314-200','51454314-100','CC-CASS11','CC-CADS11','51454314-600','51454314-400','51454314-500','CC-CASS21','CC-CASS41','CC-CASS31']
marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
Marshal_Qty = int(0)
final_qty_R = int(0)
qty1 = int(0)
Marshal_Qty_R = int(0)
qty1_R = int(0)
final_qty = int(0)
if C300_cont.Rows.Count > 0:
    for row in C300_cont.Rows:
        if row['PartNumber'] == "CC-CBDS01":
            qty1 += int(ceil(float(row['Part_Qty'])/2.0))
        elif row['PartNumber'] in parts:
            qty1 += int(row['Part_Qty'])
            Trace.Write(qty1)
        elif  row['PartNumber'] in marshal_parts:
            Marshal_Qty += int(row['Part_Qty']) 
#if  a == 'Single Access':
#     final_qty = int(round(qty1/2,0)+1)
#elif a == 'Dual Access':
#     final_qty = int(qty1)    
Product.Attr('C300_Sys_Cabinets').AssignValue(str(qty1))
Product.Attr('C300_Marshal_Cabinets').AssignValue(str(Marshal_Qty))
#Remote Group
'''C300remote_cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
for row in C300remote_cont.Rows:
    uoc_remote_cont = row.Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    M = row.Product.Attr('SerC_RG_Cabinet_Access').GetValue()

    for r in uoc_remote_cont.Rows:
        if r['PartNumber'] == 'CC-CBDD01':
            qty1_R += int(r['Part_Qty'])
        elif r['PartNumber'] == 'CC-CBDS01':
            qty1_R += int(r['Part_Qty'])
        elif  r['PartNumber'] in marshal_parts:
            Marshal_Qty_R += int(r['Part_Qty'])
    if  M == 'Single Access':
        final_qty_R = int(round(qty1_R/2,0)+1)
    elif M == 'Dual Access':
        final_qty_R = int(qty1_R)      
Product.Attr('C300_Sys_Cabinets_RG').AssignValue(str(final_qty_R))
Product.Attr('C300_Marshal_Cabinets_RG').AssignValue(str(Marshal_Qty_R))'''