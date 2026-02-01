# ================================================================================================
# Component: Project -> System Group 1 -> PLC System -> PLC Control Group -> PLC Remote Group ....
# Author: Ashok Kandi
# Purpose: This is used to create a inherit the attributes from parent product.
# Date: 02/10/2022
# ================================================================================================
ce_proj_cont = Product.GetContainerByName('CE_Project_Questions_Cont')
if ce_proj_cont.Rows.Count == 1:
    ce_proj_site_volt = ce_proj_cont.Rows[0].GetColumnByName('CE_Site_Voltage').Value
    Product.Attr('CE_Site_Voltage').AssignValue(ce_proj_site_volt)
    ce_proj_site_frequency = ce_proj_cont.Rows[0].GetColumnByName('CE_Site_Frequency').Value
    Product.Attr('CE_Site_Frequency').SelectValue(ce_proj_site_frequency)

common_prj_cont = Product.GetContainerByName('New_exp_common_prj_input1')
if common_prj_cont.Rows.Count == 1:
    Crate_type = common_prj_cont.Rows[0].GetColumnByName('Crate Type').Value
    Product.Attr('Crate Type').SelectValue(Crate_type)
    Crate_design = common_prj_cont.Rows[0].GetColumnByName('Crate Design').Value
    Product.Attr('Crate Design').SelectValue(Crate_design)


labor_products=['One Wireless System', 'Fire and Gas Consultancy Service', 'Process Safety Workbench Engineering', 'Public Address General Alarm System', 'Fire Detection & Alarm Engineering', 'Industrial Security (Access Control)', 'Tank Gauging Engineering', 'Metering Skid Engineering', 'PRMS Skid Engineering', 'Gas MeterSuite Engineering - C300 Functions', 'MS Analyser System Engineering', 'Liquid MeterSuite Engineering - C300 Functions', 'MeterSuite Engineering - MSC Functions']
systemContainer = Product.GetContainerByName('CE_SystemGroup_Cont')
if systemContainer.Rows.Count > 0:
    for row in systemContainer.Rows:
        # To remove the selected product if the Scope is changed to HWSW -- Janhavi Tanna : CXCPQ-66019 :start
        if str(row["Scope"])!="HWSWLABOR":
            selected_products=str(row["Selected_Products"]).split("<br>")
            selected_products= "<br>".join([i for i in selected_products if i not in labor_products])
            row["Selected_Products"]=selected_products
            productContainer = row.Product.GetContainerByName('CE_System_Cont')
            for row1 in productContainer.Rows:
                Trace.Write(row1["Product Name"])
                if row1["Product Name"] not in selected_products and row1["Product Name"] in labor_products:
                    index = row1.RowIndex
                    productContainer.DeleteRow(index)
                    productContainer.Calculate()
        # To remove the selected product if the Scope is changed to HWSW -- Janhavi Tanna : CXCPQ-66019 :End
        Sys_Group_Name = row.Product.Attr('Sys_Group_Name').GetValue()
        if str(row["Child Product Name"]) != Sys_Group_Name:
            row.Product.Attr('Sys_Group_Name').AssignValue(str(row["Child Product Name"]))
            row.ApplyProductChanges()
        else:
            pass
            #row.Product.ApplyRules()

Labor_Details_Cont = Product.GetContainerByName('Labor_Details_New/Expansion_Cont')
if Labor_Details_Cont.Rows.Count == 1:

    Labor_Loop_Drawings = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Loop_Drawings').Value
    Labor_Unreleased_Product = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Unreleased_Product').Value
    Labor_Marshalling_Database = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Marshalling_Database').Value
    Labor_Percentage_FAT = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Percentage_FAT').Value
    Labor_Site_Activities = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Site_Activities').Value
    Labor_Operation_Manual_Scope = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Operation_Manual_Scope').Value
    Labor_Custom_Scope = Labor_Details_Cont.Rows[0].GetColumnByName('Labor_Custom_Scope').Value
    Product.Attr('Labor_Loop_Drawings').AssignValue(Labor_Loop_Drawings)
    Product.Attr('Labor_Unreleased_Product').AssignValue(Labor_Unreleased_Product)
    Product.Attr('Labor_Marshalling_Database').AssignValue(Labor_Marshalling_Database)
    Product.Attr('Labor_Percentage_FAT').AssignValue(Labor_Percentage_FAT)
    Product.Attr('Labor_Site_Activities').AssignValue(Labor_Site_Activities)
    Product.Attr('Labor_Operation_Manual_Scope').AssignValue(Labor_Operation_Manual_Scope)
    Product.Attr('Labor_Custom_Scope').AssignValue(Labor_Custom_Scope)

CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
#if CE_SystemGroup_Cont.Rows.Count == 1:
#    CE_Scope = CE_SystemGroup_Cont.Rows[0].GetColumnByName('CE_Scope_Choices').Value
#    Product.Attr('CE_Scope_Choices_Test').AssignValue(CE_Scope)
for i in CE_SystemGroup_Cont.Rows:
    CE_Scope = i.GetColumnByName('CE_Scope_Choices').Value
    Product.Attr('CE_Scope_Choices_Test').AssignValue(CE_Scope)

CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
if CE_SystemGroup_Cont.Rows.Count == 0:
    newRow = CE_SystemGroup_Cont.AddNewRow('System_Group_cpq', False)
    newRow.Product.Attr("CE_System_Index").AssignValue(str(newRow.RowIndex + 1))
    newRow.Product.Attr('CE_Scope_Choices').SelectDisplayValue('HW/SW + LABOR')
    newRow.Product.ApplyRules()
    newRow.ApplyProductChanges()
    newRow.Calculate()

# LabourHide_second_container and LabourHide product scripts
system = Product.GetContainerByName('CE_SystemGroup_Cont')
count = 0
count1 = 0
for i in system.Rows:
    if i['Scope'] == 'HWSWLABOR':
        count += 1
    
    if i['Scope'] == 'HWSWLABOR' and i['Selected_Products']:
        ab=i['Selected_Products']
        ab=ab.split("<br>")
        Trace.Write(str(ab))
        for j in ab:
            Trace.Write(j)
            if j=="Experion Enterprise System":
                Trace.Write('true')
                Trace.Write((i['Scope']))
                count1 += 1
if count > 0:
    TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Site_Survey_Required).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Unreleased_Product).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Loop_Drawings).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Marshalling_Database).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Percentage_FAT).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Site_Activities).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Operation_Manual_Scope).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Custom_Scope).SetPermission(Editable) )*>')
else:
    TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Site_Survey_Required).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Unreleased_Product).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Loop_Drawings).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Marshalling_Database).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Percentage_FAT).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Site_Activities).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Operation_Manual_Scope).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Custom_Scope).SetPermission(Hidden) )*>')
    
if (count1 > 0):
    Product.AllowAttr('Labor_details_newexapnsion_cont2')
else:
    Product.DisallowAttr('Labor_details_newexapnsion_cont2')

tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
#condition to run the below script only on Labor Deliverables tab
if 'PM Labor Deliverables' in tabs:
    import datetime
    #hide years which are less the current year or greater than current year + 4
    def hide_year(Product, current_year, attribute_name, expected_count, max_year ):
        years_list = Product.Attr(attribute_name).Values
        for year in years_list:
            if int(year.ValueCode) in range(current_year + 4, max_year):
                Product.DisallowAttrValues(attribute_name, year.ValueCode)
            elif int(year.ValueCode) < current_year:
                Product.DisallowAttrValues(attribute_name, year.ValueCode)
    attributes = ['Project_Execution_Year', 'PLE_Execution_Year']
    for attribute_name in attributes:
        allowed_count = 0
        expected_count = 4
        years_list = Product.Attr(attribute_name).Values
        for year in years_list:
            allowed_count = allowed_count + 1 if year.Allowed else allowed_count
        #condition to run the below script only when the year attribute has more than the expected (4) items
        if allowed_count > expected_count:
            current_year = datetime.datetime.now().year
            max_year = 2037
            hide_year(Product, current_year, attribute_name, expected_count, max_year)

