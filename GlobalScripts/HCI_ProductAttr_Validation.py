#Trace.Write("-->"+str(Product.Attr("HCI_PHD_Product").SelectedValue.Display))
GeneralQuestion = ['HCI_PHD_Product','HCI_PHD_Scope','HCI_PHD_LicenseModel','HCI_PHD_OrderType','SC_Central_Managed_SQL','Trace_Software_Do_you_need_hardware','Header_01_open','ATTCON_01_open','ATTCON_01_close','Header_01_close']

PHD = ['Trace_Software_Additional_Media_Kits','HCI_PHD_API_RDI','HCI_PHD_Archive_Extracto_ Tool','HCI_PHD_Availability_Redundancy','HCI_PHD_Base_System_Size','HCI_PHD_CEJ_Experion_Area_Wide','HCI_PHD_CEJ_OPC_Area_Wide','HCI_PHD_CEJ_Required','HCI_PHD_CEJ_TPN_Area_Wide','HCI_PHD_Clustering_Option','HCI_PHD_Label_Commercial_Parameters','HCI_PHD_Label_Product_Options','HCI_PHD_License_Term','HCI_PHD_Modbus_RDI','HCI_PHD_Non_Production_QA','HCI_PHD_Peer_Tags_Lincensed','HCI_PHD_RDI_File_Access','HCI_PHD_Classic_RDI_OPC','HCI_PHD_RDI_OPC_UA','HCI_PHD_RDI_Web_Client','HCI_PHD_Scout_Express','HCI_PHD_SQL_Cluster','HCI_PHD_Standard Device','HCI_PHD_Standard_Cores','HCI_PHD_System_Monitoring_RDI','HCI_PHD_Tags_Base_Size','HCI_PHD_UpFront_Payment','HCI_PHD_Standard_User_CALs','Header_02_open','ATTCON_02_open','ATTCON_02_close','Header_02_close','HCI_PHD_Label_EnterpriseDataShadow','HCI_PHD_NewLicense_Label']
HCI_PHD_ExistingLicense = ['HCI_PHD_ExistingLicense_API_RDI','HCI_PHD_ExistingLicense_Archive_Extracto_ Tool','HCI_PHD_ExistingLicense_Availability_Redundancy','HCI_PHD_ExistingLicense_Base_System_Size','HCI_PHD_ExistingLicense_CEJ_Experion_Area_Wide','HCI_PHD_ExistingLicense_CEJ_OPC_Area_Wide','HCI_PHD_ExistingLicense_CEJ_Required','HCI_PHD_ExistingLicense_CEJ_TPN_Area_Wide','HCI_PHD_ExistingLicense_Clustering_Option','HCI_PHD_ExistingLicense_Label','HCI_PHD_ExistingLicense_LicenseTerm','HCI_PHD_ExistingLicense_Modbus_RDI','HCI_PHD_ExistingLicense_Non_Production_QA','HCI_PHD_ExistingLicense_Peer_Tags_Lincensed','HCI_PHD_ExistingLicense_RDI_File_Access','HCI_PHD_ExistingLicense_Classic_RDI_OPC','HCI_PHD_ExistingLicense_RDI_OPC_UA','HCI_PHD_ExistingLicense_RDI_Web_Client','HCI_PHD_ExistingLicense_Scout_Express','HCI_PHD_ExistingLicense_System_Monitoring_RDI','HCI_PHD_ExistingLicense_Tags_Base_Size','HCI_PHD_ExistingLicense_UpFront_Payment','ATTCON_03_open','ATTCON_03_close','HCI_PHD_ExistingLicense_MediaCopy','HCI_PHD_ExistingLicense_StandUserCals','HCI_PHD_ExistingLicense_StandDeviceCals','HCI_PHD_ExistingLicense_StandCores','HCI_PHD_ExistingLicense_SQLCluster','HCI_PHD_ExistingLicense_Comm_Parameter','HCI_PHD_ExistingLicense_ProductOptions','HCI_PHD_ExistingLicense_EnterpriseDataShadow','HCI_PHD_ExistingLicense_Convert_Clustering','HCI_PHD_Convert_Clustering']

