import re
product_list = ['New / Expansion Project', 'C300 System', 'Series-C Control Group', 'Series-C Remote Group', 'System Group','Experion Enterprise System','Experion Enterprise Group','eServer System','eServer System Group','Field Device Manager','FDM System Group','3rd Party Devices/Systems Interface (SCADA)','CCR','ControlEdge UOC System','UOC Control Group','UOC Remote Group','Safety Manager','Safety Manager FGS','Safety Manager ESD','SM Control Group','SM Remote Group','HC900 System','HC900 Group','ControlEdge PLC System','CE PLC Control Group','CE PLC Remote Group','Terminal Manager','Industrial Security (Access Control)','Fire Detection & Alarm Engineering','Digital Video Manager','Tank Gauging Engineering','Operator Training','Small Volume Prover','Skid and Instruments']
def remove_extra_list_level(data, key):
    if key in data:
        value = data[key]
        while isinstance(value, list) and len(value) == 1 and isinstance(value[0], list):
            value = value[0]
        data[key] = value
        return value
    return None
def get_sort_index(item,Quotecontaxt):
    desired_order = eval(Quotecontaxt.GetGlobal('selectedProducts1'))
    child_products = item.get("Child_Products", {})
    product_name = child_products.get("product_name", "") if isinstance(child_products, dict) else ""
    return desired_order.index(product_name) if product_name in desired_order else len(desired_order)