center = Product.Attr('Staging_and_Integration_Center').GetValue()
unit  = SqlHelper.GetFirst('SELECT Floor_Area FROM STAGING_INTEGRATION_DATA WHERE  Integration_Center = ''+center+'' and  Particular = 'Floor Space'')
if center != 'Other' and unit != None:
    Trace.Write('In not others')
    values = Product.Attr('Staging_and_Integration_Floor_Area_Unit').Values
    for i in values:
        Trace.Write(i.ValueCode)
        if i.ValueCode == unit.Floor_Area:
            i.Allowed = True
        else:
            i.Allowed = False
if center == 'Other' or unit == None:
    if Product.Attr('Staging_and_Integration_Floor_Area_Unit').SelectedValue.ValueCode != 'Square Meter': #CXCPQ-103656
        Product.Attr('Staging_and_Integration_Floor_Area_Unit').SelectValue('Square Meter')
else:
    if Product.Attr('Staging_and_Integration_Floor_Area_Unit').SelectedValue.ValueCode != unit.Floor_Area: #CXCPQ-103656
        Product.Attr('Staging_and_Integration_Floor_Area_Unit').SelectValue(unit.Floor_Area)

cont = Product.GetContainerByName('CE_SystemGroup_Cont')
selectedProducts = set()
LaborScope='HWSWLABOR'
for row in filter(lambda x : x.IsSelected , cont.Rows):
    selectedProducts.update(row['Selected_Products'].split('<br>'))
    LaborScope=row['Scope']
    
if 'ControlEdge PLC System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','PLC_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','PLC_System')

if 'ControlEdge UOC System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','UOC_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','UOC_System')

if 'ControlEdge CN900 System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','CN900_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','CN900_System')

if 'PMD System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','PMD_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','PMD_System')

if 'ControlEdge RTU System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','RTU_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','RTU_System')

if 'Experion HS System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Experion_HS_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Experion_HS_System')

if 'Virtualization System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Virtualization_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Virtualization_System')

if '3rd Party Devices/Systems Interface (SCADA)' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','3rd_Party_Devices/Systems_Interface')
else:
    Product.AllowAttrValues('CE_Product_Choices','3rd_Party_Devices/Systems_Interface')
if 'Experion MX System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Experion_MX_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Experion_MX_System')
if 'MXProLine System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','MX_Proline_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','MX_Proline_System')
if 'Simulation System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Simulation_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Simulation_System')
if 'eServer System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','eServer_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','eServer_System')
if 'Electrical Substation Data Collector' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Electrical_Substation_Data_Collector')
else:
    Product.AllowAttrValues('CE_Product_Choices','Electrical_Substation_Data_Collector')
# Experion Enterprise System
if 'Experion Enterprise System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Experion_Enterprise_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Experion_Enterprise_System')
# HC900 System
if 'HC900 System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','HC900_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','HC900_System')
# PlantCruise System
if 'PlantCruise System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','PlantCruise_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','PlantCruise_System')
# Generic System Alias products -Start
if 'Experion LX Generic' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Experion_LX_Generic')
else:
    Product.AllowAttrValues('CE_Product_Choices','Experion_LX_Generic')
if 'MasterLogic-50 Generic' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','MasterLogic-50_Generic')
else:
    Product.AllowAttrValues('CE_Product_Choices','MasterLogic-50_Generic')
if 'MasterLogic-200 Generic' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','MasterLogic-200_Generic')
else:
    Product.AllowAttrValues('CE_Product_Choices','MasterLogic-200_Generic')
# Generic System Alias products -End
# Terminal Manager
if 'Terminal Manager' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Terminal_Manager')
else:
    Product.AllowAttrValues('CE_Product_Choices','Terminal_Manager')

# ControlEdge PCD System
if 'ControlEdge PCD System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','ControlEdge_PCD_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','ControlEdge_PCD_System')
# Variable Frequency Drive System
if 'Variable Frequency Drive System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Variable_Frequency_Drive_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Variable_Frequency_Drive_System')
# Measurement IQ System
if 'Measurement IQ System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Measurement_IQ_System')
else:
    new_exp = TagParserProduct.ParseString("<*CTX ( Container(CE_SystemGroup_Cont).SelectedRow.Column(New_Expansion).Get )*>")
    if new_exp == "Expansion":
        Product.DisallowAttrValues('CE_Product_Choices', 'Measurement_IQ_System')
    else:
        Product.AllowAttrValues('CE_Product_Choices', 'Measurement_IQ_System')
