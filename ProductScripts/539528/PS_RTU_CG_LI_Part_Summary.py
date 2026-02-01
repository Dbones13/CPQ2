#import System.Decimal as d
#Log.Info('IN PS_RTU_CG_LI_Part_Summary')
rtu_cont_rows = Product.GetContainerByName('RTU_CG_PartSummary_Cont').Rows
'''cont_r = Product.GetContainerByName('RTU_CG_IO_Container').Rows[0]
cont_r["Number_Segments_FIM4"] = str(d.Ceiling(float(cont_r["FIM_Analog_Input"])/float(cont_r["FIM_devices_segment_withOpen_loop"])))'''
errorFlag = False
for row in rtu_cont_rows:
    finalQuantity = int(row['CE_Final_Quantity'])
    if finalQuantity < 0:
        errorFlag = True
        break
if errorFlag:
    Product.Attr('PartSummaryErrorMsg').AssignValue('True')
else:
    Product.Attr('PartSummaryErrorMsg').AssignValue('False')
    rtu_cont_rows = Product.GetContainerByName('RTU_CG_PartSummary_Cont').Rows
    rtu_li_cont = Product.GetContainerByName('RTU_CG_PartSummary_LI_Cont')
    rtu_li_cont.Rows.Clear()
    for row in rtu_cont_rows:
        part = row['CE_Part_Number']
        quantity = row['CE_Part_Qty']
        part_description = row['CE_Part_Description']
        adjQuantity = row['CE_Adj_Quantity'] if row['CE_Adj_Quantity'] else 0
        comments = row['CE_Comments']
        finalQuantity = int(row['CE_Final_Quantity'])
        Trace.Write('Part: ' + str(part))
        Trace.Write('Final Quantity: ' + str(finalQuantity))
        if finalQuantity > 0:
            Trace.Write('Part0: ' + str(part))
            Trace.Write('Final Quantity 0 : ' + str(finalQuantity))
            row = rtu_li_cont.AddNewRow(part, False)
            row.GetColumnByName("CE_Part_Qty").Value = quantity
            row.GetColumnByName("CE_Part_Description").Value = part_description
            row.GetColumnByName("CE_Adj_Quantity").Value = str(adjQuantity)
            row.GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(finalQuantity))
            row.GetColumnByName("CE_Comments").Value = comments
            row.Calculate()