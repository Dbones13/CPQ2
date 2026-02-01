#CXCPQ-50813
def pulseInputQuestions(Product):
    pulseQues = ['Series-C: Pulse Input (8) Single Channel (0-5000)','Series-C: Pulse Input (4) Dual Channel (0-5000)', 'Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)']
    ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    if Product.Name == 'Series-C Control Group':
        cont = Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2')
    elif Product.Name == 'Series-C Remote Group':
        cont = Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont2')
    if cont.Rows.Count > 0:
        row_list = []
        rows_to_delete = []
        for row in cont.Rows:
            if row['IO_Type'] in pulseQues:
                row_list.append(row['IO_Type'])
                rows_to_delete.append(row.RowIndex)
        if ioFamilyType == 'Series C':
            if len(row_list) < 3:
                for q in pulseQues:
                    addRow = True
                    if len(row_list) > 0:
                        if q in row_list:
                            addRow = False
                    if addRow:
                        newRow = cont.AddNewRow('CONT_Enhanced_Function_I/O2_for_Series-C_Group_cpq', False)
                        newRow['IO_Type'] = str(q)
                        newRow.Product.Attr('IO_Type').AssignValue(str(newRow["IO_Type"]))
                        newRow.Product.ApplyRules()
                        newRow.Calculate()
                cont.Calculate()
        elif ioFamilyType == 'Turbomachinery':
            rows_to_delete.sort(reverse=True)
            for x in rows_to_delete:
                cont.DeleteRow(x)