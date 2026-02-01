def getFloat(Var):
    if Var:
        return float(Var)
    return 0.0

Cond = TagParserQuote.ParseString("[AND]([OR](([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PAS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC))),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects), [GT](<*Table(select COUNT(*) from cart_item i where i.CATALOGCODE = 'PRJT' and i.cart_id=<*CTX(Quote.CartId)*> and i.USERID=<*CTX(Quote.OwnerId)*>)*>,0))")

if Cond == '1':
    
    hierarchy = {"L1":"System Group","L2":"PMD System"}
    pb_interface_col = ['Device','Devices','AI','AO','DI','DO']
    pb_cont_lst = ['PMD_Profibus_Drives_Cont','PMD_Profibus_Links_and_Gateways_Cont','PMD_Profibus_Motor_Starters and_CD_Cont','PMD_Other_Profibus_DP-Devices_Cont','PMD_Profibus_Modular_IO_Cont','PMD_Profibus_Displays_Cont','PMD_Profinet_Device_Support_blocks_Cont']
    
    Qt_Table = Quote.QuoteTables["PMD_Profibus_Interface"]
    Qt_Table.Rows.Clear()
    
    for Item in Quote.MainItems:
        if hierarchy["L1"] == Item.ProductName: 
            newRow = Qt_Table.AddNewRow()
            newRow["System_Group"] = Item.PartNumber
            newRow["System_Grp_GUID"] = Item.QuoteItemGuid 
            #newRow["System_Item_GUID_"] = Item.QuoteItemGuid
            
    for row in Qt_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["L2"] == Item.ProductName:
                row["System_Name"] = Item.ProductName
                
    
        
    
    Qt_Table.Save()
    
    for row in Qt_Table.Rows:
        for Item in Quote.MainItems:
            if Item.ParentItemGuid == row["System_Grp_GUID"]:
                row["System_Item_GUID_"] = Item.QuoteItemGuid
            prob_dic = {}
            prob_dic2 = {}
            prob_dic3 = {}
            prob_dic4 = {}
            prob_dic5 = {}
            prob_dic6 = {}
            prob_dic7 = {}
                
            if row["System_Item_GUID_"] == Item.QuoteItemGuid:              
                try:   
                    attr_cont = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Drives_Cont')        
                except:
                    pass
                try:
                    num = attr_cont.Rows.Count
                    for i in range(0,num):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]  
                             
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Drives_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic[column.Name] = column.Value
                                Trace.Write(column.Value) 
                            res = [prob_dic[d] for d in pb_interface_col if d in prob_dic.keys()]
                            newRow['PI_1'] = "|".join(res)
                            
                             
                        Trace.Write("0000000000000000000000000000000000000000000000000000000000000000000000000")        
                   
                except:
                    pass
                
                
                try:   
                    attr_cont2 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Links_and_Gateways_Cont')        
                except:
                    pass
                try:
                    num2 = attr_cont2.Rows.Count
                    for i in range(0,num2):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Links_and_Gateways_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic2[column.Name] = column.Value
                                Trace.Write(column.Value) 
                            res = [prob_dic2[d] for d in pb_interface_col if d in prob_dic2.keys()]
                            newRow['PI_2'] = "|".join(res)    
                        Trace.Write("11111111111111111111111111111111111111111111111111111111111111111111")            
                except:
                    pass
                
                try:   
                    attr_cont3 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Motor_Starters and_CD_Cont')        
                except:
                    pass
                try:
                    num3 = attr_cont3.Rows.Count
                    for i in range(0,num3):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Motor_Starters and_CD_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic3[column.Name] = column.Value
                                Trace.Write(column.Value) 
                        res = [prob_dic3[d] for d in pb_interface_col if d in prob_dic3.keys()]
                        newRow['PI_3'] = "|".join(res)         
                        Trace.Write("222222222222222222222222222222222222222222222222222222222222222222222222222222222")            
                except:
                    pass
                
                try:   
                    attr_cont4 = Item.SelectedAttributes.GetContainerByName('PMD_Other_Profibus_DP-Devices_Cont')        
                except:
                    pass
                try:
                    num4 = attr_cont4.Rows.Count
                    for i in range(0,num4):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Other_Profibus_DP-Devices_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic4[column.Name] = column.Value
                                Trace.Write(column.Value) 
                        res = [prob_dic4[d] for d in pb_interface_col if d in prob_dic4.keys()]
                        newRow['PI_4'] = "|".join(res)        
                        Trace.Write("333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")            
                except:
                    pass
                 
                try:   
                    attr_cont5 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Modular_IO_Cont')        
                except:
                    pass
                try:
                    num5 = attr_cont5.Rows.Count
                    for i in range(0,num5):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Modular_IO_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic5[column.Name] = column.Value
                                Trace.Write(column.Value) 
                        res = [prob_dic5[d] for d in pb_interface_col if d in prob_dic5.keys()]
                        newRow['PI_5'] = "|".join(res)         
                        Trace.Write("44444444444444444444444444444444444444444444444444444444444")            
                except:
                    pass 
                    
                try:   
                    attr_cont6 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Displays_Cont')        
                except:
                    pass
                try:
                    num6 = attr_cont6.Rows.Count
                    for i in range(0,num6):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Profibus_Displays_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic6[column.Name] = column.Value
                                Trace.Write(column.Value) 
                        res = [prob_dic6[d] for d in pb_interface_col if d in prob_dic6.keys()]
                        newRow['PI_6'] = "|".join(res)        
                        Trace.Write("5555555555555555555555555555555555555555555555555555555555555555555555555555555555")            
                except:
                    pass 

                try:   
                    attr_cont7 = Item.SelectedAttributes.GetContainerByName('PMD_Profinet_Device_Support_blocks_Cont')        
                except:
                    pass
                try:
                    num7 = attr_cont7.Rows.Count
                    for i in range(0,num7):
                        newRow = Qt_Table.AddNewRow()
                        newRow["System_Item_GUID_"] = Item.QuoteItemGuid
                        newRow["System_Group"] = row["System_Group"]
                        try:
                            cont_1 = Item.SelectedAttributes.GetContainerByName('PMD_Profinet_Device_Support_blocks_Cont').Rows[i].Columns
                        except:
                            pass
                        for column in cont_1:
                            if column.Name in ['Device']:
                                newRow['Device_Code'] =  column.Value
                            elif column.Name in ['Devices','AI','AO','DI','DO']:
                                prob_dic7[column.Name] = column.Value 
                                Trace.Write(column.Value)        
                        res = [prob_dic7[d] for d in pb_interface_col if d in prob_dic7.keys()]
                        newRow['PI_7'] = "|".join(res)        
                        Trace.Write("66666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666")            
                except:
                    pass   
                    
            Qt_Table.Save()