#C300 System
if 'C300 System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','C300_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','C300_System')
#FDM System
if 'Field Device Manager' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','FDM_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','FDM_System')

#Digital Video Manager
if 'Digital Video Manager' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','Digital_Video_Manager')
else:
    Product.AllowAttrValues('CE_Product_Choices','Digital_Video_Manager')
#ARO & RESS System
if 'ARO, RESS & ERG System' in selectedProducts:
    Product.DisallowAttrValues('CE_Product_Choices','ARO_&_RESS_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','ARO_&_RESS_System')
#One Wireless System
if 'One Wireless System' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','One_Wireless_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','One_Wireless_System')
#Tank Gauging Engineering
if 'Tank Gauging Engineering' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Tank_Gauging_Engineering')
else:
    Product.AllowAttrValues('CE_Product_Choices','Tank_Gauging_Engineering')
    
#Fire and Gas Consultancy Service
if 'Fire and Gas Consultancy Service' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Fire_and_Gas_Consultancy_Service')
else:
    Product.AllowAttrValues('CE_Product_Choices','Fire_and_Gas_Consultancy_Service')

#Process Safety Workbench Engineering
if 'Process Safety Workbench Engineering' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Process_Safety_Workbench_Engineering')
else:
    Product.AllowAttrValues('CE_Product_Choices','Process_Safety_Workbench_Engineering')

#Public Address General Alarm System
if 'Public Address General Alarm System' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Public_Address_General_Alarm_System')
else:
    Product.AllowAttrValues('CE_Product_Choices','Public_Address_General_Alarm_System')

#Metering Skid Engineering
if 'Metering Skid Engineering' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Metering_Skid_Engineering')
else:
    Product.AllowAttrValues('CE_Product_Choices','Metering_Skid_Engineering')

#PRMS Skid Engineering
if 'PRMS Skid Engineering' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','PRMS_Skid_Engineering')
else:
    Product.AllowAttrValues('CE_Product_Choices','PRMS_Skid_Engineering')

    #MeterSuite Engineering - MSC Functions
if 'MeterSuite Engineering - MSC Functions' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','MeterSuite_Engineering_-_MSC_Functions')
else:
    Product.AllowAttrValues('CE_Product_Choices','MeterSuite_Engineering_-_MSC_Functions')

#Fire Detection & Alarm Engineering
if 'Fire Detection & Alarm Engineering' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Fire_Detection_&_Alarm_Engineering')
else:
    Product.AllowAttrValues('CE_Product_Choices','Fire_Detection_&_Alarm_Engineering')
#Gas MeterSuite Engineering - C300 Functions
if 'Gas MeterSuite Engineering - C300 Functions' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Gas_MeterSuite_Engineering_C300_Functions')
else:
    Product.AllowAttrValues('CE_Product_Choices','Gas_MeterSuite_Engineering_C300_Functions')

# Liquid MeterSuite Engineering - C300 Functions
if 'Liquid MeterSuite Engineering - C300 Functions' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Liquid_MeterSuite_Engineering_C300_Functions')
else:
    Product.AllowAttrValues('CE_Product_Choices','Liquid_MeterSuite_Engineering_C300_Functions')
#MS Analyser System Engineering
if 'MS Analyser System Engineering' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','MS_Analyser_System_Engineering')
else:
    Product.AllowAttrValues('CE_Product_Choices','MS_Analyser_System_Engineering')

#Industrial Security (Access Control)
if 'Industrial Security (Access Control)' in selectedProducts or LaborScope!='HWSWLABOR':
    Product.DisallowAttrValues('CE_Product_Choices','Industrial_Security_(Access_Control)')
else:
    Product.AllowAttrValues('CE_Product_Choices','Industrial_Security_(Access_Control)')

