if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
    C300_remote_cont = Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    a = Product.Attr('SerC_RG_Cabinet_Access').GetValue()
    from math import ceil
    marshal_parts = ['MCD-PS-3I-672','MCD-PS-3I-672IS','MCD-PS-2P-488','MCD-PS-2P-488IS','MCD-PS-2I-488','MCD-PS-2I-488IS','MCD-ES-3I-720','MCD-ES-3I-720IS','MCD-ES-2P-480','MCD-ES-2P-480IS','MCD-ES-2I-480','MCD-ES-2I-480IS','MCS-PS-3I-288','MCS-PS-3I-288IS','MCS-PS-2P-192','MCS-PS-2P-192IS','MCS-PS-2I-192','MCS-PS-2I-192IS','MCS-ES-3I-336','MCS-ES-3I-336IS','MCS-ES-2P-224','MCS-ES-2P-224IS','MCS-ES-2I-224','MCS-ES-2I-224IS']
    parts=['CC-CBDD01','51454314-300','51454314-200','51454314-100','CC-CASS11','CC-CADS11','51454314-600','51454314-400','51454314-500','CC-CASS21','CC-CASS41','CC-CASS31']
    final_qty_R = qty1_R = int(0)
    Marshal_Qty_R = int(0)
    for row in C300_remote_cont.Rows:
        if row['PartNumber'] == "CC-CBDS01":
            qty1_R += int(ceil(float(row['Part_Qty'])/2.0))
        elif row['PartNumber'] in parts:
            qty1_R += int(row['Part_Qty'])
        elif row['PartNumber'] in marshal_parts:
            Marshal_Qty_R += int(row['Part_Qty'])  
            #if  a == 'Single Access':
            #     final_qty_R = int(ceil(float(qty1_R )/2.0))
            #elif a == 'Dual Access':
            #     final_qty_R = int(qty1_R)    

            Product.Attr('staging_Num_of_marshal_cabinet_C300_remote_group').AssignValue(str(Marshal_Qty_R ))
            Product.Attr('staging_Num_of_System_cabinet_C300_remote_group').AssignValue(str(qty1_R))