AFM = ['HCI_AFM_Additional_Media','HCI_AFM_Lable_Product_Options','HCI_AFM_Tag_License_1000','HCI_AFM_Tag_License_10000','HCI_AFM_Tag_License_2000','HCI_AFM_Tag_License_5000','HCI_AFM_Tag_License_50000','HCI_AFM_Tag_License_Unlimited','Header_03_open','ATTCON_04_open','ATTCON_04_close','Header_03_close','HCI_AFM_NewLicense_Label']
HCI_AFM_ExistingLicense = ['HCI_AFM_ExistingLicense_Label','HCI_AFM_ExistingLicense_Tag_License_1000','HCI_AFM_ExistingLicense_Tag_License_10000','HCI_AFM_ExistingLicense_Tag_License_2000','HCI_AFM_ExistingLicense_Tag_License_5000','HCI_AFM_ExistingLicense_Tag_License_50000','HCI_AFM_ExistingLicense_Tag_License_Unlimited','ATTCON_05_open','ATTCON_05_close','HCI_AFM_ExistingLicense_Additional_Media','HCI_AFM_ExistingLicense_Lable_Product_Options']

Insight = ['HCI_Insight_250_User_Pack','HCI_Insight_Additional_Media_Copies','HCI_Insight_Events_250_User_Pack','HCI_Insight_Events_Fifty_User_Pack','HCI_Insight_Events_Five_User_Pack','HCI_Insight_Events_Hundred_User_Pack','HCI_Insight_Events_Label_Product_Options','HCI_Insight_Events_Single_User','HCI_Insight_Events_Ten_User_Pack','HCI_Insight_Events_TwentyFive_User_Pack','HCI_Insight_Fifty_User_Pack','HCI_Insight_Five_User_Pack','HCI_Insight_Hundred_User_Pack','HCI_Insight_Label_Commercial_Parameters','HCI_Insight_Label_Product_Options','HCI_Insight_License_Term','HCI_Insight_Single_User','HCI_Insight_Standard_Cores','HCI_Insight_Standard_Device_CALs','HCI_Insight_Standard_User_CALs','HCI_Insight_Ten_User_Pack','HCI_Insight_TwentyFive_User_Pack','HCI_Insight_UpFront_Payment_Option','HCI_Insight_Users_NoEvents','HCI_Insight_Users_WithEvents','HCI_Insight_Users_Label_Product_Options','HCI_Insight_Users_With_Events_Label','HCI_Insight_Users_No_Events_Label','HCI_Insight_NewLicense_Label','Header_04_open','ATTCON_06_open','ATTCON_06_close','Header_04_close']
HCI_Insight_ExistingLicense = ['HCI_Insight_ExistingLicense_250_User_Pack','HCI_Insight_ExistingLicense_Events_250_User_Pack','HCI_Insight_ExistingLicense_Events_Fifty_User_Pack','HCI_Insight_ExistingLicense_Events_Five_User_Pack','HCI_Insight_ExistingLicense_Events_Hundred_Pack','HCI_Insight_ExistingLicense_Events_Single_User','HCI_Insight_ExistingLicense_Events_Ten_User_Pack','HCI_Insight_ExistingLicense_Events_TwentyFive_Pack','HCI_Insight_ExistingLicense_Fifty_User_Pack','HCI_Insight_ExistingLicense_Hundred_User_Pack','HCI_Insight_ExistingLicense_Insight_Five_User_Pack','HCI_Insight_ExistingLicense_Label','HCI_Insight_ExistingLicense_License_Term','HCI_Insight_ExistingLicense_Single_User','HCI_Insight_ExistingLicense_Ten_User_Pack','HCI_Insight_ExistingLicense_TwentyFive_User_Pack','HCI_Insight_ExistingLicense_UpFront_Payment_Option','ATTCON_07_open','ATTCON_07_close','HCI_Ins_ExistingLicense_MediaCopy','HCI_Ins_ExistingLicense_StandUserCals','HCI_Ins_ExistingLicense_StandDeviceCals','HCI_Ins_ExistingLicense_StandCores','HCI_Ins_ExistingLicense_Comm_Parameter','HCI_Ins_ExistingLicense_ProductOptions','HCI_Ins_ExistingLicense_UserNoEvents','HCI_Ins_ExistingLicense_UserWithEvents','HCI_Ins_ExistingLicense_UserNoEvents_label','HCI_Ins_ExistingLicense_UserNoEvents_ProdOpt','HCI_Ins_ExistingLicense_UserWithEvents_label','HCI_Ins_ExistingLicense_UserWithEvents_ProdOpt']