# Safety Manager Systems
sys_dict = {'Safety Manager ESD': 'Safety_Manager_ESD', 'Safety Manager FGS': 'Safety_Manager_FGS', 'Safety Manager BMS': 'Safety_Manager_BMS', 'Safety Manager HIPPS': 'Safety_Manager_HIPPS'}
for sys_name in sys_dict.keys():
    sys_id = sys_dict[sys_name]
    if sys_name in selectedProducts:
        Product.DisallowAttrValues('CE_Product_Choices', sys_id)
    else:
        Product.AllowAttrValues('CE_Product_Choices', sys_id)

isValid = True
selectedProducts = [val for val in Product.Attr('CE_Product_Choices').SelectedValues]
if len(selectedProducts) == 0:
    isValid = False

if cont.HasSelectedRow and isValid:
    Product.AllowAttr('CE_Apply_Product_Selection')
else:
    Product.DisallowAttr('CE_Apply_Product_Selection')

#Display products based on the selected category
def getDisallowProductList(allowedProducts, selectedProducts, productChoices):
    disallow_products = []
    for prd in allowedProducts:
        if prd in selectedProducts:
            disallow_products.append(prd)
    for pc in productChoices:
        if not pc in allowedProducts:
            disallow_products.append(pc)
    return disallow_products

pc = Product.Attr('CE_Product_Choices')
productChoices = []
for v in pc.Values:
    productChoices.append(v.ValueCode)

allowedProducts = ''
proj_category = Product.Attr('New_Expansion_Project_Category').GetValue()
if proj_category == 'ICS System':
    allowedProducts = ['ARO_&_RESS_System', 'C300_System', 'Digital_Video_Manager', 'Electrical_Substation_Data_Collector', 'eServer_System', 'Experion_Enterprise_System', 'FDM_System', 'PLC_System', 'RTU_System', 'Safety_Manager_BMS', 'Safety_Manager_ESD', 'Safety_Manager_FGS', 'Safety_Manager_HIPPS', 'Simulation_System', 'UOC_System', 'CN900_System', 'Virtualization_System', 'One_Wireless_System','Fire_and_Gas_Consultancy_Service','Process_Safety_Workbench_Engineering','3rd_Party_Devices/Systems_Interface','Public_Address_General_Alarm_System','Fire_Detection_&_Alarm_Engineering','Industrial_Security_(Access_Control)']
elif proj_category == 'Modular System':
    allowedProducts =  ['Experion_HS_System', 'Experion_LX_Generic', 'HC900_System', 'MasterLogic-200_Generic', 'MasterLogic-50_Generic', 'Measurement_IQ_System', 'PlantCruise_System', 'PLC_System', 'RTU_System', 'Terminal_Manager', 'Variable_Frequency_Drive_System', 'Tank_Gauging_Engineering','Metering_Skid_Engineering', 'PRMS_Skid_Engineering','Gas_MeterSuite_Engineering_C300_Functions', 'MS_Analyser_System_Engineering','Liquid_MeterSuite_Engineering_C300_Functions','MeterSuite_Engineering_-_MSC_Functions']
elif proj_category == 'Sheet Mfg System':
    allowedProducts = ['ControlEdge_PCD_System', 'Experion_Enterprise_System', 'Experion_MX_System', 'MX_Proline_System', 'PMD_System', 'UOC_System', 'Virtualization_System']
if allowedProducts != '':
    disallow_product_list = getDisallowProductList(allowedProducts, selectedProducts, productChoices)
    if len(disallow_product_list) > 0:
        for lst in disallow_product_list:
            Product.DisallowAttrValues('CE_Product_Choices', lst)

# To inherit the ges location from PRJT to ControlEdge PLC System
container = Product.GetContainerByName('CE_SystemGroup_Cont') #new and exp
location_cont=Product.GetContainerByName("CE_Project_Questions_Cont")
if (location_cont and location_cont.Rows.Count > 0):
	if location_cont.Rows[0]["GES_Location"]:
		location = location_cont.Rows[0]["GES_Location"]
