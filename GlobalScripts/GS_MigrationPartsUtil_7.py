import math as m
Cable_Total = int(0)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def cabinetParts(red, nonRed, cabinetNormal, cExtended):
    i = 0
    x = 0
    while(red > 0 or nonRed > 0):
        if i == 0:
            if red >= 8:
                cabinetNormal[7] += 2
                red -= 8
                i += 1
            else:
                if red > 0:
                    cabinetNormal[red-1] += 2
                    x = red
                    red = 0


                if nonRed >= (8-x):
                    cabinetNormal[7] += 1
                    nonRed -= (8-x)
                    x = 0
                    i += 1
                elif red == 0 and nonRed > 0:
                    cabinetNormal[x + nonRed - 1] += 1
                    nonRed = 0
                    x = 0
        elif i == 1 or i == 2:
            if red >= 9:
                cExtended[8] += 2
                red -= 9
                i += 1
            else:
                if red > 0:
                    cExtended[red-1] += 2
                    x = red
                    red = 0


                if nonRed >= (9-x):
                    cExtended[8] += 1
                    nonRed -= (9-x)
                    x = 0
                    i += 1
                elif red == 0 and nonRed > 0:
                    cExtended[x + nonRed - 1] += 1
                    nonRed = 0
                    x = 0
        else:
            if red >= 8:
                cExtended[7] += 2
                red -= 8
                i += 1
            else:
                if red > 0:
                    cExtended[red-1] += 2
                    x = red
                    red = 0


                if nonRed >= (8-x):
                    cExtended[7] += 1
                    nonRed -= (8-x)
                    x = 0
                    i += 1
                elif red == 0 and nonRed > 0:
                    cExtended[x + nonRed - 1] += 1
                    nonRed = 0
                    x = 0