Insight_SaaS = ['HCI_Insight_SaaS_CollectionRate','HCI_Insight_SaaS_Contract_length','HCI_Insight_SaaS_Data_Type','HCI_Insight_SaaS_EnterTagCount','HCI_Insight_SaaS_ExistingDataMigrate','HCI_Insight_SaaS_Label','HCI_Insight_SaaS_Label_DataManager','HCI_Insight_SaaS_Label_Migration','HCI_Insight_SaaS_Label_TimeSeriesData','HCI_Insight_SaaS_license','HCI_Insight_SaaS_SoftwareLicenseFee','Header_05_open','ATTCON_08_open','ATTCON_08_close','Header_05_close']

ThirdPartyHardware = ['HCI_Thrid_Party_Hardware','Header_06_open','ATTCON_09_open','ATTCON_09_close','Header_06_close']

Hidden = ['HCI_AFM_ExistingLicense_Additional_Media','HCI_AFM_ExistingLicense_Lable_Product_Options']
#for hide in Hidden:
	#Product.Attr(hide).Access = AttributeAccess.Hidden
# General Questions - Include Hardware?
if Product.Attr("Trace_Software_Do_you_need_hardware").SelectedValue:
	hardware = Product.GetContainerByName("HCI_Thrid_Party_Hardware")
	if Product.Attr("Trace_Software_Do_you_need_hardware").SelectedValue.Display == "No":
		for hide in ThirdPartyHardware:
			Product.Attr(hide).Access = AttributeAccess.Hidden
		hardware.Rows.Clear()
	elif Product.Attr("Trace_Software_Do_you_need_hardware").SelectedValue.Display == "Yes":
		for show in ThirdPartyHardware:
			Product.Attr(show).Access = AttributeAccess.Editable
		ProductItems = ['PHD Collector Server','PHD Shadow Server','Insight Server','AFM Server','Total Number of Servers']
		if hardware.Rows.Count == 0:
			for i in ProductItems:
				hw = hardware.AddNewRow(False)
				hw["Third_Party_Hardware"] = str(i)
				hw["Qty"] = "0"
				#hw["Price"] = ""
				#hw["Cost"] = ""
				#hw["Extended_Description"] = ""

# General Questions - What is the Scope?
try:
    if Product.Attr("HCI_PHD_Scope").SelectedValue:
        # Existing License Details
        if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "New Implementation" or Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Upgrade":
            for hide in HCI_PHD_ExistingLicense:
                Product.Attr(hide).Access = AttributeAccess.Hidden
            for hide in HCI_AFM_ExistingLicense:
                Product.Attr(hide).Access = AttributeAccess.Hidden
            for hide in HCI_Insight_ExistingLicense:
                Product.Attr(hide).Access = AttributeAccess.Hidden
except Exception as e:
    Log.Info("Error in product Script - HCI_ProductAttr_Validation Attr: HCI_PHD_Scope"+str(e))
'''# General Questions - # License Deployment Model validation
if Product.Attr("HCI_PHD_LicenseModel").SelectedValue:
	if Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Term":
		Product.DisallowAttrValues("HCI_PHD_OrderType","Non-Support Upgrade")
	elif Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "SaaS":
		Product.DisallowAttrValues("HCI_PHD_OrderType","Competitive Replacement","Non-Support Upgrade","Maintenance Support Upgrade/Update (No Charge/ BGP Active)","Modify Existing Std Commercial License Options") '''

