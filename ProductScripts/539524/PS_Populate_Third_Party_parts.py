def delete_part(cont, parts_to_delete):
    parts_to_delete.sort(reverse=True)
    for part in parts_to_delete:
        Trace.Write(part)
        cont.DeleteRow(part)
third_party_parts={}
third_party_part_description={}
for row in Product.GetContainerByName('CCR_Third_Party_Parts').Rows:
    if third_party_parts.get(row['PartNumber']):
        third_party_parts[row['PartNumber']] = int(third_party_parts[row['PartNumber']]) + (int(row['Quantity']) if row['Quantity'] != '' else 0)
    else:
        if 1:
            #if row['Quantity'] not in ('',0,'0'):
            third_party_parts[row['PartNumber']] = int(row['Quantity']) if row['Quantity'] != '' else 0
            third_party_part_description[row['PartNumber']] = row['Description']
            Trace.Write(row['PartNumber']+'==='+str(int(third_party_parts[row['PartNumber']]) + (int(row['Quantity']) if row['Quantity'] != '' else 0)))
scada_3rd_party_partsummary_cont = Product.GetContainerByName('SCADA_CG_Part_Summary_Cont_3rd_Party')
final_part_Summary = dict(list(third_party_parts.items()))
part_delete = []
for key in third_party_parts:
    flag = True
    for row in scada_3rd_party_partsummary_cont.Rows:
        if row['PartNumber'] == key:
            Trace.Write(key)
            if final_part_Summary[key] == 0:
                part_delete.append(row.RowIndex)
            row['Part_Qty'] = str(final_part_Summary[row['PartNumber']])
            Trace.Write(str(str(final_part_Summary[row['PartNumber']])))
            row['Final_Quantity'] = str(final_part_Summary[key])
            row['Part_Description'] = str(third_party_part_description[key])
            row.Calculate()
delete_part(scada_3rd_party_partsummary_cont, part_delete)
scada_3rd_party_partsummary_cont.Calculate()