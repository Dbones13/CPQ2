import re
product_list = ['R2Q New / Expansion Project', 'R2Q C300 System', 'R2Q Series-C Control Group', 'R2Q Series-C Remote Group', 'R2Q System Group','R2Q Experion Enterprise System','R2Q Experion Enterprise Group','R2Q eServer System','R2Q eServer System Group','R2Q Field Device Manager','R2Q FDM System Group','R2Q 3rd Party Devices/Systems Interface (SCADA)','R2Q CCR','R2Q ControlEdge UOC System','R2Q UOC Control Group','R2Q UOC Remote Group','R2Q Safety Manager','R2Q Safety Manager FGS','R2Q Safety Manager ESD','R2Q SM Control Group','R2Q SM Remote Group','HC900 System','HC900 Group','R2Q ControlEdge PLC System','CE PLC Control Group','CE PLC Remote Group','Terminal Manager','Industrial Security (Access Control)','Fire Detection & Alarm Engineering','Digital Video Manager','Tank Gauging Engineering','Operator Training','Small Volume Prover','Skid and Instruments']
excluded_columns = { 'AI', 'AO', 'DI','DO','C300_CONTROLLER', 'C300_Controller_and_IO_Cabinet_Sum', 'C300_MAR_PARTS', 'C300_Sys_Cabinets', 'Crate Design', 'Crate Type', 'DCS Universal Marshalling Cabinet is', 'DCS Universal Marshalling Cabinet nis', 'Experion_PKS_Software_Release', 'Labor_parameter_is', 'MIB Configuration Required?', 'New_Expansion', 'RemoteGroupCount', 'Sys_Group_Name', 'Total CG Local Io Proposal', 'Total RG Local Io Proposal', 'Total_SCAB', 'total_family_CG_ios_doc', 'CG_CN100_IO_HIVE_Redundancy', 'C300_RG_UPC_FTA', 'Controller_Module_Type_CGRG', 'TION_Val', 'Total_IO_Load', 'Total_IO_Point_Load','UniversalMarshallingCabinet','Enterprise_flag_check','Staging_C300_Marshal_Cabinets','SerC_CG_Control_Networking_Module_Required','PCNT05_Val','PCNT_Val','SerC_CG_IOTA_Carrier_Cover','Controller_Type','Remote_group_Io_family','Total_Profibus_Red_NonRed_IOs','Total_Sumof_FF_IOs','ethernet_ios','Enterprise_Groups_list','cluster1','DCS Universal umc Marshalling Cabinet is','Uni_marshling','Univ_Marshalling_Value','controler_required','RG_SYSTEM_CABINET_COUNT','DCS_UMCcabinet','QTY_CC_TION11','Total_CN100','Doc_Umc_total_32','Dummy_RG_IO_Mounting_Solution','DCS_UMCcabinet','QTY_CC_TION11','Number of FTE Communities','Number of FTE Community Locations','Number of Locations with FTE Switches','Experion_HS_Ges_Location_Labour','Network and Server Cabinet Count','Number of Console Sections with Hardwired IO','Number of FTE Communities','Number of FTE Community Locations','Number of Locations with FTE Switches','Experion_HS_Ges_Location_Labour','Network and Server Cabinet Count','Number of Console Sections with Hardwired IO','C300_RG_UPC_Cab_Count','C300_RG_UPC_Universal_IO_Count','Is Modbus Interface in Scope','Is Profibus Interface in Scope','Is System Network Engineering in Scope','Is Terminal Server Interface in Scope','Is OPC Interface in Scope','Is HART Interface in Scope','Is Fieldbus Interface in Scope','Is EtherNet IP Interface in Scope','Is DeviceNet Interface in Scope','IO_Type_info', 'IO_Type Info Icon', 'SM_CG_RelayTypeForESD','ERP_System_Interface_Required','Proposal_belongs_to_Saudi_Armco','Web_Portal_Interface_Required','SM_CNM_Switch_Network_IOTA','SM_DNP3_ProtocolLicense','SM_Experion_Integration','SM_SCController_Architecture','SM_Safenet_Options','SM_Switch_Safety_IO','Sequence_Events'}
excluded_columns_secondary={'IO_Type_with_hint', 'Deliverable_w_hint', 'IO_Type_Icon','Selected_Products','Labor_IS','CE_Site_Frequency','CE_Site_Voltage','Contracting Parties','Estimated_Project_Value_Cost','Internal Parties','Project Exeuction Locations','Project Team Size','Project Type','AI', 'AO', 'DI','DO','Project Category','R2Q_PRJT_Proposal Language','CE_Selected_Products','Additional_Stations','CE_Scope_Choices','EBR_DATA','EBR_Software_Required','Enterprise_flag_check','Experion Enterprise Group Number','Experion Software Release','Experion_Process_Points','tps required','Labor_Parameter_Sta_Quantity','Labor_para_var_4','Labor_para_var_5','Labor_para_var_7','Labor_para_var_8','MIB Configuration Required?','New/Exp','Supervisory Network Type','Sys_Group_Name','staging_Number_of_Experion_Servers_exp_ent_group','staging_Number_of_Stations_Console','DCS_UMCcabinet','QTY_CC_TION11','Total_CN100','Doc_Umc_total_32','Dummy_RG_IO_Mounting_Solution','DCS_UMCcabinet','QTY_CC_TION11','Number of FTE Communities','Number of FTE Community Locations','Number of Locations with FTE Switches','Experion_HS_Ges_Location_Labour','Network and Server Cabinet Count','Number of Console Sections with Hardwired IO','C300_RG_UPC_Cab_Count','C300_RG_UPC_Universal_IO_Count','Is Modbus Interface in Scope','Is Profibus Interface in Scope','Is System Network Engineering in Scope','Is Terminal Server Interface in Scope','Is OPC Interface in Scope','Is HART Interface in Scope','Is Fieldbus Interface in Scope','Is EtherNet IP Interface in Scope','Is DeviceNet Interface in Scope','Rank','Identifiers','GESLocation','Distance_SM_SC_UIO/DIO_modules','SM_CG_RelayTypeForESD','IO_Type_info', 'IO_Type Info Icon','UOC_Ethernet_Switch_Type','UOC_Power_Supply', 'UOC_Ges_Location_Labour','ERP_System_Interface_Required','Proposal_belongs_to_Saudi_Armco','Web_Portal_Interface_Required','Type_of_TAS_System','SM_CNM_Switch_Network_IOTA','SM_DNP3_ProtocolLicense','SM_Experion_Integration','SM_SCController_Architecture','SM_Safenet_Options','SM_Switch_Safety_IO','Sequence_Events','CNM_SFP_Type','External _24VDC_Terminal_Block','Power_Supply_Redundancy','Fiber_Optic_Extender','Field_Termination_Assembly_for_PDIO','Number_of_SFP_0-500','Cabinet_Material_Type_Ingress_Protection','Abu_Dhabi_Build_Loc','Ambient_Temperature_Range','Power_Supply_Type','Earth_Leakage_Detector_TELD','IO_Redundancy','Wire_Routing_Options','Temperature_Monitoring','Field_Termination_Assembly_for_PUIO','Number_of_Control_Network_Module_0-100','ATEX_Compliance','Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet','Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet','UI_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet','SM_Historian_Basic_SW','Extended_Temperature','Cabinet_Access','SM_Cluster','SM_Controller_Simulation_License','SM_Historian_Basic_Database_Ext','SM_Historian_Basic_Server_1Client','SM_System_Scope','Implementation_Methodology','SM_Historian_Basic_Database_Ext','Cabinet Layout','Cabinet Layout','Cabinet Power','Supply Vendor','SIC_Length','ELD_Module','Cabinet_Thermostat','Cabinet_Light','Cabinet_Feeder_Voltage','IOTA_Ethernet_Cable_Length','SM_RG_RelayTypeForESD','Cabinet_IP_Rating','Fault_Contact_GIIS_Integration_Boards'}
excluded_attributes = {'R2Q_CONFIGURATION', 'WriteInProduct','Estimated Project Value (Cost)','Selected_Products','Order_Status','FAT Duration in weeks','Is Modbus Interface in Scope?','Is OPC Interface in Scope?','Project Duration (in weeks)','R2Q Select Category','Staging_C300_Marshal_Cabinets','Input_Quality (User Requirement Specification)','Experion_PKS_Software_Release','No_of_Complex_Operations_per_Product (0-100)','No_of_Complex_SCMs_per_Unit (0-100)','SerC_CG_MIB_Configuration_Required','UOC_I/O_IsModified','C300_RG_UPC_FTA','MSID_GES_Location','FIM_FIM4_Not_Recommended','FIM_Segment_Calc_PC_Questions','Is EtherNet IP Interface in Scope?','Is Fieldbus Interface in Scope?','Is Profibus Interface in Scope?','SerC_IO_Params','flag_load_parts_cont','Labor_Loop_Drawings','Labor_Marshalling_Database','C300_Implementation_Methodology','C300_GES_Location','Ser_RG_Universal_Marshalling_Cabinet','Additional_Stations','Application Enablers','CMS Remote Peripheral Solution Type RPS','DSA Enablers','Desk _Mount_Server','Implementation Methodology','Interface with TPS Required?','PERF_ExecuteScripts','Remote Peripheral Solution Type (RPS) - (Flex Server -Cabinet)','Number of EtherNet IP Interface Types','Number of Modbus Interfaces Types','Number of OPC Interface Types','Number of Operator Console Sections','Number of Profibus Interface Types','Number of Station Types','SafeView Factor (Max quanity of Monitors in One Station)','R2Q_EGAP_Approval','R2Q_UOC_IO_Total','QTY_CC_TION11','Total_CN100','RG_SYSTEM_CABINET_COUNT','Doc_Umc_total_32','DCS_UMCcabinet','Number of FTE Communities','Number of FTE Community Locations','Number of Locations with FTE Switches','Experion_HS_Ges_Location_Labour','Network and Server Cabinet Count','Number of Console Sections with Hardwired IO','Calculate_Trigger','Labor_parameter_ai','Labor_parameter_ao','Labor_parameter_di','Labor_parameter_do','Labor_parameter_is','Sell Price Strategy','eServer_name','Rack_Mount_Server','Enhanced_function_message','SerC_CG_Control_Networking_Module_Required','SerC_CG_C300_Controller_Module_Type','SerC_IO_Mounting_Solution','SM_RG_IO_Count_Digital_Input_Cont','SM_RG_IO_Count_Digital_Output_Cont','SM_RG_IO_Count_Analog_Input_Cont','SM_RG_IO_Count_Analog_Output_Cont','OPC_server_redundancy_required','Domain_Controller_Required','Opc_server_required','UOC_Ethernet_Switch_Type','UOC_Power_Supply','ERP_System_Interface_Required','Proposal_belongs_to_Saudi_Armco','Web_Portal_Interface_Required','Type_of_TAS_System','C300_Marshalling_cabinet_count (0-500)','Orion_Console_Units_Config','Number of Server Types',  'Number of OPC Interfaces', 'Number of Fieldbus Devices', 'Number of Profibus Devices', 'Number of EtherNet IP Devices', 'Number of EtherNet IP Interface Cards', 'Number of Profibus Interface Cards','FDM_GES_Location','CE_Add_System_Rows','SerC_RG_Marshalling_Cabinet_Type','SerC_CG_Marshalling_Cabinet_Type','Customer_Budget_TextField'}
ControlEdgeUOCSystem ={"Cabinet_Required_Racks_Mounting","CE_Add_System_Rows","UOC_Cluster","UOC_IO_Filler_Module","UOC_Shielded_Terminal_Strip","UOC_Starter_Kit_with_Experion_License","UOC_Starter_Kit", "UOC_Ges_Location_Labour"}
UOCRemoteGroup ={"UOC_Field_Wiring_DIDOAOAI_Channel_Mod","UOC_Field_Wiring_Other_Mod","UOC_Power_Input","UOC_Power_Status_Mod_Redundant_Supply","UOC_Remote_Terminal_Cable_Length","UOC_RG_Name"}
UOCControlGroup ={"Cabinet_Required_Racks_Mounting","UOC_Cabinet_Base_Size","UOC_Cabinet_Door_Keylock","UOC_Cabinet_Door_Type","UOC_Cabinet_Light","UOC_Cabinet_Power_Entry","UOC_Cabinet_Thermostat","UOC_Cabinet_Type","UOC_Ethernet_Switch_Supplier","UOC_Ethernet_Switch_Type","UOC_Field_Wiring_DIDOAOAI_Channel_Mod","UOC_Field_Wiring_Other_Mod","UOC_Network_Topology","UOC_Power_Input","UOC_Power_Status_Mod_Redundant_Supply","UOC_Remote_Terminal_Cable_Length","UOC_Remote_Terminal_Panel_Cable_Type","UOC_CG_Name","UOC_Cabinet_Required_Racks_Mounting","UOC_Ges_Location_Labour","UOC_IO_Rack_Type","UOC_Power_Supply"}
required_containers = { "C300_CG_Universal_IO_cont_1", "C300_CG_Universal_IO_cont_2", "SerC_CG_Enhanced_Function_IO_Cont", "SerC_CG_Enhanced_Function_IO_Cont2", "SerC_CG_FIM_FF_IO_Cont", "Series_C_Remote_Groups_Cont","C300_RG_Universal_IO_cont_1","C300_RG_Universal_IO_cont_2","SerC_RG_Enhanced_Function_IO_Cont","SerC_RG_Enhanced_Function_IO_Cont2","Number_of_Series_C_Control_Groups","C300_TurboM_IOM_CG_Cont","C300_CG_Universal_IO_Mark_1","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont", "C300_CG_Universal_IO_Mark_2","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1","C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont","C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1","C300_TurboM_IOM_RG_Cont","C300_UPC_Labor_IO_count_RG_2","C300_UPC_Labor_IO_count_RG_1",""}
Select_Category=''
def replace_series_c_control_group(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "Child_Products" and isinstance(value, dict):
                new_child_products = {}
                for sub_key, sub_value in value.items():
                    if sub_key == "Series-C Control Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("Series_C_CG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "Series-C Remote Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("Series_C_RG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "Experion Enterprise Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("Experion Enterprise Group Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "UOC Control Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("UOC_CG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "UOC Remote Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("UOC_RG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "SM Control Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("SM_CG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "SM Remote Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("SM_RG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "CCR" and isinstance(sub_value, dict):
                        new_key = sub_value.get("CCR_group_name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "HC900 Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("HC900_Group_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "CE PLC Control Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("PLC_CG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "CE PLC Remote Group" and isinstance(sub_value, dict):
                        new_key = sub_value.get("PLC_RG_Name", sub_key)
                        new_child_products[new_key] = replace_series_c_control_group(sub_value)
                    elif sub_key == "Terminal Manager" and isinstance(sub_value, dict):
                        new_child_products['TM'] = replace_series_c_control_group(sub_value)
                    else:
                        new_child_products[sub_key] = replace_series_c_control_group(sub_value)
                new_data[key] = new_child_products
            else:
                new_data[key] = replace_series_c_control_group(value)
        return new_data
    elif isinstance(data, list):
        return [replace_series_c_control_group(item) for item in data]
    return data
def hiddenval(colName,attr_Name,product):
    if colName in ['IO_Type','Digital Input Type','Analog Input Type','Digital Output Type','Analog Output Type','Digital_Input/Output_Type','Analog_Input/Output_Type','Third_Party_Devices_Systems_Interface_SCADA','UOC_AI_Points','UOC_AI_Points','UOC_Universal_Analog_Input8']:
        return 'Editable'
    else:
        if attr_Name=='SM_RG_Cabinet_Details_Cont_Left' and colName=='Power_Supply':
            return 'Hidden'
        elif attr_Name=='SM_RG_Cabinet_Details_Cont' :
            if  colName == 'SM_Percent_Installed_Spare_IO':
                return 'Editable'
            else:
                return 'Hidden'

        else:
        	return product.ParseString('<*CTX ( Container('+attr_Name+').Column('+colName+').GetPermission )*>')

def gettab(product):
    return [va.Name for tab in product.Tabs if tab.Name not in ('Labor Deliverables','Part Summary','Product_Cnfig_Debug') for va in tab.Attributes if str(va.Access) != 'Hidden' and va.Allowed]
def is_non_zero_int_string(val):
    try:
        return int(val) != 0
    except (ValueError, TypeError):
        return False

def checkvalues(containerRowDict):
    keys_to_ignore = {
        'Digital Input Type', 'IO_Type', 'Rank', 'Digital Output Type',
        'Analog Input Type', 'Analog Output Type',
        'Digital_Input/Output_Type', 'Analog_Input/Output_Type',
        'Third_Party_Devices_Systems_Interface_SCADA',
        'UOC_AI_Points', 'UOC_Universal_Analog_Input8', 'Parent_Product','Analog_Input_Type','Analog_Output_Type','Digital_Input_Type','Digital_Output_Type'
    }

    # Check if any trigger key is present
    ignore_keys = keys_to_ignore.union({'Scada_check','Rank'})
    if any(k in containerRowDict for k in keys_to_ignore):
        # Filter relevant items and check if any is a non-zero integer string
        return any(
            is_non_zero_int_string(val)
            for key, val in containerRowDict.items()
            if key not in ignore_keys
        )
    else:
        return True

def extractProductContainer(attrName, product):
    containerList = []
    containerLabelList = []
    product_name = str(product.Name.replace("R2Q ", ""))
    containerRows = product.GetContainerByName(attrName).Rows
    if containerRows.Count > 0:
        for i, containerRow in enumerate(containerRows):
            if product_name in ["ControlEdge UOC System"] and attrName  in ControlEdgeUOCSystem:
                continue
            elif product_name in ["UOC Control Group"] and attrName  in UOCControlGroup:
                continue
            elif product_name in ["UOC Remote Group"] and attrName  in UOCRemoteGroup:
                continue
            if attrName in ["Series_C_Control_Groups_Cont", "Series_C_Remote_Groups_Cont"]:
                containerRowDict = {col.Name: col.DisplayValue if  col.DisplayType=='DropDown' else containerRow[col.Name]  for col in containerRow.Columns if col.Name not in excluded_columns and hiddenval(col.Name,attrName,product)!='Hidden'}
                containerRowDictlable = {col.Name: col.HeaderLabel for col in containerRow.Columns if col.Name not in excluded_columns and hiddenval(col.Name,attrName,product)!='Hidden'}
            else:
                containerRowDict = {col.Name: col.DisplayValue if  col.DisplayType=='DropDown' else containerRow[col.Name] for col in containerRow.Columns if col.Name not in excluded_columns_secondary and hiddenval(col.Name,attrName,product)!='Hidden' }
                containerRowDictlable = {col.Name: col.HeaderLabel for col in containerRow.Columns if col.Name not in excluded_columns_secondary and hiddenval(col.Name,attrName,product)!='Hidden' }
            if containerRow.Product and containerRow.Product.Name in product_list:
                containerRowDict["Child_Products"] = {}
                containerRowDictlable["Child_Products"] = {}
                extractProductAttributes(containerRowDict["Child_Products"], containerRowDictlable["Child_Products"], containerRow.Product)
            if product_name =="SM Remote Group":
                enclosure_type = product.Attr('SM_RG_Enclosure_Type').GetValue()
                if enclosure_type not in ['Universal Safety Cab-1.3M']:
                    marCab = product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
                    if marCab  in ['Universal Marshalling','Universal_Marshalling']:
                        Trace.Write("containerRowDict"+str(containerRowDict))
                        if ('Digital_Input_Type' in containerRowDict and containerRowDict['Digital_Input_Type'] in ('SDI(1) 24Vdc UIO  (0-5000)','SDI(1) 24Vdc DIO  (0-5000)')) or ('Digital_Output_Type' in containerRowDict and containerRowDict['Digital_Output_Type'] in ('SDO(1) 24Vdc 500mA UIO  (0-5000)','SDO(1) 24Vdc 500mA DIO  (0-5000)')) or ('Analog_Input_Type' in containerRowDict and containerRowDict['Analog_Input_Type'] in ('SAI(1)mA type Current  UIO  (0-5000)')) or ('Analog_Output_Type' in containerRowDict and containerRowDict['Analog_Output_Type'] in ('SAO(1)mA Type UIO   (0-5000)')) or ('Marshalling_Option' in containerRowDict) or ('Enclosure_Type' in containerRowDict) or('SM_Percent_Installed_Spare_IO' in containerRowDict ):
                            getadd=checkvalues(containerRowDict)
                            if getadd:
                                containerList.append(containerRowDict)
                                containerLabelList.append(containerRowDictlable)
                        else:
                            continue
                    else:
                        if ('Digital_Input_Type' in containerRowDict and containerRowDict['Digital_Input_Type'] in ('SDI(1) 24Vdc UIO  (0-5000)','SDI(1)  24Vdc SIL2 P+F UIO  (0-5000)','SDI(1)  24Vdc SIL3 P+F UIO  (0-5000)','SDI(1) 24Vdc DIO  (0-5000)')) or ('Digital_Output_Type' in containerRowDict and containerRowDict['Digital_Output_Type'] in ('SDO(1) 24Vdc 500mA UIO  (0-5000)','SDO(1) 24Vdc SIL3 P+F UIO  (0-5000)','SDO(1) 24Vdc 500mA DIO  (0-5000)')) or ('Analog_Input_Type' in containerRowDict and containerRowDict['Analog_Input_Type'] in ('SAI(1)mA type Current  UIO  (0-5000)','SAI(1) mA Type Current P+F UIO  (0-5000)')) or ('Analog_Output_Type' in containerRowDict and containerRowDict['Analog_Output_Type'] in ('SAO(1)mA Type UIO   (0-5000)','SAO(1)mA Type P+F UIO  (0-5000)')) or ('Marshalling_Option' in containerRowDict) or ('Enclosure_Type' in containerRowDict) or('SM_Percent_Installed_Spare_IO' in containerRowDict ):
                            getadd=checkvalues(containerRowDict)
                            if getadd:
                                containerList.append(containerRowDict)
                                containerLabelList.append(containerRowDictlable)
                        else:
                            continue
                else:
                    if attrName in ['SM_RG_Universal_Safety_Cabinet_1.3M_Cont','SM_SC_Universal_Safety_Cab_1_3M_Details_cont','SM_RG_ATEX Compliance_and_Enclosure_Type_Cont','SM_RG_IO_Count_Analog_Input_1.3_Cabinet_Cont','SM_RG_IO_Count_Digital_Input_1.3_Cabinet_Cont']:
                        getadd=checkvalues(containerRowDict)
                        if getadd:
                            containerList.append(containerRowDict)
                            containerLabelList.append(containerRowDictlable)
            else:
                getadd = False
                if Select_Category == 'TA System' and attrName == 'CE_System_Cont' and len(containerRowDict) != 0:
                    getadd = checkvalues(containerRowDict)
                else:
                    getadd = checkvalues(containerRowDict)

                if getadd:
                    containerList.append(containerRowDict)
                    containerLabelList.append(containerRowDictlable)
    return containerList, containerLabelList


def extractProductAttributes(attributedict, attributedictlable, product):
    product_name = str(product.Name.replace("R2Q ", ""))
    skipcontainer=[]
    keylist=['Series_C_CG_Name','Series_C_RG_Name','Experion Enterprise Group Name','UOC_CG_Name','UOC_RG_Name','SM_CG_Name','SM_RG_Name','CCR_group_name','HC900_Group_Name','PLC_CG_Name','PLC_RG_Name','DVM_System_Group_Name']
    if product.Name in product_list:
        if product.Name in["Industrial Security (Access Control)","Tank Gauging Engineering","Fire Detection & Alarm Engineering","Digital Video Manager"]:
           visible_attrs= [va.Name for tab in product.Tabs if tab.Name in ('Personnel Access Control','Tank Gauging','Fire Alarm Panel','CCTV System') for va in tab.Attributes if str(va.Access) != 'Hidden' and va.Allowed]
        else:
           visible_attrs = gettab(product)
        if product_name =='New / Expansion Project':
            skipcontainer=['Labor_details_newexapnsion_cont2']
        if product_name=="SM Remote Group":
            enclosure_type=product.Attr('SM_RG_Enclosure_Type').GetValue()
            if enclosure_type =='Universal Safety Cab-1.3M':
                skipcontainer=['SM_RG_IO_Count_Analog_Input_Cont','SM_RG_IO_Count_Digital_Output_Cont','SM_RG_IO_Count_Digital_Input_Cont','SM_RG_IO_Count_Analog_Output_Cont']
        if product_name == 'System Group':
            for attr in product.Attributes:
                if (attr.Name in visible_attrs) or (attr.Name in keylist):
                    if str(attr.Access)!='Hidden' and attr.Allowed==True:
                        if attr.DisplayType == 'Container' and attr.Name not in ('R2Q_CONFIGURATION', 'WriteInProduct','C300_UPC_Labor_IO_count_RG_1','C300_UPC_Labor_IO_count_RG_2'):
                            container_data, container_labels = extractProductContainer(attr.Name, product)
                            if container_data:
                                for child_data, child_label in zip(container_data, container_labels):
                                    if "Child_Products" in child_data:
                                        attributedict.update(child_data["Child_Products"])
                                        attributedictlable.update(child_label["Child_Products"])
            return
        if "product_name" not in attributedict:
            attributedict["product_name"] = product_name
            attributedictlable["product_name"] = product_name
        if product_name not in attributedict:
            attributedict[product_name] = {}
            attributedictlable[product_name] = {}  
        for attr in product.Attributes:
            if (attr.Name in visible_attrs) or (attr.Name in keylist):
                if str(attr.Access)!='Hidden' and attr.Allowed==True:
                    if attr.DisplayType == 'Container' and attr.Name not in ('R2Q_CONFIGURATION', 'WriteInProduct','SM_Labor_Cont') and attr.Name not in skipcontainer:
                        if product_name in ["Series-C Control Group", "Series-C Remote Group"] and attr.Name not in required_containers:
                            continue
                        container_data, container_labels = extractProductContainer(attr.Name, product)
                        if container_data:
                            if attr.Name == 'R2Q_Project_Questions_Cont':
                                attributedict[product_name]['CE_Project_Questions_Cont'] = container_data
                                attributedictlable[product_name]['CE_Project_Questions_Cont'] = container_labels
                            elif attr.Name == 'R2Q CE_System_Cont':
                                attributedict[product_name]['CE_System_Cont'] = container_data
                                attributedictlable[product_name]['CE_System_Cont'] = container_labels
                            else:
                                attributedict[product_name][attr.Name] = container_data
                                attributedictlable[product_name][attr.Name] = container_labels
                    else:
                        if product_name in ["ControlEdge UOC System"] and attr.Name  in ControlEdgeUOCSystem:
                            continue
                        elif product_name in ["UOC Control Group"] and attr.Name  in UOCRemoteGroup:
                            continue
                        elif product_name in ["UOC Remote Group"] and attr.Name  in UOCControlGroup:
                            continue
                        '''if attr.DisplayType == 'Dropdown':
                            value = product.Attr(attr.Name).SelectDisplayValue() if product.Attr(attr.Name) else None
                        else:'''
                        value = product.Attr(attr.Name).GetValue() if product.Attr(attr.Name) else None
                        if value and attr.Name not in excluded_attributes:
                            attr_label = product.Attr(attr.Name).GetLabel()
                            key_name = attr_label if attr_label else ''
                            if attr.Name=='SerC_CG_R2Q_Percent_Installed_Spare':
                                clean_attr_name = 'SerC_CG_Percent_Installed_Spare'
                            elif attr.Name=='SerC_CG_R2Q_Power_System_Vendor':
                                clean_attr_name = 'SerC_CG_Power_System_Vendor'
                            elif attr.Name=='SerC_RG_Percentage_SSM_Cabinet (0-100%)':
                                clean_attr_name = 'SeriesC_RG_Percentage'
                            elif attr.Name=='SerC_CG_Percent_SpareSpace_Marshalling_Cabinet':
                                clean_attr_name = 'SerC_CG_Percentage_of_Spare_Space_required(0-100%)'
                            else:
                                clean_attr_name = re.sub(r'–', '', attr.Name)
                            attributedict[product_name][clean_attr_name] = value
                            attributedictlable[product_name][clean_attr_name] = key_name

try:
    r2qselectAttributedict = {}
    Select_Category=Product.Attr('R2Q Select Category').GetValue()
    r2qselectAttributedict_label = {}
    extractProductAttributes(r2qselectAttributedict,r2qselectAttributedict_label, Product)
    updated_json_data1 = replace_series_c_control_group(r2qselectAttributedict)
    updated_json_data2 = replace_series_c_control_group(r2qselectAttributedict_label)
    Quote.SetGlobal('r2qcompare', str(updated_json_data1))
    Quote.SetGlobal('r2qcompare_label', str(updated_json_data2))
    #Log.Info("GS_R2Q_Genratejsondictr2qcompare")
    Quote.Save(False)

except:
    Log.Info("GS_R2Q_Genratejsondicterror")