def phd():
	for show in PHD:
		Product.Attr(show).Access = AttributeAccess.Editable
	# Existing License Details
	if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		for show in HCI_PHD_ExistingLicense:
			Product.Attr(show).Access = AttributeAccess.Editable

	# Include SQL CALs? - validation
	if Product.Attr("SC_Central_Managed_SQL").SelectedValue:
		if Product.Attr("SC_Central_Managed_SQL").SelectedValue.Display == "No":
			Product.Attr("HCI_PHD_Standard_User_CALs").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_Standard Device").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_Standard_Cores").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_SQL_Cluster").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_StandUserCals").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_StandDeviceCals").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_StandCores").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_SQLCluster").Access = AttributeAccess.Hidden
		elif Product.Attr("SC_Central_Managed_SQL").SelectedValue.Display == "Yes":
			Product.Attr("HCI_PHD_Standard_User_CALs").Access = AttributeAccess.Editable
			Product.Attr("HCI_PHD_Standard Device").Access = AttributeAccess.Editable
			Product.Attr("HCI_PHD_Standard_Cores").Access = AttributeAccess.Editable
			Product.Attr("HCI_PHD_SQL_Cluster").Access = AttributeAccess.Editable
			#Product.Attr("HCI_PHD_ExistingLicense_StandUserCals").Access = AttributeAccess.Editable
			#Product.Attr("HCI_PHD_ExistingLicense_StandDeviceCals").Access = AttributeAccess.Editable
			#Product.Attr("HCI_PHD_ExistingLicense_StandCores").Access = AttributeAccess.Editable
			#Product.Attr("HCI_PHD_ExistingLicense_SQLCluster").Access = AttributeAccess.Editable

	# PHD - Commercial Parameters validation
	if Product.Attr("HCI_PHD_LicenseModel").SelectedValue:
		if Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Perpetual":
			Product.Attr("HCI_PHD_Label_Commercial_Parameters").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_License_Term").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_UpFront_Payment").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_Comm_Parameter").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_LicenseTerm").Access = AttributeAccess.Hidden
			Product.Attr("HCI_PHD_ExistingLicense_UpFront_Payment").Access = AttributeAccess.Hidden
		elif Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Term":
			if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "New Implementation" or Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Upgrade":
				Product.Attr("HCI_PHD_Label_Commercial_Parameters").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_License_Term").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_UpFront_Payment").Access = AttributeAccess.Editable
			if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
				Product.Attr("HCI_PHD_ExistingLicense_Comm_Parameter").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_ExistingLicense_LicenseTerm").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_ExistingLicense_UpFront_Payment").Access = AttributeAccess.Editable

	# Alarm & Events (Consolidated Event Journal - CEJ) required - validation
	if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "New Implementation" or Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Upgrade":
		if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue:
			if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue.Display == "No":
				Product.Attr("HCI_PHD_CEJ_TPN_Area_Wide").Access = AttributeAccess.ReadOnly
				Product.Attr("HCI_PHD_CEJ_Experion_Area_Wide").Access = AttributeAccess.ReadOnly
				Product.Attr("HCI_PHD_CEJ_OPC_Area_Wide").Access = AttributeAccess.ReadOnly
			if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue.Display == "Yes":
				Product.Attr("HCI_PHD_CEJ_TPN_Area_Wide").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_CEJ_Experion_Area_Wide").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_CEJ_OPC_Area_Wide").Access = AttributeAccess.Editable
	if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		if Product.Attr("HCI_PHD_ExistingLicense_CEJ_Required").SelectedValue:
			if Product.Attr("HCI_PHD_ExistingLicense_CEJ_Required").SelectedValue.Display == "No":
				Product.Attr("HCI_PHD_ExistingLicense_CEJ_TPN_Area_Wide").Access = AttributeAccess.ReadOnly
				Product.Attr("HCI_PHD_ExistingLicense_CEJ_Experion_Area_Wide").Access = AttributeAccess.ReadOnly
				Product.Attr("HCI_PHD_ExistingLicense_CEJ_OPC_Area_Wide").Access = AttributeAccess.ReadOnly
			if Product.Attr("HCI_PHD_ExistingLicense_CEJ_Required").SelectedValue.Display == "Yes":
				Product.Attr("HCI_PHD_ExistingLicense_CEJ_TPN_Area_Wide").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_ExistingLicense_CEJ_Experion_Area_Wide").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_ExistingLicense_CEJ_OPC_Area_Wide").Access = AttributeAccess.Editable
		if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue:
			if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue.Display == "No":
				Product.Attr("HCI_PHD_CEJ_TPN_Area_Wide").Access = AttributeAccess.ReadOnly
				Product.Attr("HCI_PHD_CEJ_Experion_Area_Wide").Access = AttributeAccess.ReadOnly
				Product.Attr("HCI_PHD_CEJ_OPC_Area_Wide").Access = AttributeAccess.ReadOnly
			if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue.Display == "Yes":
				Product.Attr("HCI_PHD_CEJ_TPN_Area_Wide").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_CEJ_Experion_Area_Wide").Access = AttributeAccess.Editable
				Product.Attr("HCI_PHD_CEJ_OPC_Area_Wide").Access = AttributeAccess.Editable
	# Non-Production QA - validation
	#Trace.Write("--->"+str(Product.Attr("HCI_PHD_OrderType").SelectedValue.Display))
	if Product.Attr("HCI_PHD_OrderType").SelectedValue and Product.Attr("HCI_PHD_OrderType").SelectedValue.Display == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
		Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Editable
	else:
		Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Hidden
		Product.Attr("HCI_PHD_ExistingLicense_Non_Production_QA").Access = AttributeAccess.Hidden