def find_ce_system_cont(data):
    if isinstance(data, dict):
        if "CE_System_Cont" in data:
            return data["CE_System_Cont"]
        for value in data.values():
            result = find_ce_system_cont(value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_ce_system_cont(item)
            if result is not None:
                return result
    return None
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
def remove_system_group_cont(data):
    if isinstance(data, dict):
        data.pop("CE_SystemGroup_Cont", None)
        for key, value in data.items():
            data[key] = remove_system_group_cont(value)
    elif isinstance(data, list):
        return [remove_system_group_cont(item) for item in data]
    return data
def get_last_child_product(key):
    if ".Child_Products." in key:
        parts = key.split(".Child_Products.")
        last_part = parts[-1]
        child_product = last_part.split(".")[0]
        child_product = child_product.split("[")[0]
        return child_product
    return ""
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
    product_name = product.Name.replace("R2Q ", "")                                                 
    #product_name = product.Name
    containerList = []
    containerRows = product.GetContainerByName(attrName).Rows
    SMskip_conditions, CCRskip_conditions = {}, {}
    skip_conditions = {"C300_CG_Universal_IO_cont_1": {1},"C300_RG_Universal_IO_cont_1": {1}, "SerC_CG_Enhanced_Function_IO_Cont": {1}, "SerC_CG_Enhanced_Function_IO_Cont2": {2, 3, 4, 7, 8}, "SerC_RG_Enhanced_Function_IO_Cont": {1}, "SerC_RG_Enhanced_Function_IO_Cont2": {2, 3, 4, 7, 8},"C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1":{1,2,5,6},"C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont": {1},"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont":{1},"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1": {1,2,5,6}}
    if product.Name=="SM Control Group":
        univalue=product.Attr('Universal Marshalling Cabinet').GetValue()
        if univalue in ['Hardware Marshalling with P+F','Hardware_Marshalling_with_P+F']:
             SMskip_conditions={"SM_IO_Count_Digital_Input_Cont":{3,5},"SM_IO_Count_Digital_Output_Cont":{2,3,4,6,7},"SM_IO_Count_Analog_Input_Cont":{2,3,4}}
        elif univalue in ['Universal Marshalling','Universal_Marshalling']:
            SMskip_conditions={"SM_IO_Count_Digital_Input_Cont":{1,3},"SM_IO_Count_Digital_Output_Cont":{1,2,3,5,6},"SM_IO_Count_Analog_Input_Cont":{1,2,3,4}}
        else:
            SMskip_conditions={"SM_IO_Count_Digital_Input_Cont":{1,3},"SM_IO_Count_Digital_Output_Cont":{1,2,3,5,6},"SM_IO_Count_Analog_Input_Cont":{1,2,3}}
    if product.Name=="CCR":
        CCRskip_conditions={"Allen-Bradley/Siemens Interfaces":{1},"Modbus/OPC Interfaces":{4},"OPC Application Instances":{5,6,7}}
    if containerRows.Count > 0:
        for i, containerRow in enumerate(containerRows):
            if ((attrName in skip_conditions and i in skip_conditions[attrName]) or (attrName in SMskip_conditions and i in SMskip_conditions[attrName]) or (attrName in CCRskip_conditions and i in CCRskip_conditions[attrName])):
                continue
            if product_name =="SM Remote Group":
                enclosure_type = product.Attr('SM_RG_Enclosure_Type').GetValue()
                if enclosure_type =='Universal Safety Cab-1.3M':
                    containerRowDict = {col.Name: col.DisplayValue if  col.DisplayType=='DropDown' else containerRow[col.Name]  for col in containerRow.Columns if col.Name not in {'CNM_SFP_Type','External _24VDC_Terminal_Block','Power_Supply_Redundancy','Fiber_Optic_Extender','Field_Termination_Assembly_for_PDIO','Number_of_SFP_0-500','Cabinet_Material_Type_Ingress_Protection','Abu_Dhabi_Build_Loc','Ambient_Temperature_Range','Power_Supply_Type','Earth_Leakage_Detector_TELD','IO_Redundancy','Wire_Routing_Options','Temperature_Monitoring','Field_Termination_Assembly_for_PUIO','Number_of_Control_Network_Module_0-100','ATEX_Compliance','Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet','Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet','UI_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet'}}
                else:
                    containerRowDict = {col.Name: col.DisplayValue if  col.DisplayType=='DropDown' else containerRow[col.Name] for col in containerRow.Columns if col.Name not in {'IO_Type_with_hint', 'Deliverable_w_hint', 'IO_Type_Icon', 'Part_Summary', 'Displays/Shapes/Faceplates_hint'}}
            else:
                containerRowDict = {col.Name: col.DisplayValue if  col.DisplayType=='DropDown' else containerRow[col.Name] for col in containerRow.Columns if col.Name not in {'IO_Type_with_hint', 'Deliverable_w_hint', 'IO_Type_Icon', 'Part_Summary', 'Displays/Shapes/Faceplates_hint','Extended_Temperature','Cabinet_Access'}}
            if containerRow.Product and containerRow.Product.Name in product_list:
                containerRowDict["Child_Products"] = {}
                extractProductAttributes(containerRowDict["Child_Products"], containerRow.Product)
            if product_name =="SM Remote Group":
                enclosure_type = product.Attr('SM_RG_Enclosure_Type').GetValue()
                if enclosure_type not in ['Universal Safety Cab-1.3M']:
                    marCab = product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
                    if marCab  in ['Universal Marshalling','Universal_Marshalling']:
                        if ('Digital_Input_Type' in containerRowDict and containerRowDict['Digital_Input_Type'] in ('SDI(1) 24Vdc UIO  (0-5000)','SDI(1) 24Vdc DIO  (0-5000)')) or ('Digital_Output_Type' in containerRowDict and containerRowDict['Digital_Output_Type'] in ('SDO(1) 24Vdc 500mA UIO  (0-5000)','SDO(1) 24Vdc 500mA DIO  (0-5000)')) or ('Analog_Input_Type' in containerRowDict and containerRowDict['Analog_Input_Type'] in ('SAI(1)mA type Current  UIO  (0-5000)')) or ('Analog_Output_Type' in containerRowDict and containerRowDict['Analog_Output_Type'] in ('SAO(1)mA Type UIO   (0-5000)')) or ('Marshalling_Option' in containerRowDict) or ('Enclosure_Type' in containerRowDict) or('SM_Percent_Installed_Spare_IO' in containerRowDict ):
                            getadd=checkvalues(containerRowDict)
                            if getadd:
                                containerList.append(containerRowDict)
                        else:
                            continue
                    else:
                        if ('Digital_Input_Type' in containerRowDict and containerRowDict['Digital_Input_Type'] in ('SDI(1) 24Vdc UIO  (0-5000)','SDI(1)  24Vdc SIL2 P+F UIO  (0-5000)','SDI(1)  24Vdc SIL3 P+F UIO  (0-5000)','SDI(1) 24Vdc DIO  (0-5000)')) or ('Digital_Output_Type' in containerRowDict and containerRowDict['Digital_Output_Type'] in ('SDO(1) 24Vdc 500mA UIO  (0-5000)','SDO(1) 24Vdc SIL3 P+F UIO  (0-5000)','SDO(1) 24Vdc 500mA DIO  (0-5000)')) or ('Analog_Input_Type' in containerRowDict and containerRowDict['Analog_Input_Type'] in ('SAI(1)mA type Current  UIO  (0-5000)','SAI(1) mA Type Current P+F UIO  (0-5000)')) or ('Analog_Output_Type' in containerRowDict and containerRowDict['Analog_Output_Type'] in ('SAO(1)mA Type UIO   (0-5000)','SAO(1)mA Type P+F UIO  (0-5000)')) or ('Marshalling_Option' in containerRowDict) or ('Enclosure_Type' in containerRowDict) or('SM_Percent_Installed_Spare_IO' in containerRowDict ):
                            getadd=checkvalues(containerRowDict)
                            if getadd:
                                containerList.append(containerRowDict)
                        else:
                            continue
                else:
                    if attrName in ['SM_RG_Universal_Safety_Cabinet_1.3M_Cont','SM_SC_Universal_Safety_Cab_1_3M_Details_cont','SM_RG_ATEX Compliance_and_Enclosure_Type_Cont','SM_RG_IO_Count_Analog_Input_1.3_Cabinet_Cont','SM_RG_IO_Count_Digital_Input_1.3_Cabinet_Cont']:
                        getadd=checkvalues(containerRowDict)
                        if getadd:
                            containerList.append(containerRowDict)
            else:
                getadd=checkvalues(containerRowDict)
                if getadd:
                    containerList.append(containerRowDict)
    return containerList 
def extractProductAttributes(attributedict, product):
    product_name = product.Name.replace("R2Q ", "")
    #product_name = product.Name
    required_containers = { "C300_CG_Universal_IO_cont_1", "C300_CG_Universal_IO_cont_2", "SerC_CG_Enhanced_Function_IO_Cont", "SerC_CG_Enhanced_Function_IO_Cont2", "SerC_CG_FIM_FF_IO_Cont", "Series_C_Remote_Groups_Cont","C300_RG_Universal_IO_cont_1","C300_RG_Universal_IO_cont_2","SerC_RG_Enhanced_Function_IO_Cont","SerC_RG_Enhanced_Function_IO_Cont2","Number_of_Series_C_Control_Groups","C300_TurboM_IOM_CG_Cont","C300_CG_Universal_IO_Mark_1","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont", "C300_CG_Universal_IO_Mark_2","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1","C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont","C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1","C300_TurboM_IOM_RG_Cont","C300_UPC_Labor_IO_count_RG_2","C300_UPC_Labor_IO_count_RG_1"}
    if "product_name" not in attributedict:
        attributedict["product_name"] = product_name
    if product_name not in attributedict:
        attributedict[product_name] = {}
    for attr in product.Attributes:
        if attr.DisplayType == 'Container' and attr.Name not in ('R2Q_CONFIGURATION', 'WriteInProduct'):
            if product_name in ["Series-C Control Group", "Series-C Remote Group"] and attr.Name not in required_containers:
                continue
            container_data = extractProductContainer(attr.Name, product)
            if container_data: 
                if attr.Name == 'R2Q_Project_Questions_Cont':
                    attributedict[product_name]['CE_Project_Questions_Cont'] = container_data
                elif attr.Name == 'R2Q CE_System_Cont':
                    attributedict[product_name]['CE_System_Cont'] = container_data
                else:
                    attributedict[product_name][attr.Name] = container_data
        else:
            '''if attr.DisplayType == 'Dropdown':
                value = product.Attr(attr.Name).SelectDisplayValue()
            else:'''
            value = product.Attr(attr.Name).GetValue()
            R2q_attr_name = product.Attr(attr.Name).GetLabel()
            if value and attr.Name not in {'R2Q_CONFIGURATION', 'WriteInProduct'}:
                key_name = R2q_attr_name if R2q_attr_name else attr.Name
                clean_attr_name = re.sub(r'–', '', attr.Name)
                if product_name in ["Industrial Security (Access Control)","Tank Gauging Engineering","Fire Detection & Alarm Engineering","Digital Video Manager"]:
                    attributedict[product_name][clean_attr_name] = ''
                else:
                    attributedict[product_name][clean_attr_name] = value


Quote.SetGlobal('normalcompare', '')
selectAttributedict = {}
extractProductAttributes(selectAttributedict, Product)
updated_json_data1 = replace_series_c_control_group(selectAttributedict)
getsysupval=find_ce_system_cont(updated_json_data1)
getsysupval = sorted(getsysupval, key=lambda item: get_sort_index(item, Quote))
updated_data = remove_system_group_cont(updated_json_data1)
updated_data["New / Expansion Project"]["CE_System_Cont"] = []
updated_data["New / Expansion Project"]['CE_System_Cont'].append(getsysupval)
remove_extra_list_level(updated_json_data1["New / Expansion Project"], "CE_System_Cont")
Quote.SetGlobal('normalcompare', str(updated_data))