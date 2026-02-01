sum_scada_points = 0
scada_cont = Product.GetContainerByName('Scada_CCR_Unit_Cont')
if scada_cont.Rows.Count > 0:
    for row in scada_cont.Rows:
        ccr_cont1 = row.Product.GetContainerByName('Modbus/OPC Interfaces')
        for row1 in ccr_cont1.Rows:
            sum_scada_points += int(row1['SCADA Points']) if str(row1['SCADA Points']).isdigit() else 0
        ccr_cont2 = row.Product.GetContainerByName('OPC Application Instances')
        for row2 in ccr_cont2.Rows:
            sum_scada_points += int(row2['SCADA Points']) if str(row2['SCADA Points']).isdigit() else 0
        ccr_cont3 = row.Product.GetContainerByName('IEC/DNP3 Interfaces')
        for row3 in ccr_cont3.Rows:
            sum_scada_points += int(row3['SCADA Points']) if str(row3['SCADA Points']).isdigit() else 0
        ccr_cont4 = row.Product.GetContainerByName('Leak Detection System Interfaces')
        for row4 in ccr_cont4.Rows:
            sum_scada_points += int(row4['SCADA Points']) if str(row4['SCADA Points']).isdigit() else 0
        ccr_cont5 = row.Product.GetContainerByName('Allen-Bradley/Siemens Interfaces')
        for row5 in ccr_cont5.Rows:
            sum_scada_points += int(row5['SCADA Points']) if str(row5['SCADA Points']).isdigit() else 0
        ccr_cont6 = row.Product.GetContainerByName('Flow Computer Interfaces')
        for row6 in ccr_cont6.Rows:
            sum_scada_points += int(row6['SCADA Points']) if str(row6['SCADA Points']).isdigit() else 0
        ccr_cont7 = row.Product.GetContainerByName('GE_OR_OMNI_Interfaces')
        for row7 in ccr_cont7.Rows:
            sum_scada_points += int(row7['SCADA_Points']) if str(row7['SCADA_Points']).isdigit() else 0
        ccr_cont8 = row.Product.GetContainerByName('Miscellaneous Interfaces')
        for row8 in ccr_cont8.Rows:
            sum_scada_points += int(row8['SCADA Points']) if str(row8['SCADA Points']).isdigit() else 0
Product.Attr('Number_of_SCADA_points').AssignValue(str(sum_scada_points))