def afm():
	#Trace.Write(str(Product.Attr("HCI_PHD_Product").SelectedValue.Display)+"-00->"+str(dir(Product.Attr("Header_03_open").Access.Hidden)))
	for show in AFM:
		Product.Attr(show).Access = AttributeAccess.Editable

	# Existing License Details
	if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		#Product.Attr("HCI_AFM_ExistingLicense_Additional_Media").Access = AttributeAccess.Hidden
		#Product.Attr("HCI_AFM_ExistingLicense_Lable_Product_Options").Access = AttributeAccess.Hidden
		for show in HCI_AFM_ExistingLicense:
			Product.Attr(show).Access = AttributeAccess.Editable

def insight():
	for show in Insight_SaaS:
		Product.Attr(show).Access = AttributeAccess.Editable
	for show in Insight:
		Product.Attr(show).Access = AttributeAccess.Editable

	# Existing License Details
	if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		for show in HCI_Insight_ExistingLicense:
			Product.Attr(show).Access = AttributeAccess.Editable

	# Include SQL CALs? - validation
	if Product.Attr("SC_Central_Managed_SQL").SelectedValue:
		if Product.Attr("SC_Central_Managed_SQL").SelectedValue.Display == "No":
			Product.Attr("HCI_Insight_Standard_User_CALs").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Insight_Standard_Device_CALs").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Insight_Standard_Cores").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Ins_ExistingLicense_StandUserCals").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Ins_ExistingLicense_StandDeviceCals").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Ins_ExistingLicense_StandCores").Access = AttributeAccess.Hidden
		elif Product.Attr("SC_Central_Managed_SQL").SelectedValue.Display == "Yes":
			Product.Attr("HCI_Insight_Standard_User_CALs").Access = AttributeAccess.Editable
			Product.Attr("HCI_Insight_Standard_Device_CALs").Access = AttributeAccess.Editable
			Product.Attr("HCI_Insight_Standard_Cores").Access = AttributeAccess.Editable
			#Product.Attr("HCI_Ins_ExistingLicense_StandUserCals").Access = AttributeAccess.Editable
			#Product.Attr("HCI_Ins_ExistingLicense_StandDeviceCals").Access = AttributeAccess.Editable
			#Product.Attr("HCI_Ins_ExistingLicense_StandCores").Access = AttributeAccess.Editable

	# Insight - Commercial Parameters validation
	if Product.Attr("HCI_PHD_LicenseModel").SelectedValue:
		if Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Perpetual":
			Product.Attr("HCI_Insight_Label_Commercial_Parameters").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Insight_License_Term").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Insight_UpFront_Payment_Option").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Ins_ExistingLicense_Comm_Parameter").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Insight_ExistingLicense_License_Term").Access = AttributeAccess.Hidden
			Product.Attr("HCI_Insight_ExistingLicense_UpFront_Payment_Option").Access = AttributeAccess.Hidden
		elif Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Term":
			if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "New Implementation" or Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Upgrade":
				Product.Attr("HCI_Insight_Label_Commercial_Parameters").Access = AttributeAccess.Editable
				Product.Attr("HCI_Insight_License_Term").Access = AttributeAccess.Editable
				Product.Attr("HCI_Insight_UpFront_Payment_Option").Access = AttributeAccess.Editable
			if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
				Product.Attr("HCI_Insight_Label_Commercial_Parameters").Access = AttributeAccess.Editable
				Product.Attr("HCI_Insight_ExistingLicense_License_Term").Access = AttributeAccess.Editable
				Product.Attr("HCI_Insight_ExistingLicense_UpFront_Payment_Option").Access = AttributeAccess.Editable


	# Insight Users (No Events)- validation
	if Product.Attr("HCI_Insight_Users_NoEvents").SelectedValue.Display == "No":
		Product.Attr("HCI_Insight_Users_No_Events_Label").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Label_Product_Options").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Single_User").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Five_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Ten_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_TwentyFive_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Fifty_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Hundred_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_250_User_Pack").Access = AttributeAccess.ReadOnly
	elif Product.Attr("HCI_Insight_Users_NoEvents").SelectedValue.Display == "Yes":
		Product.Attr("HCI_Insight_Users_No_Events_Label").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Label_Product_Options").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Single_User").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Five_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Ten_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_TwentyFive_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Fifty_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Hundred_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_250_User_Pack").Access = AttributeAccess.Editable
	if Product.Attr("HCI_Ins_ExistingLicense_UserNoEvents").SelectedValue.Display == "No" and Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		Trace.Write("------ext----no---")
		#Product.Attr("HCI_Insight_Users_No_Events_Label").Access = AttributeAccess.Hidden
		#Product.Attr("HCI_Insight_Label_Product_Options").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Ins_ExistingLicense_UserNoEvents_label").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Ins_ExistingLicense_UserNoEvents_ProdOpt").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Single_User").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Insight_Five_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Ten_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_TwentyFive_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Fifty_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Hundred_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_250_User_Pack").Access = AttributeAccess.ReadOnly
	elif Product.Attr("HCI_Ins_ExistingLicense_UserNoEvents").SelectedValue.Display == "Yes" and Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		Trace.Write("------ext----yes---")
		#Product.Attr("HCI_Insight_Users_No_Events_Label").Access = AttributeAccess.Editable
		#Product.Attr("HCI_Insight_Label_Product_Options").Access = AttributeAccess.Editable
		Product.Attr("HCI_Ins_ExistingLicense_UserNoEvents_label").Access = AttributeAccess.Editable
		Product.Attr("HCI_Ins_ExistingLicense_UserNoEvents_ProdOpt").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Single_User").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Insight_Five_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Ten_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_TwentyFive_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Fifty_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Hundred_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_250_User_Pack").Access = AttributeAccess.Editable

	# Insight Users (With Events)- validation
	if Product.Attr("HCI_Insight_Users_WithEvents").SelectedValue.Display == "No":
		Product.Attr("HCI_Insight_Users_With_Events_Label").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Label_Product_Options").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Single_User").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Five_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Ten_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_TwentyFive_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Fifty_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Hundred_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_250_User_Pack").Access = AttributeAccess.ReadOnly
	elif Product.Attr("HCI_Insight_Users_WithEvents").SelectedValue.Display == "Yes":
		Product.Attr("HCI_Insight_Users_With_Events_Label").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_Label_Product_Options").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_Single_User").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_Five_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_Ten_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_TwentyFive_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_Fifty_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_Hundred_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_Events_250_User_Pack").Access = AttributeAccess.Editable
	if Product.Attr("HCI_Ins_ExistingLicense_UserWithEvents").SelectedValue.Display == "No" and Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		Product.Attr("HCI_Ins_ExistingLicense_UserWithEvents_label").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Ins_ExistingLicense_UserWithEvents_ProdOpt").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_Single_User").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_Five_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_Ten_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_TwentyFive_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_Fifty_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_Hundred_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_ExistingLicense_Events_250_User_Pack").Access = AttributeAccess.ReadOnly
	elif Product.Attr("HCI_Ins_ExistingLicense_UserWithEvents").SelectedValue.Display == "Yes" and Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Expansion":
		Product.Attr("HCI_Ins_ExistingLicense_UserWithEvents_label").Access = AttributeAccess.Editable
		Product.Attr("HCI_Ins_ExistingLicense_UserWithEvents_ProdOpt").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_Single_User").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_Five_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_Ten_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_TwentyFive_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_Fifty_User_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_Hundred_Pack").Access = AttributeAccess.Editable
		Product.Attr("HCI_Insight_ExistingLicense_Events_250_User_Pack").Access = AttributeAccess.Editable

	# License Deployment Model - validation
	if Product.Attr("HCI_PHD_LicenseModel").SelectedValue:
		if Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Perpetual" or Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "Term":
			for hide in Insight_SaaS:
				Product.Attr(hide).Access = AttributeAccess.Hidden
		elif Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display == "SaaS":
			#if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "New Implementation" or Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Upgrade":
			for hide in Insight:
				Product.Attr(hide).Access = AttributeAccess.Hidden
			for hide in HCI_Insight_ExistingLicense:
				Product.Attr(hide).Access = AttributeAccess.Hidden
			for show in Insight_SaaS:
				Product.Attr(show).Access = AttributeAccess.Editable

