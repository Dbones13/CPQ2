def populateSMData(Quote):
    hierarchy = {
        'Level0': "New / Expansion Project",
        'Level1': "System Group",
        "Level2": "Safety Manager",
        "Level3":"SM Control Group"
    }

    sys_columns = ['Percent_Installed_Spare_IOs']
    sys_columns_seq = ['Percent_Installed_Spare_IOs']

    cg_columns_map =[
        'SDO(1) 24Vdc 500mA UIO (0-5000)',
        'SDO(7) 24Vdc Line Mon UIO (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)',
        'SDO(1) 24Vdc SIL3 P+F UIO (0-5000)',
        'SDI(1) 24Vdc UIO (0-5000)',
        'SDI(1)  24Vdc SIL2 P+F UIO (0-5000)',
        'SDI(1)  24Vdc SIL3 P+F UIO (0-5000)',
        'SDI(1) 24Vdc Line Mon UIO (0-5000)',
        'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)',
        'SAI(1)mA type Current UIO (0-5000)',
        'SAI(1)FIRE 2 wire current UIO (0-5000)',
        'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)',
        'SAI(1) GAS current UIO (0-5000)',
        'SAI(1)FIRE 3-4 wire current UIO (0-5000)',
        'SAO(1)mA Type UIO (0-5000)',
        'SAO(1)mA Type P+F UIO (0-5000)'
    ]
    cg_columns_dio = [
        'SDI(1) 24Vdc DIO (0-5000)',
        'SDI(1) 24Vdc Line Mon DIO (0-5000)',
        'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)',
        'SDO(1) 24Vdc 500mA DIO (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)'
    ]
    rg_column_uio =[
        'SDI(1) 24Vdc UIO  (0-5000)',
        'SDI(1) 24Vdc Line Mon UIO  (0-5000)',
        'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)',
        'SDI(1)  24Vdc SIL2 P+F UIO  (0-5000)',
        'SDI(1)  24Vdc SIL3 P+F UIO  (0-5000)',
        'SDO(1) 24Vdc 500mA UIO  (0-5000)',
        'SDO(1) 24Vdc SIL3 P+F UIO  (0-5000)',
        'SDO(7) 24Vdc Line Mon UIO  (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)',
        'SAI(1)mA type Current  UIO  (0-5000)',
        'SAI(1) mA Type Current P+F UIO  (0-5000)',
        'SAI(1)FIRE 2 wire current  UIO   (0-5000)',
        'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)',
        'SAI(1) GAS current  UIO  (0-5000)',
        'SAO(1)mA Type UIO   (0-5000)',
        'SAO(1)mA Type P+F UIO  (0-5000)',
        'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)',
        'SDI(1) 24Vdc UIO (0-5000)',
        'SDO(1) 24Vdc 500mA UIO (0-5000)'
    ]
    rg_column_dio =[
        'SDI(1) 24Vdc DIO  (0-5000)',
        'SDI(1) 24Vdc Line Mon DIO (0-5000)',
        'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)',
        'SDO(1) 24Vdc 500mA DIO  (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc COM DIO  (0-5000)',
        'SDO(16) SIL 2/3 250Vac/Vdc DIO  (0-5000)',
        'SDI(1) 24Vdc DIO (0-5000)',
        'SDO(1) 24Vdc 500mA DIO (0-5000)'
    ]

    QT_Table = Quote.QuoteTables["PAS_Document_Data"]
    SM = ''
    for Item in filter(lambda item:item.ProductName.startswith(hierarchy["Level2"]), Quote.MainItems):
        SM ='Yes'
        newRow = QT_Table.AddNewRow()
        newRow["System_Name"] = Item.ProductName
        newRow["System_Item_GUID"] = Item.QuoteItemGuid
        newRow["System_Grp_GUID"] = Item.ParentItemGuid
        newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem

    if SM != 'Yes':
        for row in QT_Table.Rows:
            if row["System_Name"].startswith('Safety Manager'):
                rowId = row.Id
                QT_Table.DeleteRow(int(rowId))

    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName and row["System_Item_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber

    #for level 3
    for Item in filter(lambda item:item.ProductName == hierarchy["Level3"], Quote.MainItems):
        newRow = QT_Table.AddNewRow()
        newRow["CG_Name"] = Item.PartNumber
        newRow["CG_Item_GUID"] = Item.QuoteItemGuid
        newRow["System_Item_GUID"] = Item.ParentItemGuid
        newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem

    LST_CG_GUID = 1
    CGn = {
        "Safety Manager ESD" : 0,
        "Safety Manager FGS" : 0,
        "Safety Manager BMS" : 0,
        "Safety Manager HIPPS" : 0
    }
    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if Item.ProductName.startswith(hierarchy["Level2"]) and row["System_Item_GUID"] == Item.QuoteItemGuid:
                row["System_Name"] = Item.ProductName
                row["System_Item_GUID"] = Item.QuoteItemGuid
                row["System_Grp_GUID"] = Item.ParentItemGuid
                if LST_CG_GUID == Item.ParentItemGuid and row["CG_Name"] != '':
                    CGn[Item.ProductName] += int(1)
                    row["CG_No"] = str(CGn[Item.ProductName])
                elif row["CG_Name"] != '':
                    CGn = {
                        "Safety Manager ESD" : 0,
                        "Safety Manager FGS" : 0,
                        "Safety Manager BMS" : 0,
                        "Safety Manager HIPPS" : 0
                    }
                    CGn[Item.ProductName] = 1
                    row["CG_No"] = str(CGn[Item.ProductName])
                    LST_CG_GUID = Item.ParentItemGuid

    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName and row["System_Grp_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber

    n = RIO_CNT = LIO_CNT = 0
    for Item in filter(lambda item: item.ProductName.startswith("Safety Manager"), Quote.MainItems):
        for child in filter(lambda item: item.ProductName == "SM Control Group", Item.Children):
            Sysdic = {}

            cg_right_cont_rows = child.SelectedAttributes.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows
            cg_left_cont_rows = child.SelectedAttributes.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows

            io_spare = 0
            for row in cg_right_cont_rows:
                io_spare = int(row['Percent_Installed_Spare_IOs']) if row['Percent_Installed_Spare_IOs']!='' else 0
            Sysdic['io_spare'] = io_spare
            expectedResult = [str(Sysdic[d]) for d in Sysdic.keys()]
            for row in QT_Table.Rows:
                if row['System_Item_GUID'] == Item.QuoteItemGuid:
                    if row['CG_Item_GUID'] == child.QuoteItemGuid:
                        row['System'] = "|".join(expectedResult)

            di_cont_rows = child.SelectedAttributes.GetContainerByName("SM_IO_Count_Digital_Input_Cont").Rows
            do_cont_rows = child.SelectedAttributes.GetContainerByName("SM_IO_Count_Digital_Output_Cont").Rows
            ao_cont_rows = child.SelectedAttributes.GetContainerByName("SM_IO_Count_Analog_Output_Cont").Rows
            ai_cont_rows = child.SelectedAttributes.GetContainerByName("SM_IO_Count_Analog_Input_Cont").Rows

            ioSum = [0] * 53
            #Digital Input Container Data
            for attr_cnt in di_cont_rows:
                if attr_cnt['Digital Input Type'] in cg_columns_map:
                    ioSum[1] += int(attr_cnt['Red (IS)']) if attr_cnt['Red (IS)']!='' else 0
                    ioSum[2] += int(attr_cnt['Non Red (IS)']) if attr_cnt['Non Red (IS)']!='' else 0
                    ioSum[3] += int(attr_cnt['Red (NIS)']) if attr_cnt['Red (NIS)']!='' else 0
                    ioSum[4] += int(attr_cnt['Non Red (NIS)']) if attr_cnt['Non Red (NIS)']!='' else 0
                    ioSum[5] += int(attr_cnt['Red (RLY)']) if attr_cnt['Red (RLY)']!='' else 0
                    ioSum[6] += int(attr_cnt['Non Red (RLY)']) if attr_cnt['Non Red (RLY)']!='' else 0
                if attr_cnt['Digital Input Type'] in cg_columns_dio:
                    ioSum[13] += int(attr_cnt['Red (IS)']) if attr_cnt['Red (IS)']!='' else 0
                    ioSum[14] += int(attr_cnt['Non Red (IS)']) if attr_cnt['Non Red (IS)']!='' else 0
                    ioSum[15] += int(attr_cnt['Red (NIS)']) if attr_cnt['Red (NIS)']!='' else 0
                    ioSum[16] += int(attr_cnt['Non Red (NIS)']) if attr_cnt['Non Red (NIS)']!='' else 0
                    ioSum[17] += int(attr_cnt['Red (RLY)']) if attr_cnt['Red (RLY)']!='' else 0
                    ioSum[18] += int(attr_cnt['Non Red (RLY)']) if attr_cnt['Non Red (RLY)']!='' else 0

            #Digital Output Container Data
            for attr_cnt in do_cont_rows :
                dot = ""
                #There is issue getting the value using attr_cnt['Digital Output Type']
                #workaround
                for col in attr_cnt.Columns:
                    if col.Name == "Digital Output Type":
                        dot = col.Value
                        break
                if dot in cg_columns_map:
                    ioSum[25] += int(attr_cnt['Red (IS)']) if attr_cnt['Red (IS)'] != '' else 0
                    ioSum[26] += int(attr_cnt['Non Red (IS)']) if attr_cnt['Non Red (IS)'] != '' else 0
                    ioSum[27] += int(attr_cnt['Red (NIS)']) if attr_cnt['Red (NIS)'] !='' else 0
                    ioSum[28] += int(attr_cnt['Non Red (NIS)']) if attr_cnt['Non Red (NIS)'] !='' else 0
                    ioSum[29] += int(attr_cnt['Red (RLY)']) if attr_cnt['Red (RLY)'] !='' else 0
                    ioSum[30] += int(attr_cnt['Non Red (RLY)']) if attr_cnt['Non Red (RLY)'] !='' else 0
                if dot in cg_columns_dio:
                    ioSum[35] += int(attr_cnt['Red (IS)']) if attr_cnt['Red (IS)'] != '' else 0
                    ioSum[36] += int(attr_cnt['Non Red (IS)']) if attr_cnt['Non Red (IS)'] != '' else 0
                    ioSum[37] += int(attr_cnt['Red (NIS)']) if attr_cnt['Red (NIS)'] != '' else 0
                    ioSum[38] += int(attr_cnt['Non Red (NIS)']) if attr_cnt['Non Red (NIS)'] != '' else 0
                    ioSum[39] += int(attr_cnt['Red (RLY)']) if attr_cnt['Red (RLY)'] != '' else 0
                    ioSum[40] += int(attr_cnt['Non Red (RLY)']) if attr_cnt['Non Red (RLY)'] != '' else 0

            #Analog Input Container Data
            for attr_cnt in ai_cont_rows :
                if attr_cnt['Analog Input Type'] in cg_columns_map:
                    ioSum[45] +=int(attr_cnt['Red (IS)']) if attr_cnt['Red (IS)']!='' else 0
                    ioSum[46] +=int(attr_cnt['Non Red (IS)']) if attr_cnt['Non Red (IS)']!='' else 0
                    ioSum[47] +=int(attr_cnt['Red (NIS)']) if attr_cnt['Red (NIS)']!='' else 0
                    ioSum[48] +=int(attr_cnt['Non Red (NIS)']) if attr_cnt['Non Red (NIS)']!='' else 0

            #Analog Output Container Data
            for attr_cnt in ao_cont_rows :
                if attr_cnt['Analog Output Type'] in cg_columns_map:
                    ioSum[49] +=int(attr_cnt['Red (IS)']) if attr_cnt['Red (IS)']!='' else 0
                    ioSum[50] +=int(attr_cnt['Non Red (IS)']) if attr_cnt['Non Red (IS)']!='' else 0
                    ioSum[51] +=int(attr_cnt['Red (NIS)']) if attr_cnt['Red (NIS)']!='' else 0
                    ioSum[52] +=int(attr_cnt['Non Red (NIS)']) if attr_cnt['Non Red (NIS)']!='' else 0

            for leftRow in cg_left_cont_rows :
                if leftRow['Marshalling_Option'] == "Universal_Marshalling":
                    for rightRow in cg_right_cont_rows :
                        sil = rightRow['DI/DO_SIL2/3_Relay_Adapter_UMC']
                        nmr = rightRow['DI_NAMUR_proximity_Switches_Adapter_UMC']
                        if sil == 'Yes' or nmr == 'Yes':
                            attr_containers3 = child.SelectedAttributes.GetContainerByName("SM_CG_DI_RLY_NMR_Cont").Rows
                            for attr_cnt in attr_containers3:
                                if attr_cnt['Digital Input Type'] in cg_columns_map:
                                    ioSum[7] += int(attr_cnt['Red_SIL3_RLY']) if attr_cnt['Red_SIL3_RLY)']!='' else 0
                                    ioSum[8] += int(attr_cnt['Non_Red_SIL3_RLY']) if attr_cnt['Non_Red_SIL3_RLY']!='' else 0
                                    ioSum[9] += int(attr_cnt['Red_NMR']) if attr_cnt['Red_NMR']!='' else 0
                                    ioSum[10] += int(attr_cnt['Non_Red_NMR']) if attr_cnt['Non_Red_NMR']!='' else 0
                                    ioSum[11] += int(attr_cnt['Red_NMR_Safety']) if attr_cnt['Red_NMR_Safety']!='' else 0
                                    ioSum[12] += int(attr_cnt['Non_Red_NMR_Safety']) if attr_cnt['Non_Red_NMR_Safety']!=''  else 0
                                if attr_cnt['Digital Input Type'] in cg_columns_dio:
                                    ioSum[19] += int(attr_cnt['Red_SIL3_RLY']) if attr_cnt['Red_SIL3_RLY)']!=''  else 0
                                    ioSum[20] += int(attr_cnt['Non_Red_SIL3_RLY']) if attr_cnt['Non_Red_SIL3_RLY']!=''  else 0
                                    ioSum[21] += int(attr_cnt['Red_NMR']) if attr_cnt['Red_NMR']!='' else 0
                                    ioSum[22] += int(attr_cnt['Non_Red_NMR']) if attr_cnt['Non_Red_NMR']!=''  else 0
                                    ioSum[23] += int(attr_cnt['Red_NMR_Safety']) if attr_cnt['Red_NMR_Safety']!=''  else 0
                                    ioSum[24] += int(attr_cnt['Non_Red_NMR_Safety']) if attr_cnt['Non_Red_NMR_Safety']!='' else 0

                            attr_containers4 = child.SelectedAttributes.GetContainerByName("SM_CG_DO_RLY_NMR_Cont").Rows
                            for attr_cnt in attr_containers4:
                                if attr_cnt['Digital Output Type'] in cg_columns_map:
                                    ioSum[31] +=int(attr_cnt['Red_SIL2_RLY']) if attr_cnt['Red_SIL2_RLY']!='' else 0
                                    ioSum[32] +=int(attr_cnt['Non_Red_SIL2_RLY']) if attr_cnt['Non_Red_SIL2_RLY']!='' else 0
                                    ioSum[33] +=int(attr_cnt['Red_SIL3_RLY']) if attr_cnt['Red_SIL3_RLY']!='' else 0
                                    ioSum[34] +=int(attr_cnt['Non_Red_SIL3_RLY']) if attr_cnt['Non_Red_SIL3_RLY']!='' else 0
                                if attr_cnt['Digital Output Type'] in cg_columns_dio:
                                    ioSum[41] +=int(attr_cnt['Red_SIL2_RLY']) if attr_cnt['Red_SIL2_RLY']!='' else 0
                                    ioSum[42] +=int(attr_cnt['Non_Red_SIL2_RLY']) if attr_cnt['Non_Red_SIL2_RLY']!='' else 0
                                    ioSum[43] +=int(attr_cnt['Red_SIL3_RLY']) if attr_cnt['Red_SIL3_RLY']!='' else 0
                                    ioSum[44] +=int(attr_cnt['Non_Red_SIL3_RLY']) if attr_cnt['Non_Red_SIL3_RLY']!='' else 0

            LIO_CNT = sum(ioSum)
            ioSum.pop(0) #calculation started from index 1
            expectedResult = [str(d) for d in ioSum]
            Trace.Write("Expected Result: "+str(expectedResult))
            for row in QT_Table.Rows:
                if row['System_Item_GUID'] == Item.QuoteItemGuid:
                    if row['CG_Item_GUID'] == child.QuoteItemGuid:
                        row['CG'] = "|".join(expectedResult)
                        row['Local_IO']= LIO_CNT

            n = 0
            for rg in filter(lambda item: item.ProductName == "SM Remote Group", child.Children):
                    n += 1
                    attr = rg.SelectedAttributes.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows
                    rgIoSum = [0] * 53
                    for att in attr:
                        Enclosure=(att['Enclosure_Type'])
                        if Enclosure == "Cabinet":
                            attr_container = rg.SelectedAttributes.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows
                            attr_container1= rg.SelectedAttributes.GetContainerByName("SM_RG_IO_Count_Digital_Output_Cont").Rows
                            attr_container2= rg.SelectedAttributes.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows
                            attr_container3= rg.SelectedAttributes.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows
                            attr_container4= rg.SelectedAttributes.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows
                            attr_container5= rg.SelectedAttributes.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows
                            for cnt in attr_container:
                                for k in rg_column_uio:
                                    if cnt['Digital_Input_Type']==str(k):
                                        rgIoSum[1] +=int(cnt['Red_IS']) if cnt['Red_IS']!='' else 0
                                        rgIoSum[2] +=int(cnt['Non_Red_IS']) if cnt['Non_Red_IS']!='' else 0
                                        rgIoSum[3] +=int(cnt['Red_NIS']) if cnt['Red_NIS']!='' else 0
                                        rgIoSum[4] +=int(cnt['Non_Red_NIS']) if cnt['Non_Red_NIS']!='' else 0
                                        rgIoSum[5] +=int(cnt['Red_RLY']) if cnt['Red_RLY']!='' else 0
                                        rgIoSum[6] +=int(cnt['Non_Red_RLY']) if cnt['Non_Red_RLY']!='' else 0
                                for i in rg_column_dio:
                                    if cnt['Digital_Input_Type']==str(i):
                                        rgIoSum[13] +=int(cnt['Red_IS']) if cnt['Red_IS']!='' else 0
                                        rgIoSum[14] +=int(cnt['Non_Red_IS']) if cnt['Non_Red_IS']!='' else 0
                                        rgIoSum[15] +=int(cnt['Red_NIS']) if cnt['Red_NIS']!='' else 0
                                        rgIoSum[16] +=int(cnt['Non_Red_NIS']) if cnt['Non_Red_NIS']!='' else 0
                                        rgIoSum[17] +=int(cnt['Red_RLY']) if cnt['Red_RLY']!='' else 0
                                        rgIoSum[18] +=int(cnt['Non_Red_RLY']) if cnt['Non_Red_RLY']!='' else 0
                            for att in attr_container4:
                                marshalling_option =(att['Marshalling_Option'])
                                if marshalling_option== "Universal_Marshalling":
                                    for att1 in attr_container5:
                                        Sil=(att1['SM_DI_DORelay_Adapter_UMC'])
                                        nmr=(att1['SM_DI_NAMUR_Switches_Adapter_UMC'])
                                        if Sil=='Yes' or nmr =='Yes':
                                            attr_container6= child.SelectedAttributes.GetContainerByName("SM_RG_DI_RLY_NMR_Cont").Rows
                                            for cnt in attr_container6:
                                                for j in rg_column_uio:
                                                    if cnt['Digital_Input_Type']==str(j):
                                                        rgIoSum[7] +=int(cnt['Red_SIL3_RLY']) if cnt['Red_SIL3_RLY)']!='' else 0
                                                        rgIoSum[8] +=int(cnt['Non_Red_SIL3_RLY']) if cnt['Non_Red_SIL3_RLY']!='' else 0
                                                        rgIoSum[9] +=int(cnt['Red_NMR']) if cnt['Red_NMR']!='' else 0
                                                        rgIoSum[10] +=int(cnt['Non_Red_NMR']) if cnt['Non_Red_NMR']!='' else 0
                                                        rgIoSum[11] +=int(cnt['Red_NMR_Safety']) if cnt['Red_NMR_Safety']!='' else 0
                                                        rgIoSum[12] +=int(cnt['Non_Red_NMR_Safety']) if cnt['Non_Red_NMR_Safety']!=''  else 0
                                                for i in rg_column_dio:
                                                    if cnt['Digital_Input_Type']==str(i):
                                                        rgIoSum[19] +=int(cnt['Red_SIL3_RLY']) if cnt['Red_SIL3_RLY)']!=''  else 0
                                                        rgIoSum[20] +=int(cnt['Non_Red_SIL3_RLY']) if cnt['Non_Red_SIL3_RLY']!=''  else 0
                                                        rgIoSum[21] +=int(cnt['Red_NMR']) if cnt['Red_NMR']!='' else 0
                                                        rgIoSum[22] +=int(cnt['Non_Red_NMR']) if cnt['Non_Red_NMR']!=''  else 0
                                                        rgIoSum[23] +=int(cnt['Red_NMR_Safety']) if cnt['Red_NMR_Safety']!=''  else 0
                                                        rgIoSum[24] +=int(cnt['Non_Red_NMR_Safety']) if cnt['Non_Red_NMR_Safety']!='' else 0
                            for cnt in attr_container1:
                                for j in rg_column_uio:
                                    if cnt['Digital_Output_Type']==str(j):
                                        rgIoSum[25] +=int(cnt['Red_IS']) if cnt['Red_IS']!='' else 0
                                        rgIoSum[26] +=int(cnt['Non_Red_IS']) if cnt['Non_Red_IS']!='' else 0
                                        rgIoSum[27] +=int(cnt['Red_NIS']) if cnt['Red_NIS']!='' else 0
                                        rgIoSum[28] +=int(cnt['Non_Red_NIS']) if cnt['Non_Red_NIS']!='' else 0
                                        rgIoSum[29] +=int(cnt['Red_RLY']) if cnt['Red_RLY']!='' else 0
                                        rgIoSum[30] +=int(cnt['Non_Red_RLY']) if cnt['Non_Red_RLY']!='' else 0
                                for i in rg_column_dio:
                                    if cnt['Digital_Output_Type']==str(i):
                                        rgIoSum[35] +=int(cnt['Red_IS']) if cnt['Red_IS']!='' else 0
                                        rgIoSum[36] +=int(cnt['Non_Red_IS']) if cnt['Non_Red_IS']!='' else 0
                                        rgIoSum[37] +=int(cnt['Red_NIS']) if cnt['Red_NIS']!='' else 0
                                        rgIoSum[38] +=int(cnt['Non_Red_NIS']) if cnt['Non_Red_NIS']!='' else 0
                                        rgIoSum[39] +=int(cnt['Red_RLY']) if cnt['Red_RLY']!='' else 0
                                        rgIoSum[40] +=int(cnt['Non_Red_RLY']) if cnt['Non_Red_RLY']!='' else 0
                            for att in attr_container4:
                                marshalling_option = att['Marshalling_Option']
                                if marshalling_option == "Universal_Marshalling":
                                    for att1 in attr_container5:
                                        sil = att1['SM_DI_DORelay_Adapter_UMC']
                                        nmr = att1['SM_DI_NAMUR_Switches_Adapter_UMC']
                                        if sil=='Yes' or nmr =='Yes':
                                            attr_container7= child.SelectedAttributes.GetContainerByName("SM_RG_DO_RLY_NMR_Cont").Rows
                                            for cnt in attr_containers4:
                                                for j in rg_column_uio:
                                                    if cnt['Digital_Output_Type']==str(j):
                                                        rgIoSum[31] +=int(cnt['Red_SIL2_RLY']) if cnt['Red_SIL2_RLY']!='' else 0
                                                        rgIoSum[32] +=int(cnt['Non_Red_SIL2_RLY']) if cnt['Non_Red_SIL2_RLY']!='' else 0
                                                        rgIoSum[33] +=int(cnt['Red_SIL3_RLY']) if cnt['Red_SIL3_RLY']!='' else 0
                                                        rgIoSum[34] +=int(cnt['Non_Red_SIL3_RLY']) if cnt['Non_Red_SIL3_RLY']!='' else 0
                                                for i in rg_column_dio:
                                                    if cnt['Digital_Output_Type']==str(i):
                                                        rgIoSum[41] +=int(cnt['Red_SIL2_RLY']) if cnt['Red_SIL2_RLY']!='' else 0
                                                        rgIoSum[42] +=int(cnt['Non_Red_SIL2_RLY']) if cnt['Non_Red_SIL2_RLY']!='' else 0
                                                        rgIoSum[43] +=int(cnt['Red_SIL3_RLY']) if cnt['Red_SIL3_RLY']!='' else 0
                                                        rgIoSum[44] +=int(cnt['Non_Red_SIL3_RLY']) if cnt['Non_Red_SIL3_RLY']!='' else 0
                            for cnt in attr_container3:
                                for j in rg_column_uio:
                                    if cnt['Analog_Input_Type']==str(j):
                                        rgIoSum[45] +=int(cnt['Red_IS']) if cnt['Red_IS']!='' else 0
                                        rgIoSum[46] +=int(cnt['Non_Red_IS']) if cnt['Non_Red_IS']!='' else 0
                                        rgIoSum[47] +=int(cnt['Red_NIS']) if cnt['Red_NIS']!='' else 0
                                        rgIoSum[48] +=int(cnt['Non_Red_NIS']) if cnt['Non_Red_NIS']!='' else 0
                            for cnt in attr_container2:
                                for j in rg_column_uio:
                                    if cnt['Analog_Output_Type']==str(j):
                                        rgIoSum[49] +=int(cnt['Red_IS']) if cnt['Red_IS']!='' else 0
                                        rgIoSum[50] +=int(cnt['Non_Red_IS']) if cnt['Non_Red_IS']!='' else 0
                                        rgIoSum[51] +=int(cnt['Red_NIS']) if cnt['Red_NIS']!='' else 0
                                        rgIoSum[52] +=int(cnt['Non_Red_NIS']) if cnt['Non_Red_NIS']!='' else 0
                            RIO_CNT = sum(rgIoSum)
                        else:
                            ai_ao_count_rows = rg.SelectedAttributes.GetContainerByName('SM_RG_IO_Count_Analog_Input_1.3_Cabinet_Cont').Rows
                            di_do_count_rows = rg.SelectedAttributes.GetContainerByName('SM_RG_IO_Count_Digital_Input_1.3_Cabinet_Cont').Rows

                            for row in ai_ao_count_rows:
                                if row["Analog_Input/Output_Type"] == "SAI(1)mA type Current UIO (0-5000)":
                                    rgIoSum[45] += int(row['Red_IS']) if row['Red_IS']!='' else 0
                                    rgIoSum[46] += int(row['Non_Red_IS']) if row['Non_Red_IS']!='' else 0
                                    rgIoSum[47] += int(row['Red_NIS']) if row['Red_NIS']!='' else 0
                                    rgIoSum[48] += int(row['Non_Red_NIS']) if row['Non_Red_NIS']!='' else 0

                                if row["Analog_Input/Output_Type"] == "SAO(1)mA Type UIO (0-5000)":
                                    rgIoSum[49] +=int(row['Red_IS']) if row['Red_IS']!='' else 0
                                    rgIoSum[50] +=int(row['Non_Red_IS']) if row['Non_Red_IS']!='' else 0
                                    rgIoSum[51] +=int(row['Red_NIS']) if row['Red_NIS']!='' else 0
                                    rgIoSum[52] +=int(row['Non_Red_NIS']) if row['Non_Red_NIS']!='' else 0

                            for row in di_do_count_rows:
                                if row["Digital_Input/Output_Type"] == "SDI(1) 24Vdc UIO (0-5000)":
                                    rgIoSum[1] += int(row['Red_IS']) if row['Red_IS']!='' else 0
                                    rgIoSum[2] += int(row['Non_Red_IS']) if row['Non_Red_IS']!='' else 0
                                    rgIoSum[3] += int(row['Red_NIS']) if row['Red_NIS']!='' else 0
                                    rgIoSum[4] += int(row['Non_Red_NIS']) if row['Non_Red_NIS']!='' else 0
                                    rgIoSum[5] += int(row['Red_RLY']) if row['Red_RLY']!='' else 0
                                    rgIoSum[6] += int(row['Non_Red_RLY']) if row['Non_Red_RLY']!='' else 0

                                if row["Digital_Input/Output_Type"] == "SDO(1) 24Vdc 500mA UIO (0-5000)":
                                    rgIoSum[25] +=int(row['Red_IS']) if row['Red_IS']!='' else 0
                                    rgIoSum[26] +=int(row['Non_Red_IS']) if row['Non_Red_IS']!='' else 0
                                    rgIoSum[27] +=int(row['Red_NIS']) if row['Red_NIS']!='' else 0
                                    rgIoSum[28] +=int(row['Non_Red_NIS']) if row['Non_Red_NIS']!='' else 0
                                    rgIoSum[29] +=int(row['Red_RLY']) if row['Red_RLY']!='' else 0
                                    rgIoSum[30] +=int(row['Non_Red_RLY']) if row['Non_Red_RLY']!='' else 0
                            RIO_CNT = sum(rgIoSum)

                    rgIoSum.pop(0) #calculation started from index 1
                    expectedResult = [str(d) for d in rgIoSum]
                    for row in QT_Table.Rows:
                        if row['System_Item_GUID'] == Item.QuoteItemGuid:
                            if row['CG_Item_GUID'] == child.QuoteItemGuid:
                                row['RG'+str(n)] = "|".join(expectedResult)
                                row['Remote_IO'] = RIO_CNT
                                row['Remote_Qty'] = str(n)
                                if n == 1:
                                    row['RGNames'] = rg.PartNumber
                                else:
                                    row['RGNames'] = row['RGNames'] + "|" + rg.PartNumber
    QT_Table.Save()
    if SM != 'Yes':
        return False
    else:
        return True