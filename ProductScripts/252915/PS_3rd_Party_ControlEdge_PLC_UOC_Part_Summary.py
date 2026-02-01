import GS_PS_Exp_Ent_BOM
result_dic=dict()
if Product.GetContainerByName('LSS_Configuration_for_Rockwell_transpose') != None and Product.Attr('Migration_Scope_Choices').GetValue() != 'LABOR':
    base_media_delivery = Product.Attr('LSS_PLC_Base_Media_Delivery').GetValue()
    for row in Product.GetContainerByName('LSS_Configuration_for_Rockwell_transpose').Rows:
        controller_migrated = row['LSS_PLC_controllers_intend_to_migrate']
        sql_res = SqlHelper.GetList("Select * from LSS_3RD_PARTY_CONTROLEDGE_PLC_BOM where ('{}' = isPLC or '{}' = isUOC or '{}' = isvUOC) and (Operating_Temperature = '{}' or Operating_Temperature = '') and (Controller_Type = '{}' or Controller_Type = '') and (Power_Input_Type = '{}' or Power_Input_Type = '') and (Power_Supply_Type='{}' or Power_Supply_Type = '') and (Power_Status_Module_for_Redundant_Power_Supply='{}' or Power_Status_Module_for_Redundant_Power_Supply = '') and (Redundant_Controller_Physical_Separation_Required='{}' or Redundant_Controller_Physical_Separation_Required = '') and (IO_Rack_Type='{}'  or IO_Rack_Type = '') and (ControlEdge_PLC_System_Software_Release='{}' or ControlEdge_PLC_System_Software_Release = '') and (Base_Media_Delivery='{}' or Base_Media_Delivery = '') and (Ethernet_Switch_Type='{}' or Ethernet_Switch_Type = '') and (Ethernet_Switch_Ports='{}' or Ethernet_Switch_Ports = '') and (Network_Topology='{}' or Network_Topology = '') and (G3_Option_Ethernet_Switch='{}' or G3_Option_Ethernet_Switch = '')".format(row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_Operating_temp_for_Controller_Module'], row['LSS_PLC_Controller_Type'], row['LSS_PLC_Power_Input_Type'], row['LSS_PLC_Power_Supply_Type'], row['LSS_PLC_Power_Status_Module_for_Redundant_Pwr_Sply'], row['LSS_PLC_Redundant_Controller_Phy_Sep_Req'], row['LSS_PLC_IO_Rack_Type'], row['LSS_PLC_ControlEdge_PLC_System_Software_Release'], base_media_delivery,row['LSS_PLC_Ethernet_Switch_Type'], row['LSS_Ethernet_Switch_Ports'], row['LSS_PLC_Network_Topology'], "No" if row['LSS_PLC_G3_Option_Ethernet_Switch']=="" else row['LSS_PLC_G3_Option_Ethernet_Switch']))
        for i in sql_res:
            if i.Part_Number in ['SP-EMD170-ESD','SP-EMD171-ESD','SP-EMD172-ESD','SP-EMD174-ESD','SP-EMD170','SP-EMD171','SP-EMD172','SP-EMD174']:
                part_number1_sum=sum(result_dic.get('900CP1-0200',list()))
                part_number2_sum=sum(result_dic.get('900CP1-0300',list()))
                #Trace.Write(str(part_number1_sum)+str('        :::      ')+str(part_number2_sum))
                if part_number1_sum <= 0 and part_number2_sum <= 0:
                    continue
            part_number = result_dic.get(i.Part_Number,list())
            try:
                part_number.append(int(i.Qty) * int(controller_migrated))
            except:
                if row[i.Qty] =='':
                    part_number.append(0)
                else:
                    part_number.append(int(row[i.Qty]) * int(controller_migrated))
            result_dic[i.Part_Number]=part_number
    Trace.Write(str(result_dic))
    part_numbers=Product.Attr('PLC_UOC_BOM_Items')
    #Product.Attr('PLC_UOC_BOM_Items').Allowed=False
    #Product.Attr('PLC_UOC_BOM_Items').Allowed=True
if len(result_dic)>0:
    part_numbers_keys=[]
    for i in result_dic:
        if sum(result_dic[i]) != 0:
            part_numbers_keys.append(i)
    #part_numbers.SelectValues(*part_numbers_keys)
    Trace.Write(len(part_numbers_keys))
    for r in part_numbers_keys:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product, "PLC_UOC_BOM_Items", r, sum(result_dic[r]))
        #i.Quantity=sum(result_dic[i.UserInput])