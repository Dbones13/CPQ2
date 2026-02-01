def populatePASData(Quote):
 #["System_Group",   "System_Grp_GUID"   "System_Name"   "System_Item_GUID"  "CG_Name"   "CG_Item_GUID"  "CG"]
 hierarchy = {'Level0': "New / Expansion Project", 'Level1': "System Group", "Level2": "ControlEdge PLC System", "Level3":"CE PLC Control Group"}

 lst = ["CE_Site_Voltage", "PLC_IO_Filler_Module", "PLC_IO_Spare", "PLC_IO_Slot_Spare", "PLC_Shielded_Terminal_Strip", "CE_Selected_Products", "CE_Add_System_Rows", "CE_Apply_System_Number", "CE_Scope_Choices", "New_Expansion", "Sys_Group_Name", "PLC_Software_Release","PLC_CG_Name","PLC_RG_Name", "CE PLC Engineering Execution Year"]

 proj_columns = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']
 proj_columns_seq = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']

 sysgrp_columns = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']
 sysgrp_columns_seq = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']

 sys_columns = ['PLC_IO_Spare', 'PLC_IO_Slot_Spare', 'PLC_Marshalling_Cabinet_Cont']
 sys_columns_seq = ['PLC_IO_Spare', 'PLC_IO_Slot_Spare', 'PLC_Marshalling_Cabinet_Cont']

 cabinets_columns = ['Cabinet_cnt']
 cabinet_columns_seq = ['Cabinet_cnt']

 cg_columns = ['PLC_AI_Points', 'PLC_AI_HART_Points', 'PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500', 'PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500', 'PLC_Universal_Analog_Input8', 'PLC_Universal_Analog_Input8_TCRTDmVOhm', 'PLC_Analog_Input16', 'PLC_Analog_Output4', 'PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_DI_Points', 'PLC_DO_10_250', 'PLC_DO_250_500', 'PLC_Digital_Input32', 'PLC_Digital_Input16_120240VAC','PLC_Digital_Input16_125VDC', 'PLC_Digital_Input_Contact_Type16', 'PLC_Pulse_Input_Freq_Input4', 'PLC_Quadrature_Input', 'PLC_Pulse_Output4', 'PLC_Digital_Output32', 'PLC_Digital_Output8', 'PLC_Digital_Output_Relay8', 'PLC_Cabinet_Spare_Space', 'PLC_Integrated_Marshalling_Cabinet']

 cg_columns_seq = ['PLC_AI_Points', 'PLC_AI_Points_R', 'PLC_AI_HART_Points', 'PLC_AO', 'PLC_AO_R', 'PLC_AO_HART', 'PLC_Universal', 'PLC_Analog_Input16', 'PLC_Analog_Output4', 'PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_DI_Points', 'PLC_DI_Points_R', 'PLC_DO_Points', 'PLC_DO_Points_R', 'PLC_Digital_Input32','PLC_DI_Points_16', 'PLC_Digital_Input_Contact_Type16', 'PLC_Pulse_Input_Freq_Input4', 'PLC_Quadrature_Input', 'PLC_Pulse_Output4', 'PLC_Digital_Output32', 'PLC_Digital_Output8', 'PLC_Digital_Output_Relay8', 'PLC_Cabinet_Spare_Space', 'PLC_Integrated_Marshalling_Cabinet', 'PLC_AI_HART_Points_R','PLC_AO_HART_R']

 rg_columns = ['PLC_AI_Points', 'PLC_AI_HART_Points', 'PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500', 'PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500', 'PLC_Universal_Analog_Input8', 'PLC_Universal_Analog_Input8_TCRTDmVOhm', 'PLC_Analog_Input16', 'PLC_Analog_Output4', 'PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_DI_Points', 'PLC_DO_10_250', 'PLC_DO_250_500', 'PLC_Digital_Input32', 'PLC_Digital_Input16_120240VAC','PLC_Digital_Input16_125VDC', 'PLC_Digital_Input_Contact_Type16', 'PLC_Pulse_Input_Freq_Input4', 'PLC_Quadrature_Input', 'PLC_Pulse_Output4', 'PLC_Digital_Output32', 'PLC_Digital_Output8', 'PLC_Digital_Output_Relay8']

 rg_columns_seq = ['PLC_AI_Points', 'PLC_AI_Points_R', 'PLC_AI_HART_Points', 'PLC_AO', 'PLC_AO_R', 'PLC_AO_HART', 'PLC_Universal', 'PLC_Analog_Input16', 'PLC_Analog_Output4', 'PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_DI_Points', 'PLC_DI_Points_R', 'PLC_DO_Points', 'PLC_DO_Points_R', 'PLC_Digital_Input32', 'PLC_DI_Points_16', 'PLC_Digital_Input_Contact_Type16', 'PLC_Pulse_Input_Freq_Input4', 'PLC_Quadrature_Input', 'PLC_Pulse_Output4', 'PLC_Digital_Output32', 'PLC_Digital_Output8', 'PLC_Digital_Output_Relay8', 'PLC_AI_HART_Points_R','PLC_AO_HART_R']


 QT_Table = Quote.QuoteTables["PAS_Document_Data"]
 QT_Table.Rows.Clear()
 PLC = ''

 #for level 0
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
   newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem

 #for level 2
 for Item in Quote.MainItems:
  if hierarchy["Level2"] == Item.ProductName:
   PLC ='Yes'
   newRow = QT_Table.AddNewRow()
   newRow["System_Name"] = Item.ProductName
   newRow["System_Item_GUID"] = Item.QuoteItemGuid
   newRow["System_Grp_GUID"] = Item.ParentItemGuid
   newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
 if PLC != 'Yes':
  for row in QT_Table.Rows:
   if row["System_Name"] == 'ControlEdge PLC System':
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


 for row in QT_Table.Rows:
  n = 0 
  RIO_CNT = 0
  LIO_CNT = 0 
  for Item in Quote.Items:
   if row['Project_GUID'] == Item.QuoteItemGuid and Item.ProductName == "New / Expansion Project" and row['System_Group'] == '' and row['System_Name'] == '' and row['CG_Name'] == '':
    projdic = {}
    for attr in Item.SelectedAttributes:
     if attr.Name not in lst and "UOC" not in attr.Name:
      try:
       attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
       for column in attr_containers:
        if column.Name in proj_columns:
         projdic[column.Name] = column.Value
      except:
       pass

    expectedResult = [projdic[d] for d in proj_columns_seq if d in projdic.keys()]
    row['Project_Info'] = "|".join(expectedResult) 
   elif row['System_Grp_GUID'] == Item.QuoteItemGuid and Item.ProductName == "System Group" and row['System_Name'] == '' and row['CG_Name'] == '':
    Sysgrpdic = {}
    for attr in Item.SelectedAttributes:
     if attr.Name not in lst and "UOC" not in attr.Name:
      try:
       attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns

      except:
       pass
      for column in attr_containers:
       if column.Name in sysgrp_columns:
        #Trace.Write('==========='+str(column.Name))
        Sysgrpdic[column.Name] = column.Value

    expectedResult = [Sysgrpdic[d] for d in sysgrp_columns_seq if d in Sysgrpdic.keys()]
    row['System_grp'] = "|".join(expectedResult)
   elif row['System_Item_GUID'] == Item.QuoteItemGuid and Item.ProductName == "ControlEdge PLC System" and row['CG_Name'] == '':
    Sysdic = {}
    for attr in Item.SelectedAttributes:
     if attr.Name not in lst and "UOC" not in attr.Name:
      try:
       attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
      except:
       pass
      for column in attr_containers:
       if column.Name in sys_columns:  
        Sysdic[column.Name] = column.Value
    expectedResult = [Sysdic[d] for d in sys_columns_seq if d in Sysdic.keys()]
    row['System'] = "|".join(expectedResult)

   elif row['CG_ITEM_GUID'] == Item.QuoteItemGuid and Item.ProductName != "CE PLC Remote Group":
    CGdic = {}
    for attr in Item.SelectedAttributes:
     if attr.Name not in lst and "UOC" not in attr.Name:
      try:
       attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
      except:
       pass
      PLC_AO = 0
      PLC_AO_R = 0
      PLC_AO_HART = 0
      PLC_Universal = 0
      PLC_AO_HART_R = 0
      PLC_DO = 0
      PLC_DO_R = 0
      PLC_DI_Points_16 = 0
      for column in attr_containers:
       if column.Name in cg_columns:
        #Trace.Write("Column Name: "+str(column.Name)+"	 Container Name: "+str(attr.Name)+"	 Column Value: "+str(column.Value))
        #Trace.Write('==========='+str(column.Name))
        if column.Name in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
         PLC_AO = int(PLC_AO) + int(column.Value)
         CGdic["PLC_AO"] = str(PLC_AO)
         LIO_CNT += int(column.Value)
        elif column.Name in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
         PLC_AO_HART = int(PLC_AO_HART) + int(column.Value)
         CGdic["PLC_AO_HART"] = str(PLC_AO_HART)
         LIO_CNT += int(column.Value)
        elif column.Name in ['PLC_Universal_Analog_Input8', 'PLC_Universal_Analog_Input8_TCRTDmVOhm']:
         PLC_Universal = int(PLC_Universal) + int(column.Value)
         CGdic["PLC_Universal"] = str(PLC_Universal)
         LIO_CNT += int(column.Value)
        elif column.Name in ['PLC_DO_10_250', 'PLC_DO_250_500']:
         PLC_DO = int(PLC_DO) + int(column.Value)
         CGdic["PLC_DO_Points"] = str(PLC_DO)
         LIO_CNT += int(column.Value)
        elif column.Name in ['PLC_Digital_Input16_125VDC', 'PLC_Digital_Input16_120240VAC']:
         PLC_DI_Points_16 = int(PLC_DI_Points_16) + int(column.Value)
         CGdic["PLC_DI_Points_16"] = str(PLC_DI_Points_16)
         LIO_CNT += int(column.Value)
        elif column.Name in ['PLC_Cabinet_Spare_Space', 'PLC_Integrated_Marshalling_Cabinet']:
         CGdic[column.Name] = column.Value
        else:
         LIO_CNT += int(column.Value)
         CGdic[column.Name] = column.Value
      try:
       attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[1].Columns
      except:
       pass
      for column in attr_containers:
       if column.Name == 'PLC_AI_Points': 
        CGdic["PLC_AI_Points_R"] = column.Value
        LIO_CNT += int(column.Value)
       elif column.Name == 'PLC_AI_HART_Points':
        CGdic["PLC_AI_HART_Points_R"] = column.Value
        LIO_CNT += int(column.Value)
       elif column.Name in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
        PLC_AO_HART_R = int(PLC_AO_HART_R) + int(column.Value)
        LIO_CNT += int(column.Value)
       elif column.Name in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
        PLC_AO_R = int(PLC_AO_R) + int(column.Value)
        CGdic["PLC_AO_R"] = str(PLC_AO_R)
        LIO_CNT += int(column.Value)
       elif column.Name == 'PLC_DI_Points':
        CGdic["PLC_DI_Points_R"] = column.Value
        LIO_CNT += int(column.Value)
       elif column.Name in ['PLC_DO_10_250', 'PLC_DO_250_500']:
        PLC_DO_R = int(PLC_DO_R) + int(column.Value)
        CGdic["PLC_DO_Points_R"] = str(PLC_DO_R)
        LIO_CNT += int(column.Value)
    expectedResult = [CGdic[d] for d in cg_columns_seq if d in CGdic.keys()]
    #Trace.Write("Expected Result: "+str(expectedResult))
    row['CG'] = "|".join(expectedResult)
    row['Local_IO'] = LIO_CNT

   elif Item.ProductName == "CE PLC Remote Group" and Item.ParentItemGuid == row['CG_ITEM_GUID']:
    RGdic = {}
    n = n + 1
    for attr in Item.SelectedAttributes:
     if attr.Name not in lst and "UOC" not in attr.Name:
      try:
       attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
      except:
       pass
      PLC_AO = 0
      PLC_AO_R = 0
      PLC_AO_HART = 0
      PLC_Universal = 0
      PLC_AO_HART_R = 0
      PLC_DO = 0
      PLC_DO_R = 0
      PLC_DI_Points_16 = 0
      for column in attr_containers:
       if column.Name in rg_columns:
        #Trace.Write("RG Column Name: "+str(column.Name)+"	 Container Name: "+str(attr.Name)+"	 Column Value: "+str(column.Value))
        if column.Name in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
         plc_ao = int(column.Value) if column.Value else 0
         PLC_AO = int(PLC_AO) + plc_ao
         RGdic["PLC_AO"] = str(PLC_AO)
        elif column.Name in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
         plc_ao_hart = int(column.Value) if column.Value else 0
         PLC_AO_HART = int(PLC_AO_HART) + plc_ao_hart
         RGdic["PLC_AO_HART"] = str(PLC_AO_HART)
        elif column.Name in ['PLC_Universal_Analog_Input8', 'PLC_Universal_Analog_Input8_TCRTDmVOhm']:
         plc_univer = int(column.Value) if column.Value else 0
         PLC_Universal = int(PLC_Universal) + plc_univer
         RGdic["PLC_Universal"] = str(PLC_Universal)
        elif column.Name in ['PLC_DO_10_250', 'PLC_DO_250_500']:
         plc_do = int(column.Value) if column.Value else 0
         PLC_DO = int(PLC_DO) + plc_do
         RGdic["PLC_DO_Points"] = str(PLC_DO)
        elif column.Name in ['PLC_Digital_Input16_125VDC', 'PLC_Digital_Input16_120240VAC']:
         plc_di = int(column.Value) if column.Value else 0
         PLC_DI_Points_16 = int(PLC_DI_Points_16) + plc_di
         RGdic["PLC_DI_Points_16"] = str(PLC_DI_Points_16)
        else:
         RGdic[column.Name] = column.Value if column.Value else '0'
      try:
       attr_containers_r = Item.SelectedAttributes.GetContainerByName('PLC_RG_UIO_Cont').Rows[1].Columns
      except:
       pass
      for column in attr_containers_r:
       if column.Name == 'PLC_AI_Points':
        RGdic["PLC_AI_Points_R"] = column.Value if column.Value else '0'
       elif column.Name == 'PLC_AI_HART_Points':
        RGdic["PLC_AI_HART_Points_R"] = str(column.Value) if column.Value else '0'
       elif column.Name in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
        plc_val = int(column.Value) if column.Value else 0
        PLC_AO_HART_R = int(PLC_AO_HART_R) + plc_val
        RGdic["PLC_AO_HART_R"] = str(PLC_AO_HART_R)
       elif column.Name in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
        plc_val = int(column.Value) if column.Value else 0
        PLC_AO_R = int(PLC_AO_R) + plc_val
        RGdic["PLC_AO_R"] = str(PLC_AO_R)
       elif column.Name == 'PLC_DI_Points':
        RGdic["PLC_DI_Points_R"] = column.Value if (column.Value) else '0'
       elif column.Name in ['PLC_DO_10_250', 'PLC_DO_250_500']:
        plc_dval = int(column.Value) if column.Value else 0
        PLC_DO_R = int(PLC_DO_R) + plc_dval
        RGdic["PLC_DO_Points_R"] = str(PLC_DO_R)
    expectedResult = [RGdic[d] for d in rg_columns_seq if d in RGdic.keys()]
    #Trace.Write("RG-Expected Result: "+str(expectedResult))
    row['RG'+str(n)] = "|".join(expectedResult)
    rg_list = [int(i) for i in row['RG'+str(n)].split("|")]
    RIO_CNT += sum(rg_list)
    row['Remote_IO'] = RIO_CNT
    row['Remote_Qty'] = str(n)
    if n == 1:
     row['RGNames'] = Item.PartNumber
    else:
     row['RGNames'] = row['RGNames'] + "|" + Item.PartNumber

 for row in QT_Table.Rows:
  Cabinet_cnt = 0
  Cabinet_dic = {}
  if row['System_Name'] == "ControlEdge PLC System" and row['CG_Name'] == '':
   for Item in Quote.Items:
    if Item.PartNumber in ('CC-CBDS01', 'CC-CBDD01') and Item.RolledUpQuoteItem[:3] == row['RolledUpQuoteItem'][:3]:
     Cabinet_cnt += Item.Quantity
     Cabinet_dic["Cabinet_cnt"] = str(Cabinet_cnt)
   expectedResult = [Cabinet_dic[d] for d in cabinet_columns_seq if d in Cabinet_dic.keys()]
   row["Cabinets"] = "|".join(expectedResult)
  if row['System_Name'] == "ControlEdge PLC System" and row['CG_Name'] != '':
   if row['Remote_IO'] == '':
    row['Remote_IO'] = '0'
    row['Remote_Qty'] = '0'

 QT_Table.Save()

 if PLC != 'Yes':
  return False
 else:
  return True
#populatePASData(Quote)