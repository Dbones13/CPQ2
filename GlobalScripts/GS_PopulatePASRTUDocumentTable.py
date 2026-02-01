def populateRTUData(Quote):
    #["System_Group",   "System_Grp_GUID"   "System_Name"   "System_Item_GUID"  "CG_Name"   "CG_Item_GUID"  "CG"]
    hierarchy = {'Level0': "New / Expansion Project", 'Level1': "System Group", "Level2": "ControlEdge RTU System", "Level3":"RTU Group"}

    lst = ["CE_Site_Voltage", "PLC_IO_Filler_Module", "PLC_IO_Spare", "PLC_IO_Slot_Spare", "PLC_Shielded_Terminal_Strip", "CE_Selected_Products", "CE_Add_System_Rows", "CE_Apply_System_Number", "CE_Scope_Choices", "New_Expansion", "Sys_Group_Name", "PLC_Software_Release","PLC_CG_Name","PLC_RG_Name", "CE PLC Engineering Execution Year"]
    
    proj_columns = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']
    proj_columns_seq = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']
    
    sysgrp_columns = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']
    sysgrp_columns_seq = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']
    

    # UOC_Common_Questions_Cont
    sys_columns = ['Marshalling_Cabinet_Count']
    sys_columns_seq = ['Marshalling_Cabinet_Count']

    #['Non_HART_Analog_Input', 'HART_Analog_Input', 'Non_HART_Analog_Output', 'HART_Analog_Output', 'Digital_Input', 'Digital_Output', 'Pulse_Input', 'FIM_Analog_Input', 'Field_ISA100_Wireless_Devices']
    cg_columns = ['Non_HART_Analog_Input', 'HART_Analog_Input', 'Non_HART_Analog_Output', 'HART_Analog_Output', 'Digital_Input', 'Digital_Output', 'Integrated_Marshalling_Cabinet', "Pulse_Input","FIM_Analog_Input","FIM_devices_segment_withOpen_loop","Number_Segments_FIM4","Field_ISA100_Wireless_Devices","FDAP","Modbus_RS485_Serial_Communication_Devices","Modbus_RS232_Serial_Communication_Devices","Modbus_TCP_IP_Ethernet_Device","Cabinet_Spare_space","Marshalling_Cabinet_Count"]

    cg_columns_seq = ['Cabinet_Spare_space', 'Integrated_Marshalling_Cabinet', 'Non_HART_Analog_Input', 'HART_Analog_Input', 'Non_HART_Analog_Output', 'HART_Analog_Output', 'Digital_Input', 'Digital_Output',"Pulse_Input","FIM_Devices","Field_ISA100_Wireless_Devices","Modbus_RS485_Serial_Communication_Devices","Modbus_RS232_Serial_Communication_Devices","Modbus_TCP_IP_Ethernet_Device","FDAP"]

    rg_columns = ['Non_HART_Analog_Input', 'HART_Analog_Input', 'Non_HART_Analog_Output', 'HART_Analog_Output', 'Digital_Input', 'Digital_Output']

    rg_columns_seq = []

    cabinets_columns = ['Cabinet_cnt']
    cabinet_columns_seq = ['Cabinet_cnt']

    cg_system_col_seq = ['IMC_Yes','IMC_No','cab_count_yes', 'cab_count_no',"mar_cab_count"]



    QT_Table = Quote.QuoteTables["PAS_Document_Data"]
    RTU = ''

    '''#for level 0
    for Item in Quote.MainItems:
        if hierarchy["Level0"] == Item.ProductName:
            newRow = QT_Table.AddNewRow()
            newRow["Project"] = Item.PartNumber
            newRow["Project_GUID"] = Item.QuoteItemGuid
            newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem

    #for level 1
    for Item in Quote.MainItems:
        if hierarchy["Level1"] == Item.ProductName:
            newRow = QT_Table.AddNewRow()
            newRow["System_Group"] = Item.PartNumber
            newRow["System_Grp_GUID"] = Item.QuoteItemGuid
            newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem'''

    #for level 2
    for Item in Quote.MainItems:
        if hierarchy["Level2"] == Item.ProductName:
            RTU ='Yes'
            newRow = QT_Table.AddNewRow()
            newRow["System_Name"] = Item.ProductName
            newRow["System_Item_GUID"] = Item.QuoteItemGuid
            newRow["System_Grp_GUID"] = Item.ParentItemGuid
            newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
    if RTU != 'Yes':
        for row in QT_Table.Rows:
            if row["System_Name"] == 'ControlEdge RTU System':
                rowId = row.Id
                QT_Table.DeleteRow(int(rowId))


    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName and row["System_Item_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber


    #for level 3
    for Item in Quote.MainItems:
        if hierarchy["Level3"] == Item.ProductName:
            newRow = QT_Table.AddNewRow()
            newRow["CG_Name"] = Item.PartNumber
            newRow["CG_Item_GUID"] = Item.QuoteItemGuid
            newRow["System_Item_GUID"] = Item.ParentItemGuid
            newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem


    LST_CG_GUID = 1
    CGn = 0
    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level2"] == Item.ProductName and row["System_Item_GUID"] == Item.QuoteItemGuid:
                row["System_Name"] = Item.ProductName
                row["System_Item_GUID"] = Item.QuoteItemGuid
                row["System_Grp_GUID"] = Item.ParentItemGuid
                if LST_CG_GUID == Item.ParentItemGuid and row["CG_Name"] != '':
                    CGn += int(1)
                    row["CG_No"] = str(CGn)
                elif row["CG_Name"] != '':
                    CGn = 1
                    row["CG_No"] = str(CGn)
                    LST_CG_GUID = Item.ParentItemGuid


    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName and row["System_Grp_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber

    IMC_Yes = False
    IMC_No = False
    cab_count_yes = 0
    cab_count_no = 0
    mar_cab_count = 0
    for row in QT_Table.Rows:
        n = 0
        RIO_CNT = 0
        LIO_CNT = 0
        for Item in Quote.Items:
            '''if row['Project_GUID'] == Item.QuoteItemGuid and Item.ProductName == "New / Expansion Project" and row['System_Group'] == '' and row['System_Name'] == '' and row['CG_Name'] == '':
                 projdic = {}
                 for attr in Item.SelectedAttributes:
                     if attr.Name not in lst and "PLC" not in attr.Name:
                         try:
                             attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                             for column in attr_containers:
                                 if column.Name in proj_columns:
                                     projdic[column.Name] = column.Value
                         except:
                             pass

                 expectedResult = [projdic[d] for d in proj_columns_seq if d in projdic.keys()]
                 row['Project_Info'] = "|".join(expectedResult)
            if row['System_Grp_GUID'] == Item.QuoteItemGuid and Item.ProductName == "System Group" and row['System_Name'] == '' and row['CG_Name'] == '':
                Sysgrpdic = {}
                for attr in Item.SelectedAttributes:
                    if attr.Name not in lst and "PLC" not in attr.Name:
                        try:
                            attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                        except:
                            pass
                        for column in attr_containers:
                            if column.Name in sysgrp_columns:
                                #Trace.Write('==========='+str(column.Name))
                                Sysgrpdic[column.Name] = column.Value
                expectedResult = [Sysgrpdic[d] for d in sysgrp_columns_seq if d in Sysgrpdic.keys()]
                row['System_grp'] = "|".join(expectedResult)'''
            if row['System_Item_GUID'] == Item.QuoteItemGuid and Item.ProductName == "ControlEdge RTU System" and row['CG_Name'] == '':
                Sysdic = {}
                for attr in Item.SelectedAttributes:
                    error_flag = False
                    if attr.Name not in lst and "PLC" not in attr.Name:
                        try:
                            attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                        except:
                            error_flag = True
                        if error_flag:
                            continue
                        for column in attr_containers:
                            if column.Name in sys_columns:
                                Sysdic[column.Name] = column.Value
                expectedResult = [Sysdic[d] for d in sys_columns_seq if d in Sysdic.keys()]
                row['System'] = "|".join(expectedResult)

            elif row['CG_ITEM_GUID'] == Item.QuoteItemGuid and Item.ProductName == "RTU Group":
                CGdic = {}
                for attr in Item.SelectedAttributes:
                    error_flag = False
                    if attr.Name not in lst and "PLC" not in attr.Name:
                        try:
                            attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                        except:
                            error_flag = True
                        if error_flag:
                            continue
                        RTU_AO = 0
                        RTU_AO_HART = 0
                        RTU_Universal = 0
                        RTU_DO = 0
                        RTU_DI = 0
                        FIM_Devices = 0
                        for column in attr_containers:
                            if column.Name in cg_columns:
                                if column.Name == 'Integrated_Marshalling_Cabinet':
                                    try:
                                        CGdic[column.Name] = column.Value
                                        if column.Value == 'Yes':
                                            parts = Item.SelectedAttributes.GetContainerByName('RTU_CG_PartSummary_Cont').Rows
                                            for part in parts:
                                                if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
                                                    cab_count_yes += int(part['CE_Part_Qty'])
                                            IMC_Yes = True
                                        elif column.Value == 'No':
                                            IMC_No = True
                                            parts = Item.SelectedAttributes.GetContainerByName('RTU_CG_PartSummary_Cont').Rows
                                            for part in parts:
                                                if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
                                                    cab_count_no += int(part['CE_Part_Qty'])
                                    except:
                                        Trace.Write('Error while reading Part Summary')
                                    CGdic[column.Name] = column.Value
                                elif column.Name == 'Marshalling_Cabinet_Count':
                                    mar_cab_count += int(column.Value)
                                elif column.Name == 'Cabinet_Spare_space':
                                    CGdic[column.Name] = column.Value
                                elif column.Name in ['Non_HART_Analog_Output']:
                                    LIO_CNT += int(column.Value)
                                    RTU_AO += int(column.Value)
                                    CGdic['RTU_AO'] = RTU_AO
                                    CGdic['Non_HART_Analog_Output'] = column.Value
                                elif column.Name in ['HART_Analog_Output']:
                                    LIO_CNT += int(column.Value)
                                    RTU_AO_HART += int(column.Value)
                                    CGdic['RTU_AO_HART_Points'] = RTU_AO_HART
                                    CGdic['HART_Analog_Output'] = int(column.Value)
                                elif column.Name in ["FIM_Analog_Input","FIM_devices_segment_withOpen_loop","Number_Segments_FIM4"]:
                                    FIM_Devices += int(column.Value)
                                    CGdic['FIM_Devices'] = FIM_Devices
                                elif column.Name in ["Field_ISA100_Wireless_Devices","Modbus_RS485_Serial_Communication_Devices","Modbus_RS232_Serial_Communication_Devices","Modbus_TCP_IP_Ethernet_Device","Pulse_Input"]:
                                    if column.Name == 'Pulse_Input':
                                        LIO_CNT += int(column.Value)
                                    CGdic[column.Name] = column.Value
                                elif column.Name in ['Digital_Output']:
                                    LIO_CNT += int(column.Value)
                                    RTU_DO += int(column.Value)
                                    CGdic['RTU_DO'] = RTU_DO
                                    CGdic['Digital_Output'] = int(column.Value)
                                elif column.Name in ['Digital_Input']:
                                    LIO_CNT += int(column.Value)
                                    RTU_DI += int(column.Value)
                                    CGdic['RTU_DI'] = RTU_DI
                                    CGdic['Digital_Input'] = int(column.Value)
                                elif attr.Name == 'RTU_CG_IO_Container' and column.Name == 'Non_HART_Analog_Input':
                                    LIO_CNT += int(column.Value)
                                    CGdic['RTU_AI'] = column.Value
                                    CGdic['Non_HART_Analog_Input'] = column.Value
                                else:
                                    Trace.Write(column.Name) 
                                    Trace.Write(column.Value) 
                                    LIO_CNT += int(column.Value)
                                    CGdic[column.Name] = column.Value
                expectedResult = [str(CGdic[d]) for d in cg_columns_seq if d in CGdic.keys()]
                Trace.Write("Expected Result: "+str(expectedResult))
                row['CG'] = "|".join(expectedResult)
                row['Local_IO'] = LIO_CNT
    for row in QT_Table.Rows:
        Cabinet_cnt = 0
        Cabinet_dic = {}
        CG_dic = {}
        if row['System_Name'] == "ControlEdge RTU System" and row['CG_Name'] == '':
            CG_dic['IMC_No'] = '1' if IMC_No else '0'
            CG_dic['IMC_Yes'] = '1' if IMC_Yes else '0'
            CG_dic['cab_count_yes'] = str(cab_count_yes)
            CG_dic['cab_count_no'] = str(cab_count_no)
            CG_dic["mar_cab_count"] = str(mar_cab_count)
            for Item in Quote.Items:
                if Item.PartNumber in ('CC-CBDS01', 'CC-CBDD01') and Item.RolledUpQuoteItem[:3] == row['RolledUpQuoteItem'][:3]:
                    Cabinet_cnt += Item.Quantity
                    Cabinet_dic["Cabinet_cnt"] = str(Cabinet_cnt)
            expectedResult = [Cabinet_dic[d] for d in cabinet_columns_seq if d in Cabinet_dic.keys()]
            row["Cabinets"] = "|".join(expectedResult)
            expectedResultCG = [CG_dic[d] for d in cg_system_col_seq if d in CG_dic.keys()]
            row["CG"] = "|".join(expectedResultCG)
        if row['System_Name'] == "ControlEdge RTU System" and row['CG_Name'] != '':
            if row['Remote_IO'] == '':
                row['Remote_IO'] = '0'
                row['Remote_Qty'] = '0'
    QT_Table.Save()

    if RTU != 'Yes':
        return False
    else:
        return True