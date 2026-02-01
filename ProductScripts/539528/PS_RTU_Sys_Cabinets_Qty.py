# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)
rtu_cont = Product.GetContainerByName('RTU_CG_PartSummary_Cont')
cab_cont = Product.GetContainerByName('RTU_CG_Cabinet_Cont')
marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
from math import ceil
Marshal_Qty = qty1 = int(0)
final_qty = int(0)
for row in rtu_cont.Rows:
    if row['CE_Part_Number'] == 'CC-CBDD01':
        qty1 += int(row['CE_Part_Qty'])
    elif row['CE_Part_Number'] == 'CC-CBDS01':
        qty1 += int(row['CE_Part_Qty'])
    elif  row['CE_Part_Number'] in marshal_parts:
        Marshal_Qty += int(row['CE_Part_Qty'])

for val in cab_cont.Rows:
    if  val['Cabinet_Type'] == 'One':
        final_qty = int(ceil(float(qty1)/2.0)) #int(ceil(float(qty1)/2.0))
    elif val['Cabinet_Type'] == 'Dual':
        final_qty = int(qty1)    
Product.Attr('RTU_Num_of_Sys_Cabinets').AssignValue(str(final_qty))
Product.Attr('RTU_Marshal_Cabinet_Qty').AssignValue(str(Marshal_Qty))