# Product validation
try:
    Product.Attr("Calculation_Button").Access = AttributeAccess.Editable
    if Product.Attr("HCI_PHD_Product").SelectedValue.Display == "Process History Database (PHD)":
        for hide in AFM:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_AFM_ExistingLicense:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in Insight:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in Insight_SaaS:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_Insight_ExistingLicense :
            Product.Attr(hide).Access = AttributeAccess.Hidden
        phd()
    elif Product.Attr("HCI_PHD_Product").SelectedValue.Display == "Advanced Formula Manager (AFM)":
        for hide in PHD:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_PHD_ExistingLicense:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in Insight:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in Insight_SaaS:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_Insight_ExistingLicense :
            Product.Attr(hide).Access = AttributeAccess.Hidden
        afm()
    elif Product.Attr("HCI_PHD_Product").SelectedValue.Display == "Insight":
        for hide in PHD:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_PHD_ExistingLicense:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in AFM:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_AFM_ExistingLicense:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        insight()
    elif Product.Attr("HCI_PHD_Product").SelectedValue.Display == "PHD & Insight":
        Product.Attr("HCI_PHD_ExistingLicense_MediaCopy").Access = AttributeAccess.Hidden
        for hide in AFM:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        for hide in HCI_AFM_ExistingLicense:
            Product.Attr(hide).Access = AttributeAccess.Hidden
        phd()
        insight()
    elif Product.Attr("HCI_PHD_Product").SelectedValue.Display == "PHD & Insight & AFM":
        phd()
        insight()
        afm()
    Product.Attr("HCI_PHD_LicenseModel").Access = AttributeAccess.ReadOnly #CXCPQ-109043
    #Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Hidden
except Exception as e:
    Log.Info("Error in product Script - HCI_ProductAttr_Validation Attr: Calculation_Button"+str(e))