def FSCtoSM_IOparts(product, attrValDict):
    cont1 = product.GetContainerByName("FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations")
    scope_check = product.Attr("MIgration_Scope_Choices").GetValue()
    scope = 0
    if scope_check != "LABOR":
        scope = 1

        contGen = product.GetContainerByName("FSC_to_SM_IO_Migration_General_Information")
        contSet8 = product.GetContainerByName("FSC_SM_IO_SIC_Cable")
        IO_place = 0
        if contGen:
            if scope == 1:
                IO_check = contGen.Rows[0]["FSC_to_SM_IO_Migration_Where_will_the_IOs_be_installed"]
                if IO_check == "Other cabinet":
                    IO_place = 1

        qtyGMDO08 = 0
        qty1624 = 0
        qtyGMLD16 = 0
        qty1024 = 0
        qty1620M = 0
        qty0220M = 0
        qtyTSDI1624 = 0
        qtyTSDI1648 = 0
        qty16UNI = 0
        qty0424 = 0
        qty04UNI = 0
        qty0824 = 0
        #set 1
        qty0003R = 0
        qty0003S = 0
        qtyCab = 0
        qtyTerm1 = 0 
        qtyTerm2 = 0
        #set 5
        cabCheck1 = 0
        cabCheck2 = 0
        rackCheck6 = 0
        #set 4
        qtyCPX11 = 0
        qtyCPX12 = 0
        cabCount = 0
        #set 6
        qtySDI1624 = 0
        qtySDI1648 = 0
        qtySAI1620M = 0
        qtySDO0824 = 0
        qtySAO0220M = 0
        qtyDO1224 = 0
        qtyRO1024 = 0
        qtyDO1624 = 0
        qtySDO04110 = 0
        qtySDO0448 = 0
        qtySDO0424 = 0
        qtySDOL0448 = 0
        qtySDIL1608 = 0
        qtySDOL0424 = 0
        #set 2
        cabinetNormal = [0, 0, 0, 0, 0, 0, 0, 0]
        #set 3
        cExtended = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        #set 8
        qty3 = 0
        qty5 = 0
        qty6 = 0
        qty8 = 0
        qty10 = 0
        qty15 = 0
        qty20 = 0
        qty25 = 0
        qty30 = 0
        
        if cont1:
            for row in cont1.Rows:
                cabinet = getFloat(row['FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack'])
                redRack = getFloat(row['FSC_to_SM_IO_Number_of_IO_Racks'])
                nonRedRack = getFloat(row['NON_RED_FSC_to_SM_IO_Number_of_IO_Racks'])
                #set 6
                qtySDI1624 += ((m.ceil(((getFloat(row['FSC_to_SM_IO_DI_IS_(Eex(i))'])+ getFloat(row['FSC_to_SM_IO_DI_IS_(Eex(ii))']))*4)/16)+ getFloat(row['FSC_to_SM_IO_DI_24VDC_10104/2/1'])+ getFloat(row['FSC_to_SM_IO_DI_24VDC_10104/1/1'])+ getFloat(row['FSC_to_SM_IO_DI_24VDC'])+ getFloat(row['FSC_to_SM_IO_SDI_24VDC']))*2 +m.ceil(((getFloat(row['NON_RED_FSC_to_SM_IO_DI_IS_(Eex(i))'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_IS_(Eex(ii))']))*4)/16)+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC_10104/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC_10104/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDI_24VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC']))
                qtySDI1648 += ((getFloat(row['FSC_to_SM_IO_SDI_48VDC_10101/2/3'])+ getFloat(row['FSC_to_SM_IO_DI_48VDC']))*2 + getFloat(row['NON_RED_FSC_to_SM_IO_DI_48VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDI_48VDC_10101/2/3']))
                qtySAI1620M += (m.ceil(((getFloat(row['FSC_to_SM_IO_AI_4_20mA'])+ getFloat(row['FSC_to_SM_IO_SAI_10102/2/1']))*4)/16)*2 + m.ceil(((getFloat(row['NON_RED_FSC_to_SM_IO_SAI_10102/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_AI_4_20mA']))*4)/16))
                qtySDO0824 += ((getFloat(row['FSC_to_SM_IO_DO_IS_10207/1/1'])+ getFloat(row['FSC_to_SM_IO_SDO_24VDC_10201/2/1'])+ getFloat(row['FSC_to_SM_IO_DO 24VDC_10201/1/1'])+ m.ceil(((getFloat(row['FSC_to_SM_IO_SDOL_220VDC_10214/2/2']) +getFloat(row['FSC_to_SM_IO_SDOL 220VDC_10214/1/2']))*3)/8))*2 +m.ceil(((getFloat(row['NON_RED_FSC_to_SM_IO_SDOL 220VDC_10214/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_220VDC_10214/2/2']))*3)/8)+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_IS_10207/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10201/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO 24VDC_10201/1/1']))
                qtySAO0220M += (getFloat(row['NON_RED_FSC_to_SM_IO_AO_4-20mA_10205/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SAO_10205/2/1']))
                qtyDO1224 += ((getFloat(row['FSC_to_SM_IO_DO_24VDC_10206/1/1'])+ getFloat(row['FSC_to_SM_IO_DO_24VDC_10206/2/1']))*2 + getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10206/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10206/2/1']))
                qtyRO1024 += (m.ceil(((getFloat(row['NON_RED_FSC_to_SM_IO_RO_10208/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_RO_10208/2/1']))*12)/10)+ m.ceil(((getFloat(row['FSC_to_SM_IO_RO_10208/1/1'])+ getFloat(row['FSC_to_SM_IO_RO_10208/2/1']))*12)/10)*2)
                qtyDO1624 += ((getFloat(row['FSC_to_SM_IO_DO_24VDC_10209/1/1'])+ getFloat(row['FSC_to_SM_IO_DO_24VDC_10209/2/1']))*2 + getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10209/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10209/2/1']))
                qtySDO04110 += ((getFloat(row['FSC_to_SM_IO_DO_110VDC_10213/1/1'])+ getFloat(row['FSC_to_SM_IO_SDO_110VDC_10213/2/1']))*2 + getFloat(row['NON_RED_FSC_to_SM_IO_DO_110VDC_10213/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_110VDC_10213/2/1']))
                qtySDO0448 += ((getFloat(row['FSC_to_SM_IO_SD_ 48VDC_10213/1/3'])+ getFloat(row['FSC_to_SM_IO_SDO_48VDC_10213/2/3']))*2 + getFloat(row['NON_RED_FSC_to_SM_IO_SD_ 48VDC_10213/1/3'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_48VDC_10213/2/3']))
                qtySDO0424 += (getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10212/1/1'])*2 + getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2'])+ (getFloat(row['FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1'])+ getFloat(row['FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2'])+ getFloat(row['FSC_to_SM_IO_SDO_24VDC_10215/2/1'])+ getFloat(row['FSC_to_SM_IO_SDO_24VDC_10215/1/1'])+ getFloat(row['FSC_to_SM_IO_DO_24VDC_10212/1/1'])*2)*2)
                qtySDOL0448 += ((getFloat(row['FSC_to_SM_IO_SDOL_48VDC_10216/2/3'])*2) + getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_48VDC_10216/2/3']))#((getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/1/1'])+ getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/2/1']))*2 +  getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/2/1']))
                qtySDIL1608 += (getFloat(row['FSC_to_SM_IO_SDIL_10106/2/1'])*2 + getFloat(row['NON_RED_FSC_to_SM_IO_SDIL_10106/2/1']))
                qtySDOL0424 += ((getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/1/1'])+ getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/2/1']))*2 +  getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/2/1']))
                #set 7
                qtyGMDO08 += (getFloat(row['FSC_to_SM_IO_DO_IS_10207/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_IS_10207/1/1']))
                qty1624 += (getFloat(row['FSC_to_SM_IO_DO_24VDC_10206/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10206/1/1'])+ getFloat(row['FSC_to_SM_IO_DO_24VDC_10209/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10209/1/1']))
                qtyGMLD16 +=  m.ceil(((getFloat(row['FSC_to_SM_IO_DI_IS_(Eex(i))'])+ getFloat(row['FSC_to_SM_IO_DI_IS_(Eex(ii))'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_IS_(Eex(i))'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_IS_(Eex(ii))']))*4)/16)
                qty1024 += m.ceil(((getFloat(row['FSC_to_SM_IO_RO_10208/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_RO_10208/1/1']))*12)/10)
                qty1620M += m.ceil(((getFloat(row['FSC_to_SM_IO_AI_4_20mA'])+ getFloat(row['NON_RED_FSC_to_SM_IO_AI_4_20mA']))* 4)/16)
                qty0220M +=  (getFloat(row['FSC_to_SM_IO_AO_4-20mA_10205/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_AO_4-20mA_10205/1/1']))
                qtyTSDI1624 += (getFloat(row['FSC_to_SM_IO_DI_24VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC'])+ getFloat(row['FSC_to_SM_IO_DI_24VDC_10104/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC_10104/1/1']))
                qtyTSDI1648 += (getFloat(row['FSC_to_SM_IO_DI_48VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_48VDC'])) 
                qty16UNI += (getFloat(row['FSC_to_SM_IO_DI_60VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_60VDC']))
                qty0424 += ((getFloat(row['FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1'])+ getFloat(row['FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2'])+ getFloat(row['FSC_to_SM_IO_SDO_24VDC_10215/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/1/1']))+ (getFloat(row['FSC_to_SM_IO_DO_24VDC_10212/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10212/1/1']))*2)
                qty04UNI += (getFloat(row['FSC_to_SM_IO_DO_110VDC_10213/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_110VDC_10213/1/1'])+ getFloat(row['FSC_to_SM_IO_SDO_60VDC_10213/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/1/2'])+ getFloat(row['FSC_to_SM_IO_SD_ 48VDC_10213/1/3'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SD_ 48VDC_10213/1/3'])+ getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/1/1']))
                qty0824 += ((getFloat(row['FSC_to_SM_IO_DO 24VDC_10201/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO 24VDC_10201/1/1'])) + m.ceil(((getFloat(row['FSC_to_SM_IO_SDOL 220VDC_10214/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL 220VDC_10214/1/2']))*3)/8)) 
                #set 1
                qty0003R += redRack
                qty0003S += nonRedRack
                qtyCab += cabinet
                
                if redRack == 0:
                    qtyTerm2 += 0
                elif redRack > 0 and redRack <= 8:
                    qtyTerm2 += 1
                elif redRack > 8 and redRack <= 17:
                    qtyTerm2 += 2
                elif redRack > 17 and redRack <= 26:
                    qtyTerm2 += 3
                elif redRack > 26 and redRack <= 34:
                    qtyTerm2 += 4

                if nonRedRack == 0:
                    qtyTerm1 += 0
                elif nonRedRack > 0 and nonRedRack <= 8:
                    qtyTerm1 += 1
                elif nonRedRack > 8 and nonRedRack <= 17:
                    qtyTerm1 += 2
                elif nonRedRack > 17 and nonRedRack <= 26:
                    qtyTerm1 += 3
                elif nonRedRack > 26 and nonRedRack <= 34:
                    qtyTerm1 += 4
                
                #set 5
                if IO_place == 1:
                    if cabinet > 1:
                        cabCheck1 += 1
                    if cabinet > 2:
                        cabCheck2 += 1
                    if (nonRedRack + redRack) > 6:
                        rackCheck6 += cabinet
                        
                #set 4
                if cabinet > 1:
                    if (nonRedRack + redRack) > 8:
                        if redRack > 0:
                            qtyCPX11 += 2
                        if nonRedRack > 0:
                            qtyCPX11 += 1
                    if (nonRedRack + redRack) >= 17 and (nonRedRack + redRack) <= 25:
                        if redRack > 0:
                            qtyCPX12 += 2
                        if nonRedRack > 0:
                            qtyCPX12 += 1
                    
                    if (nonRedRack + redRack) > 25 and (nonRedRack + redRack) <= 34:
                        if redRack > 0:
                            qtyCPX12 += 4
                        if nonRedRack > 0:
                            qtyCPX12 += 2
                
                if cabinet > 0:
                    cabCount += 1
                    
                if (nonRedRack + redRack) <= 34 and (nonRedRack + redRack) > 0:
                    cabinetParts(int(redRack), int(nonRedRack), cabinetNormal, cExtended)
                    
        #set 8
        if contSet8:
            for row in contSet8.Rows:
                if row.RowIndex==0:
                    qty3 += getFloat(row["Quantity"])
                elif row.RowIndex==1:
                    qty5 += getFloat(row["Quantity"])
                elif row.RowIndex==2:
                    qty6 += getFloat(row["Quantity"])
                elif row.RowIndex==3:
                    qty8 += getFloat(row["Quantity"])
                elif row.RowIndex==4:
                    qty10 += getFloat(row["Quantity"])
                elif row.RowIndex==5:
                    qty15 += getFloat(row["Quantity"])
                elif row.RowIndex==6:
                    qty20 += getFloat(row["Quantity"])
                elif row.RowIndex==7:
                    qty25 += getFloat(row["Quantity"])
                elif row.RowIndex==8:
                    qty30 += getFloat(row["Quantity"])
        #set 7
        attrValDict["FC-GMDO08"] = qtyGMDO08
        attrValDict["FC-TDO-1624"] = qty1624
        attrValDict["FC-GMLD16"] = qtyGMLD16
        attrValDict["FC-TRO-1024"] = qty1024
        attrValDict["FC-TSAI-1620M"] = qty1620M
        attrValDict["FC-TSAO-0220M"] = qty0220M
        attrValDict["FC-TSDI-1624"] = qtyTSDI1624
        attrValDict["FC-TSDI-1648"] = qtyTSDI1648
        attrValDict["FC-TSDI-16UNI"] = qty16UNI
        attrValDict["FC-TSDO-0424"] = qty0424
        attrValDict["FC-TSDO-04UNI"] = qty04UNI
        attrValDict["FC-TSDO-0824"] = qty0824
        Cable_Total = qtyGMDO08+qty1624+qtyGMLD16+qty1024+qty1620M+qty0220M+qtyTSDI1624+qtyTSDI1648+qty16UNI+qty0424+qty04UNI+qty0824
        product.Attr('FSC_SM_IO_Total_ Calculated_SIC_cables').AssignValue(str(Cable_Total))
        #set 1
        attrValDict["FC-IOCHAS-0003R"] = qty0003R
        attrValDict["FC-IOCHAS-0003S"] = qty0003S
        attrValDict["FS-PDC-IOR05A"] = qty0003R
        attrValDict["FS-PDC-IOS05A"] = qty0003S
        attrValDict["FS-PDC-IOSET"] = qty0003S + qty0003R
        attrValDict["FS-IOBUS-FSC-R"] = qtyCab*2
        if qtyCab > 0:
            attrValDict["FS-IOBUS-FSCX-R"] = (qtyCab - cabCount)*2
        else:
            attrValDict["FS-IOBUS-FSCX-R"] = 0
            
        attrValDict["FC-TERM-0002"] = qtyTerm2
        attrValDict["FC-TERM-0001"] = qtyTerm1

        #set 5
        if IO_place == 1:
            attrValDict["FC-PDB-0824P"] = qtyCab
            attrValDict["FC-PDB-IO05"] = qtyCab
            attrValDict["FC-PSU-240516"] = 2 * cabCount
            attrValDict["FC-PSU-UNI2450U"] =  2 * cabCount
            attrValDict["FS-PDC-FTA24P"] = qtyCab * 2
            attrValDict["FS-PDC-CPSET"] = 1 * cabCount
            attrValDict["FC-PDB-CPX05"] = 1 * cabCheck1
            attrValDict["FS-PDC-CPX05"] = 3 * cabCheck1
            attrValDict["FS-PDC-IOX05-1"] = 3 * cabCheck1
            attrValDict["FS-PDC-IOX05-2"] = 3 * cabCheck2
            attrValDict["4070572"] = rackCheck6
            attrValDict["FS-MB-0001"] = rackCheck6
            attrValDict["FS-PDC-MB24-1P"] = rackCheck6

        #set 4
        attrValDict["FS-IOBUS-CPX11"] = qtyCPX11
        attrValDict["FS-IOBUS-CPX12"] = qtyCPX12
        attrValDict["10312/1/1"] = cabCount
        attrValDict["4212118"] = cabCount * 2
        
        
        #set 6
        attrValDict["FC-SDI-1624"] = qtySDI1624
        attrValDict["FC-SDI-1648"] = qtySDI1648
        attrValDict["FC-SAI-1620M"] = qtySAI1620M
        attrValDict["FC-SDO-0824"] = qtySDO0824
        attrValDict["FC-SAO-0220M"] = qtySAO0220M
        attrValDict["FC-DO-1224"] = qtyDO1224
        attrValDict["FC-RO-1024"] = qtyRO1024
        attrValDict["FC-DO-1624"] = qtyDO1624
        attrValDict["FC-SDO-04110"] = qtySDO04110
        attrValDict["FC-SDO-0448"] = qtySDO0448
        attrValDict["FC-SDO-0424"] = qtySDO0424
        attrValDict["FC-SDOL-0448"] = qtySDOL0448
        attrValDict["FC-SDIL-1608"] = qtySDIL1608
        attrValDict["FC-SDOL-0424"] = qtySDOL0424
        
        #set 2
        attrValDict["FS-IOBUS-CPIO1"] = cabinetNormal[0]
        attrValDict["FS-IOBUS-CPIO2"] = cabinetNormal[1]
        attrValDict["FS-IOBUS-CPIO3"] = cabinetNormal[2]
        attrValDict["FS-IOBUS-CPIO4"] = cabinetNormal[3]
        attrValDict["FS-IOBUS-CPIO5"] = cabinetNormal[4]
        attrValDict["FS-IOBUS-CPIO6"] = cabinetNormal[5]
        attrValDict["FS-IOBUS-CPIO7"] = cabinetNormal[6]
        attrValDict["FS-IOBUS-CPIO8"] = cabinetNormal[7]

        
        #set 3
        attrValDict["FS-IOBUS-CPIOX1"] = cExtended[0]
        attrValDict["FS-IOBUS-CPIOX2"] = cExtended[1]
        attrValDict["FS-IOBUS-CPIOX3"] = cExtended[2]
        attrValDict["FS-IOBUS-CPIOX4"] = cExtended[3]
        attrValDict["FS-IOBUS-CPIOX5"] = cExtended[4]
        attrValDict["FS-IOBUS-CPIOX6"] = cExtended[5]
        attrValDict["FS-IOBUS-CPIOX7"] = cExtended[6]
        attrValDict["FS-IOBUS-CPIOX8"] = cExtended[7]
        attrValDict["FS-IOBUS-CPIOX9"] = cExtended[8]
        
        #set 8
        attrValDict["FS-SICC-0001/L3"] = qty3
        attrValDict["FS-SICC-0001/L5"] = qty5
        attrValDict["FS-SICC-0001/L6"] = qty6
        attrValDict["FS-SICC-0001/L8"] = qty8
        attrValDict["FS-SICC-0001/L10"] = qty10
        attrValDict["FS-SICC-0001/L15"] = qty15
        attrValDict["FS-SICC-0001/L20"] = qty20
        attrValDict["FS-SICC-0001/L25"] = qty25
        attrValDict["FS-SICC-0001/L30"] = qty30

def cal10k(value):
    list1 = ["10k","5k","2k","1k","100"]
    partDict = {}
    for x in list1:
        partDict[x]=0
    if 9900<value<= 10000:
        partDict["10k"] = 1
    else:
        partDict["10k"] =  m.floor(value/10000)
        if 4900 < value<=5000 or 4900 < (value -partDict["10k"]*10000)<=5000:
            partDict["5k"] =1
        else:
            partDict["5k"] = m.floor((value -partDict["10k"]*10000)/5000)
            if 3900 < value<=4000 or 3900 < (value-partDict["10k"]*10000-partDict["5k"]*5000)<=4000:
                partDict["2k"] =2
            elif 1900 < value<=2000 or 1900 < (value-partDict["10k"]*10000-partDict["5k"]*5000)<=2000:
                partDict["2k"] =1
            else:
                partDict["2k"] =m.floor((value-partDict["10k"]*10000-partDict["5k"]*5000)/2000)
                if 900 < value<=1000 or 900 < (value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000)<=1000:
                    partDict["1k"] =1
                else:
                    partDict["1k"] =m.floor((value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000)/1000)
                    partDict["100"] =m.ceil((value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000-partDict["1k"]*1000)/100)
    return partDict
def updateAttrDictWithTPA(product, attDict,Quote):

    ConremoteView= getFloat(product.Attr('TPA_How_many_Concurrent_remote_view_operation_in_RHS_session').GetValue())
    ssHMIvirt= getFloat(product.Attr('TPA_How_many_SINGLE_screen_HMI_in_virtualized_desk_configuration_are_in_total').GetValue())
    dsHMIvirt= getFloat(product.Attr('TPA_How_many_DUAL_screen_HMI_in_virtualized_desk_configuration_are_in_total').GetValue())
    qsHMIvirt= getFloat(product.Attr('TPA_How_many_QUAD_screen_HMI_in_virtualized_desk_configuration_are_in_total').GetValue())
    ssHMIcab= getFloat(product.Attr('TPA_How_many_SINGLE_screen_physical_HMI_in_CABINET_are_required').GetValue())
    dsHMIcab= getFloat(product.Attr('TPA_How_many_DUAL_screen_physical_HMI_in_CABINET_are_required').GetValue())
    qsHMIcab= getFloat(product.Attr('TPA_How_many_QUAD_screen_physical_HMI_in_CABINET_are_required').GetValue())
    appBlocks= getFloat(product.Attr('TPA_Count_of_application_blocks_in_department').GetValue())
    multiWindowLic= getFloat(product.Attr('TPA_How_many_multi_window_licenses_are_currently_licensed_in_existing_PMD').GetValue())
    OPCcomm= getFloat(product.Attr('TPA_How_many_existing_OPC_communication_partners_direct_to_DCS_No_PHD_available_or_data_is_not_in_PHD_or_OPC_data_is_used_for_controls').GetValue())
    MDCont= getFloat(product.Attr('TPA_How_many_MD_control_packages_are_done_in_TPA_PMD').GetValue())
    CDCont= getFloat(product.Attr('TPA_How_many_CD_control_packages_are_done_in_TPA_PMD').GetValue())
    VPMDSys= product.Attr('TPA_Non-virtualized_or_virtualized_PMD_system').GetValue()
    mainMSID= product.Attr('TPA_Is_this_the_main_MSID_system').GetValue()
    sepDepart= getFloat(product.Attr('TPA_How_many_separate_departments_systems_are_under_migration').GetValue())
    PMDserType= product.Attr('TPA_PMD_server_type_required').GetValue()
    CM_EWS= getFloat(product.Attr('TPA_How_many_cabinet_mounted_EWS_DxMs_are_in_total').GetValue())
    VDM_EWS= getFloat(product.Attr('TPA_How_many_virtualized_desk_mounted_EWS_DxMs_are_in_total').GetValue())
    AmtFiberOptic= getFloat(product.Attr('TPA_Amount_of_fiber_optic_convertters_GBICs_required').GetValue())
    NonRedFEC_DP= getFloat(product.Attr('TPA_How_many_new_Non_Redundant_FCE_controllers_DP_are_delivered_in_migration').GetValue())
    NonRedFEC_PN= getFloat(product.Attr('TPA_How_many_new_Non_Redundant_FCE_controllers_PN_are_delivered_in_migration').GetValue())
    RedFCE_DP= getFloat(product.Attr('TPA_How_many_new_redundant_FCE_controllers_are_delivered_in_migration').GetValue())
    sepFCEcabinet= getFloat(product.Attr('TPA_How_many_separate_FCE_cabinets_are_required').GetValue())
    SWI_BOU_16UIO= getFloat(product.Attr('TPA_Total_Number_of_SWI_and_BOU_cards_to_be_replaced').GetValue())
    SWI_BOU_16UIO_UMS= getFloat(product.Attr('TPA_Total_Number_of_SWI_and_BOU_cards_to_be_replaced_with_16_ch_UIO_and_Universal_Marshalling_Module').GetValue())
    SWI_32BI= getFloat(product.Attr('TPA_Total_Number_of_SWI_cards_to_be_combined_and_replaced').GetValue())
    BOU_32BO= getFloat(product.Attr('TPA_Total_Number_of_BOU_cards_to_be_combined_replaced').GetValue())
    MSI_32BI= getFloat(product.Attr('TPA_Total_Number_of_MSI_cards_to_be_replaced').GetValue())
    MAI_ACO_16UIO= getFloat(product.Attr('TPA_Total_Number_of_MAI_ACO_cards_to_be_replaced').GetValue())
    MAI_2x8UAI= getFloat(product.Attr('TPA_Total_Number_of_MAI_with_active_field_AIs_to_be_replaced').GetValue())
    MAI_ACO_16UIO_UMS= getFloat(product.Attr('TPA_Total_Number_of_MAI_and_ACO_cards_to_be_replaced_with_16_ch_UIO_and_Universal_Marshalling_Module').GetValue())
    PBI_16DI= getFloat(product.Attr('TPA_Total_Number_of_PBI_cards_to_be_replaced').GetValue())
    PB0_8DO= getFloat(product.Attr('TPA_Total_Number_of_PB0_cards_to_be_replaced').GetValue())

    UseOnlyCE900= product.Attr('TPA_Use_only_single_CE900_rack_in_KIT_assembly').GetValue()
    TpaRacksReplace= getFloat(product.Attr('TPA_Total_number_of_TPA_Racks_to_be_replaced_with_CE900').GetValue())
    AIchannelUMS= getFloat(product.Attr('TPA_Number_of_AI_channels_which_are_field_powered_wihtout_UMS').GetValue())
    migratingSyst= product.Attr('TPA_What_system_are_we_migrating').GetValue()
    flexLicenses= getFloat(product.Attr('TPA_How_many_flex_licenses_are_currently_licensed_in_existing_PMD').GetValue())
    HMI_DxMLCDHon= product.Attr('TPA_Are_HMI_and_DxM_LCD_displays_in_Honeywell_scope_of_supply').GetValue()
    EBR_NAS= product.Attr('TPA_Include_EBR_and_NAS').GetValue()
    DCS_Alarm= product.Attr('TPA_DCS_Alarm_&_Event_information_link_required').GetValue()
    processScadaPoint= getFloat(product.Attr('TPA_How_many_process_scada_points_are_licensed_currently_in_existing_PMD').GetValue())
    addNewSwitch= getFloat(product.Attr('TPA_How_many_additional_new_replaced_switches_are_required').GetValue())
    serialLinksSupported= getFloat(product.Attr('TPA_Existing_serial_links_with_supported_protocol_which_will_be_redone_with_Serial_Device_Driver').GetValue())
    serialLinksUnsupported= getFloat(product.Attr('TPA_Existing_serial_links_with_unsupported_protocol_which_will_be_redone_with_Serial_Device_Driver_Profibus_or_Profinet').GetValue())
    XPRs_VPRs= getFloat(product.Attr('TPA_How_many_XPRs_VPRs_which_has_IO_in_same_rack_are_in_the_system').GetValue())
    RedPowerSupplies= product.Attr('TPA_Redundant_power_supplies_required').GetValue()
    CE900connt_UI= product.Attr('TPA_CE900_connection_method_to_FCE').GetValue()
    GI_iso_AI_AO= getFloat(product.Attr('TPA_Number_of_GI_isolators_for_AI_AO_in_UMS').GetValue())
    GI_iso_DI_DO= getFloat(product.Attr('TPA_Number_of_GI_isolators_for_DI_DO_in_UMS').GetValue())
    DSA_community= getFloat(product.Attr('TPA_How_many_PMD_systems_need_to_publish_DSA_data_in_DSA_community').GetValue())
   
    sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
    
    TotalPhysStationTPA = ConremoteView+ssHMIvirt+dsHMIvirt+qsHMIvirt+ssHMIcab+dsHMIcab+qsHMIcab
    TotalPhysStationPMD = ssHMIvirt+dsHMIvirt+qsHMIvirt+ssHMIcab+dsHMIcab+qsHMIcab
    TotalProcessPoint =100 * m.ceil((appBlocks*0.005))
    OPCclient = OPCcomm +m.ceil((MDCont+CDCont)/10000)
    VirtHMIworkstn = ssHMIvirt+dsHMIvirt+qsHMIvirt if VPMDSys =="Virtualized" else 0
    VirtRHSser = m.ceil(ConremoteView/10) if VPMDSys =="Virtualized" else 0
    if VPMDSys =="Virtualized" and mainMSID =="Main MSID system" and sepDepart!=0:
        if PMDserType =="Redundant":
            VirtPMDser =2
        else:
            VirtPMDser=1
    else:
        VirtPMDser = 0
    VirtWorkstation = CM_EWS+VDM_EWS if VPMDSys =="Virtualized" else 0
    NetworkBasic = 1  if mainMSID =="Main MSID system" and sepDepart == 1 else 0
    NetworkExpand =1  if sepDepart>1 else 0
    Smallfirewall =1 if NetworkBasic == 1 and VPMDSys == "Non Virtualized" else 0
    Largefirewall =1 if NetworkExpand == 1 or VPMDSys == "Virtualized" else 0
    DSSwitches = 2 + m.floor(AmtFiberOptic/8.01) *2
    SUnitDSSwitches = DSSwitches if DSSwitches >2 else 0
    L25L35Switches =2 if NetworkExpand !=0 or VPMDSys =="Virtualized" else 0
    SUnitL25L35Switches = L25L35Switches if L25L35Switches >=2 else 0
    #parts
    PDCFFCE22 = NonRedFEC_DP +RedFCE_DP*2
    PDCFFCE31 = (NonRedFEC_PN)
    #parts
    RackForTwoPMD_FCE_Cont = m.ceil((PDCFFCE22+PDCFFCE31)/2)
    max16or20 = m.ceil((RackForTwoPMD_FCE_Cont*2 -8)/20) if (RackForTwoPMD_FCE_Cont *2) >8 else 0
    max16or20+= sepFCEcabinet

    CE900_IOcards = SWI_BOU_16UIO+SWI_BOU_16UIO_UMS +m.ceil(SWI_32BI/2) +m.ceil(BOU_32BO/2)+MSI_32BI+MAI_ACO_16UIO+MAI_2x8UAI+MAI_ACO_16UIO_UMS+PBI_16DI+PB0_8DO
    CE900_IOracks = m.ceil(CE900_IOcards/8)
    UMSmodulesCabinet = SWI_BOU_16UIO_UMS+MAI_ACO_16UIO_UMS
    CE900racksCabinet = CE900_IOracks - TpaRacksReplace if UseOnlyCE900 == "Single" and CE900_IOracks >TpaRacksReplace else max((CE900_IOracks - TpaRacksReplace*2),0)
    NewCabinets_1 = 3 if UMSmodulesCabinet==0 else m.floor((5/21)*UMSmodulesCabinet)
    NewCabinets_2 = 3 if UMSmodulesCabinet==0 else m.floor((5/25)*UMSmodulesCabinet)
    NewCabinets = m.ceil((CE900racksCabinet +NewCabinets_1 +NewCabinets_2)/10)
    I_O_Replaced = (SWI_BOU_16UIO+SWI_32BI+BOU_32BO+PBI_16DI)*16 + (MSI_32BI)*24 + (MAI_ACO_16UIO+MAI_2x8UAI+AIchannelUMS)*10 + PB0_8DO*8
    DInput24VDC32Ch = m.ceil(SWI_32BI/2)+ MSI_32BI
    DOutput24VDC32Ch = m.ceil(BOU_32BO/2)
    UniversalIOmodules = MAI_ACO_16UIO +SWI_BOU_16UIO+ SWI_BOU_16UIO_UMS+MAI_ACO_16UIO_UMS
    DiscreteIOpoints = PB0_8DO*8 + PBI_16DI*16+ (DInput24VDC32Ch+DOutput24VDC32Ch)*32 +SWI_BOU_16UIO*16 if I_O_Replaced>0 else 0
    AnalogIOpoints = MAI_2x8UAI*2 + PB0_8DO*8+ (UniversalIOmodules+PBI_16DI)*16 +(DInput24VDC32Ch+DOutput24VDC32Ch)*32 - DiscreteIOpoints if I_O_Replaced>0 else 0
    #custom_intemediate_calculation_not_given in excel
    if VPMDSys =="Non Virtualized" and mainMSID =="Main MSID system" and sepDepart!=0:
        if PMDserType =="Redundant":
            Non_VirtPMDser =2
        else:
            Non_VirtPMDser=1
    else:
        Non_VirtPMDser = 0

    #BOM_calculation

    MZSQLCL4_1 =TotalPhysStationTPA  if migratingSyst =="TPA Alcont" else max((TotalPhysStationPMD+ConremoteView-flexLicenses),0)
    MZSQLCL4_2 =flexLicenses
    MZSQLCL4 = MZSQLCL4_1+MZSQLCL4_2
    EPSTAT01 = MZSQLCL4_1%5
    EPSTAT05 = m.floor((MZSQLCL4_1%10)/5)
    EPSTAT10 = m.floor(MZSQLCL4_1/10)
    #EPSMWIN1
    if migratingSyst =="TPA Alcont":
        EPSMWIN1 = dsHMIvirt+qsHMIvirt
    else:
        EPSMWIN1 = max((dsHMIvirt+qsHMIvirt+dsHMIcab+qsHMIcab - multiWindowLic),0)
    MZPCWS93_1_1 = ssHMIvirt+dsHMIvirt+qsHMIvirt if VPMDSys == "Non Virtualized" else 0
    MZPCWS93_1 = MZPCWS93_1_1 +ssHMIcab+dsHMIcab+qsHMIcab
    MZPCWS93_2 = CM_EWS+VDM_EWS if VPMDSys == "Non Virtualized" else 0 
    EPCOAW10 = MZPCWS93 = MZPCWS93_1+ MZPCWS93_2
    PDWSLBS01_1 = MZPCWS93_1
    PDWSLBS01_2 = VirtHMIworkstn
    PDWSLBS01_3 = CM_EWS+VDM_EWS if  VPMDSys =="Virtualized" else 0
    PDWSLBS01 = PDWSLBS01_1 + PDWSLBS01_2+ PDWSLBS01_3

    TPFPW271_1 = ssHMIvirt+ssHMIcab +(dsHMIvirt+dsHMIcab)*2+(qsHMIvirt+qsHMIcab)*4 if HMI_DxMLCDHon =="Yes" else 0
    TPFPW271_2 =1 if VPMDSys =="Non Virtualized" and mainMSID =="Main MSID system" and sepDepart!=0 else 0
    TPFPW271_3 = CM_EWS+VDM_EWS if VPMDSys =="Non Virtualized" else 0
    TPFPW271 = TPFPW271_1 +TPFPW271_2 +TPFPW271_3
    TPTHNCL6100_1 = ssHMIvirt+dsHMIvirt if  VPMDSys =="Virtualized" else 0
    TPTHNCL6100_2 = CM_EWS+VDM_EWS if  VPMDSys =="Virtualized" else 0 

    TPTHNCL6100 = TPTHNCL6100_1 +TPTHNCL6100_2
    TPTHNCL7100 = qsHMIvirt if  VPMDSys =="Virtualized" else 0 
    PDHMIC01 = m.ceil((ssHMIcab+dsHMIcab+qsHMIcab+CM_EWS)/5)
    PDCSAB01 = MZPCWS93_1
    EPS04CAL = m.ceil(max(0,((MZPCWS93)/5 -1)))
    
    EPBRSE05_1 = m.ceil(ConremoteView/10) if VPMDSys =="Non Virtualized" else 0
    EPBRSE05_2 = Non_VirtPMDser
    EPBRSE05 = 0
    if VPMDSys =="Non Virtualized":
        if EBR_NAS == "Yes":
            EPBRSE05 = EPBRSE05_1 +EPBRSE05_2
    EPBRWE05 = MZPCWS93
        
    MZPCSR02_1 = m.ceil(ConremoteView/10) if VPMDSys =="Non Virtualized" else 0
    MZPCSR02_2 =  Non_VirtPMDser
    MZPCSR02_3 =0
    if VPMDSys =="Non Virtualized":
        if OPCclient!=0:
            MZPCSR02_3 =1
    MZPCSR02= MZPCSR02_1 + MZPCSR02_2+MZPCSR02_3
    EPCOAS19 = MZPCSR02
    EPT09CAL = MZPCSR02*5
    PDSSLBS01_1 = MZPCSR02_1
    PDSSLBS01_2 = VirtRHSser
    PDSSLBS01_3 =MZPCSR02_2
    PDSSLBS01_4 = VirtPMDser
    PDSSLBS01_5 =1 if OPCclient!=0 else 0
    PDSSLBS01_6=0
    if VPMDSys =="Virtualized":
        if OPCclient!=0:
            PDSSLBS01_6 =1
    PDSSLBS01_7 = 0
    if VPMDSys =="Non Virtualized":
        if EBR_NAS == "Yes":
            PDSSLBS01_7 = m.ceil((EPBRSE05*1.2 + EPBRWE05*0.3)/8)
    PDSSLBS01 = PDSSLBS01_1 +PDSSLBS01_2 +PDSSLBS01_3+ PDSSLBS01_4+ PDSSLBS01_5+ PDSSLBS01_6+ PDSSLBS01_7
   

    PDDPBL01 = CM_EWS+VDM_EWS
    if sespType =="No":
        PDDPBL01 *=2
    EPOPCDA1 = OPCclient
    TPRDM000 = 1 if OPCclient!=0 else 0
    EPAEAPD1 = 1 if DCS_Alarm == "Yes" else 0

    EPDBASE1 = 1 if  TotalProcessPoint != 0 and mainMSID =="Main MSID system" else 0
    EPRBASE1= EPDBASE1 if PMDserType =="Redundant" else 0

    Resultant =cal10k(TotalProcessPoint)
    EPDPR100=Resultant["100"]
    EPDPR01K=Resultant["1k"]
    EPDPR02K=Resultant["2k"]
    EPDPR05K=Resultant["5k"]
    EPDPR10K=Resultant["10k"]

    EPRPR100= EPDPR100 if PMDserType =="Redundant" else 0
    EPRPR01K= EPDPR01K if PMDserType =="Redundant" else 0
    EPRPR02K= EPDPR02K if PMDserType =="Redundant" else 0
    EPRPR05K= EPDPR05K if PMDserType =="Redundant" else 0
    EPRPR10K= EPDPR10K if PMDserType =="Redundant" else 0
    
    PMD_variable =2 if PMDserType =="Redundant" else 1
    EP_middle = round(65 + flexLicenses *35 + (processScadaPoint * (0.05))*PMD_variable )
    EPUPANR1=EPUPANR2=EPUPANR3=EPUPANRX=0
    if sespType =="No":
        if migratingSyst =="PMD R91x":
            EPUPANR1 = EP_middle
        elif migratingSyst =="PMD R90x":
            EPUPANR2 = EP_middle
        elif migratingSyst =="PMD R83x":
            EPUPANR3 = EP_middle
        elif migratingSyst =="PMD R80x":
            EPUPANRX = EP_middle
    
    EPBRSE05_1 = m.ceil(ConremoteView/10) if VPMDSys =="Non Virtualized" else 0
    EPBRSE05_2 =  Non_VirtPMDser 
    EPBRSE05 = 0
    if VPMDSys =="Non Virtualized":
        if EBR_NAS == "Yes":
            EPBRSE05 = EPBRSE05_1 + EPBRSE05_2
    
    EPBRWE05 = MZPCWS93
    MZNWSTR6 = 0
    if VPMDSys =="Non Virtualized":
        if EBR_NAS == "Yes":
            MZNWSTR6 = m.ceil((EPBRSE05*1.2 + EPBRWE05 *0.3 )/8)
    SI920LN4 = DSSwitches +L25L35Switches +addNewSwitch
    #PDCFFCE22 = NonRedFEC_DP + RedFCE_DP*2
    PDCFFCE31 = NonRedFEC_PN
    PDSWFN01 = NonRedFEC_DP + NonRedFEC_PN +RedFCE_DP
    PDSWFN02 =PDCFFCE200= RedFCE_DP
    PDCFFCE100 =NonRedFEC_DP +NonRedFEC_PN
    PDFPCB03 = max (max16or20,m.ceil(PDCFFCE22/4))
    PDMBTB01 = 0
    if sespType== "No" and migratingSyst =="TPA Alcont":
        PDMBTB01 = m.ceil((serialLinksSupported +serialLinksUnsupported)/3)
    PDESDV01= serialLinksSupported +serialLinksUnsupported
    ALOCIP01 = XPRs_VPRs if migratingSyst in ['TPA Alcont','PMD R61x or older' , 'PMD R7xx (>R612)'] else 0

    T_900U010100 = UniversalIOmodules
    T_900A010202 = MAI_2x8UAI*2
    T_900G030202 = PBI_16DI
    T_900G320101 = DInput24VDC32Ch
    T_900H030202 = PB0_8DO
    T_900H320102 = DOutput24VDC32Ch
    #intermediate
    sumofabove = T_900U010100+T_900A010202+T_900G030202+T_900G320101+T_900H030202+T_900H320102
    T_900R080200 = max(CE900_IOracks,m.ceil((sumofabove)/8))
    T_900TNF0200 = T_900R080200*8 - (sumofabove)
    T_900P010301_1 = T_900R080200 if RedPowerSupplies=="No" else 0
    T_900SP10200 =T_900P010301_2 = CFMSD000 =T_900CP10200=T_900RNF0200=T_900RR00200=TCSWCS90 = EPAIO100=EPDIO100=0
    if CE900connt_UI =="PMD IO HIVE gateway (UOCGW)":
        somerandomname = m.ceil(T_900R080200/8)
        T_900SP10200 =T_900R080200
        T_900P010301_2 = CFMSD000 =T_900CP10200=somerandomname*2
        T_900RNF0200=T_900RR00200=TCSWCS90 = somerandomname
        EPAIO100 = max(m.ceil((AnalogIOpoints-200)/100),0)
        EPDIO100 = max(m.ceil((DiscreteIOpoints-600)/100),0)
    T_900P010301 = T_900P010301_1 +T_900P010301_2
    
    CCUSCA01 = SWI_BOU_16UIO_UMS +MAI_ACO_16UIO_UMS
    CCUAIA01 = GI_iso_AI_AO
    CCUDXA01 = GI_iso_DI_DO
    CCUPTA01 = max(((CCUSCA01*16)-CCUAIA01-CCUDXA01),0)
    T_900UMCT010 = CCUSCA01
    PDSDCD01 =1
    EPXRESR1 =DSA_community

    attDict["TEPSTAT01"] =EPSTAT01
    attDict["TEPSTAT05"] =EPSTAT05
    attDict["TEPSTAT10"] =EPSTAT10
    attDict["TEPSMWIN1"] =EPSMWIN1
    attDict["TMZSQLCL4"] =MZSQLCL4
    attDict["TMZPCWS93"] =MZPCWS93
    attDict["TEPCOAW10"] =EPCOAW10
    attDict["TPDWSLBS01"] =PDWSLBS01
    attDict["TTPFPW271"] =TPFPW271
    attDict["TTPTHNCL6100"] =TPTHNCL6100
    attDict["TTPTHNCL7100"] =TPTHNCL7100
    attDict["TPDHMIC01"] =PDHMIC01
    attDict["TPDCSAB01"] =PDCSAB01
    attDict["TMZPCSR02"] =MZPCSR02
    attDict["TEPCOAS19"] =EPCOAS19
    attDict["TEPT09CAL"] =EPT09CAL
    attDict["TPDSSLBS01"] =PDSSLBS01
    attDict["TEPDBASE1"] =EPDBASE1
    attDict["TEPRBASE1"] =EPRBASE1
    attDict["TEPDPR100"] =EPDPR100
    attDict["TEPDPR01K"] =EPDPR01K
    attDict["TEPDPR02K"] =EPDPR02K
    attDict["TEPDPR05K"] =EPDPR05K
    attDict["TEPDPR10K"] =EPDPR10K
    attDict["TEPRPR100"] =EPRPR100
    attDict["TEPRPR01K"] =EPRPR01K
    attDict["TEPRPR02K"] =EPRPR02K
    attDict["TEPRPR05K"] =EPRPR05K
    attDict["TEPRPR10K"] =EPRPR10K
    attDict["TEPUPANR1"] =EPUPANR1
    attDict["TEPUPANR2"] =EPUPANR2
    attDict["TEPUPANR3"] =EPUPANR3
    attDict["TEPUPANRX"] =EPUPANRX
    attDict["TEPS04CAL"] =EPS04CAL
    attDict["TPDDPBL01"] =PDDPBL01
    attDict["TEPOPCDA1"] =EPOPCDA1
    attDict["TTPRDM000"] =TPRDM000
    attDict["TEPAEAPD1"] =EPAEAPD1
    attDict["TEPBRSE05"] =EPBRSE05
    attDict["TEPBRWE05"] =EPBRWE05
    attDict["TMZNWSTR6"] =MZNWSTR6
    attDict["TSI920LN4"] =SI920LN4
    attDict["TPDCFFCE22"] =PDCFFCE22
    attDict["TPDCFFCE31"] =PDCFFCE31
    attDict["TPDSWFN01"] =PDSWFN01
    attDict["TPDSWFN02"] =PDSWFN02
    attDict["TPDCFFCE100"] =PDCFFCE100
    attDict["TPDCFFCE200"] =PDCFFCE200
    attDict["TPDFPCB03"] =PDFPCB03
    attDict["TPDMBTB01"] =PDMBTB01
    attDict["TPDESDV01"] =PDESDV01
    attDict["TALOCIP01"] =ALOCIP01
    attDict["T_900U010100"] =T_900U010100
    attDict["T_900A010202"] =T_900A010202
    attDict["T_900G030202"] =T_900G030202
    attDict["T_900G320101"] =T_900G320101
    attDict["T_900H030202"] =T_900H030202
    attDict["T_900H320102"] =T_900H320102
    attDict["T_900TNF0200"] =T_900TNF0200
    attDict["T_900R080200"] =T_900R080200
    attDict["T_900P010301"] =T_900P010301
    attDict["T_900SP10200"] =T_900SP10200
    attDict["TCFMSD000"] =CFMSD000
    attDict["T_900CP10200"] =T_900CP10200
    attDict["T_900RNF0200"] =T_900RNF0200
    attDict["T_900RR00200"] =T_900RR00200
    attDict["TTCSWCS90"] =TCSWCS90
    attDict["TEPAIO100"] =EPAIO100
    attDict["TEPDIO100"] =EPDIO100
    attDict["TCCUSCA01"] =CCUSCA01
    attDict["TCCUAIA01"] =CCUAIA01
    attDict["TCCUDXA01"] =CCUDXA01
    attDict["TCCUPTA01"] =CCUPTA01
    attDict["T_900UMCT010"] =T_900UMCT010
    attDict["TPDSDCD01"] =PDSDCD01
    attDict["TEPXRESR1"] =EPXRESR1