locationdict = {'EG':'GES Egypt', 'UZ':'GES Uzbekistan', 'RO':'GES Romania', 'CN':'GES China', 'IN':'GES India', 'None':'None'}
if container.Rows.Count > 0:
	for row in container.Rows:
		if 'ControlEdge PLC System' in row['Selected_Products']:
			system_cont = row.Product.GetContainerByName('CE_System_Cont')
			for rows in system_cont.Rows:
				if rows['Product Name'] ==  'ControlEdge PLC System':
					labour_cont = rows.Product.GetContainerByName('PLC_Labour_Details') #PLC Labour cont
					if location:
						loc = locationdict[location]
						rows.Product.Attr('PLC_Ges_Location').SelectDisplayValue(loc)
						labour_cont.Rows[0].GetColumnByName("PLC_Ges_Location").SetAttributeValue(loc)
						Trace.Write(labour_cont.Rows[0].GetColumnByName("PLC_Ges_Location").Value)
Io_dict = {'C300 System':'Series_C_Control_Groups_Cont','Safety Manager ESD':'SM_ControlGroup_Cont','Safety Manager FGS':'SM_ControlGroup_Cont','Safety Manager BMS':'SM_ControlGroup_Cont','Safety Manager HIPPS':'SM_ControlGroup_Cont'}
new_expansion = Product.GetContainerByName('CE_SystemGroup_Cont').Rows
analog_IO = 0
digital_IO = 0
for prd in new_expansion:
		system_container = prd.Product.GetContainerByName('CE_System_Cont').Rows
		for ind_prd in system_container:
			if ind_prd.Product.Name not in ('ControlEdge RTU System','ControlEdge PLC System','ControlEdge UOC System') and Io_dict.get(ind_prd.Product.Name,None):
				Trace.Write(Io_dict[ind_prd.Product.Name])
				Trace.Write('injn')
				for con_grp in ind_prd.Product.GetContainerByName(Io_dict[ind_prd.Product.Name]).Rows:
					Trace.Write(ind_prd.Product.Name)
					if ind_prd.Product.Name == 'C300 System':
						analog_IO += int(con_grp['AI'])+int(con_grp['AO'])
						digital_IO += int(con_grp['DI'])+int(con_grp['DO'])
					elif ind_prd.Product.Name in('Safety Manager ESD','Safety Manager FGS','Safety Manager BMS','Safety Manager HIPPS'):
						analog_IO += int(con_grp['Labor_parameter_ai'])+int(con_grp['Labor_parameter_ao'])
						digital_IO += int(con_grp['Labor_parameter_di'])+int(con_grp['Labor_parameter_do'])
			elif ind_prd.Product.Name == 'ControlEdge RTU System':#ok
				import GS_RTU_Labor_Parameters as RTU
				Ioval = RTU.AttrStorage(ind_prd.Product)
				analog_IO += int(Ioval.AI) + int(Ioval.AO)
				digital_IO += int(Ioval.DI) + int(Ioval.DO)
			elif ind_prd.Product.Name == 'ControlEdge PLC System': #ok
				import GS_PLC_Labor_Parameters as PLC
				Ioval = PLC.AttrStorage(ind_prd.Product)
				analog_IO += int(Ioval.AI) + int(Ioval.AO)
				digital_IO += int(Ioval.DI) + int(Ioval.DO)
			elif ind_prd.Product.Name == 'ControlEdge UOC System': #ok
				import GS_UOC_Labor_Parameters as UOC
				Ioval = UOC.AttrStorage(ind_prd.Product)
				analog_IO += int(Ioval.AI) + int(Ioval.AO)
				digital_IO += int(Ioval.DI) + int(Ioval.DO)
Trace.Write('analog_IO:'+str(analog_IO))
Trace.Write('digital_IO:'+str(digital_IO))
IO_cont = Product.GetContainerByName('Total_Analog_Digital_IO')
Trace.Write('all out')
if IO_cont and IO_cont.Rows.Count > 0:
    IO_cont.Rows[0]['Analog_IO'] = str(analog_IO)
    IO_cont.Rows[0]['Digital_IO'] = str(digital_IO)
else:
	new_row = IO_cont.AddNewRow(False)
	new_row['Analog_IO'] = str(analog_IO)
	new_row['Digital_IO'] = str(digital_IO)