HCI_PHD_ExistingLicense = ['SC_Central_Managed_SQL','Trace_Software_Do_you_need_hardware','HCI_PHD_ExistingLicense_API_RDI','HCI_PHD_ExistingLicense_Archive_Extracto_ Tool','HCI_PHD_ExistingLicense_Availability_Redundancy','HCI_PHD_ExistingLicense_Base_System_Size','HCI_PHD_ExistingLicense_CEJ_Experion_Area_Wide','HCI_PHD_ExistingLicense_CEJ_OPC_Area_Wide','HCI_PHD_ExistingLicense_CEJ_Required','HCI_PHD_ExistingLicense_CEJ_TPN_Area_Wide','HCI_PHD_ExistingLicense_Clustering_Option','HCI_PHD_ExistingLicense_Label','HCI_PHD_ExistingLicense_LicenseTerm','HCI_PHD_ExistingLicense_Modbus_RDI','HCI_PHD_ExistingLicense_Non_Production_QA','HCI_PHD_ExistingLicense_Peer_Tags_Lincensed','HCI_PHD_ExistingLicense_RDI_File_Access','HCI_PHD_ExistingLicense_Classic_RDI_OPC','HCI_PHD_ExistingLicense_RDI_OPC_UA','HCI_PHD_ExistingLicense_RDI_Web_Client','HCI_PHD_ExistingLicense_Scout_Express','HCI_PHD_ExistingLicense_System_Monitoring_RDI','HCI_PHD_ExistingLicense_Tags_Base_Size','HCI_PHD_ExistingLicense_UpFront_Payment','ATTCON_03_open','ATTCON_03_close','HCI_PHD_ExistingLicense_MediaCopy','HCI_PHD_ExistingLicense_StandUserCals','HCI_PHD_ExistingLicense_StandDeviceCals','HCI_PHD_ExistingLicense_StandCores','HCI_PHD_ExistingLicense_SQLCluster','HCI_PHD_ExistingLicense_Comm_Parameter','HCI_PHD_ExistingLicense_ProductOptions','HCI_PHD_ExistingLicense_EnterpriseDataShadow','HCI_PHD_ExistingLicense_Convert_Clustering','HCI_PHD_Convert_Clustering','HCI_PHD_Standard_User_CALs','HCI_PHD_Standard Device','HCI_PHD_Standard_Cores','HCI_PHD_SQL_Cluster','HCI_PHD_Label_Commercial_Parameters','HCI_PHD_License_Term','HCI_PHD_Upfront_Payment']
HCI_AFM_ExistingLicense = ['HCI_AFM_ExistingLicense_Label','HCI_AFM_ExistingLicense_Tag_License_1000','HCI_AFM_ExistingLicense_Tag_License_10000','HCI_AFM_ExistingLicense_Tag_License_2000','HCI_AFM_ExistingLicense_Tag_License_5000','HCI_AFM_ExistingLicense_Tag_License_50000','HCI_AFM_ExistingLicense_Tag_License_Unlimited','ATTCON_05_open','ATTCON_05_close','HCI_AFM_ExistingLicense_Additional_Media','HCI_AFM_ExistingLicense_Lable_Product_Options']
HCI_Insight_ExistingLicense = ['HCI_Insight_ExistingLicense_250_User_Pack','HCI_Insight_ExistingLicense_Events_250_User_Pack','HCI_Insight_ExistingLicense_Events_Fifty_User_Pack','HCI_Insight_ExistingLicense_Events_Five_User_Pack','HCI_Insight_ExistingLicense_Events_Hundred_Pack','HCI_Insight_ExistingLicense_Events_Single_User','HCI_Insight_ExistingLicense_Events_Ten_User_Pack','HCI_Insight_ExistingLicense_Events_TwentyFive_Pack','HCI_Insight_ExistingLicense_Fifty_User_Pack','HCI_Insight_ExistingLicense_Hundred_User_Pack','HCI_Insight_ExistingLicense_Insight_Five_User_Pack','HCI_Insight_ExistingLicense_Label','HCI_Insight_ExistingLicense_License_Term','HCI_Insight_ExistingLicense_Single_User','HCI_Insight_ExistingLicense_Ten_User_Pack','HCI_Insight_ExistingLicense_TwentyFive_User_Pack','HCI_Insight_ExistingLicense_UpFront_Payment_Option','ATTCON_07_open','ATTCON_07_close','HCI_Ins_ExistingLicense_MediaCopy','HCI_Ins_ExistingLicense_StandUserCals','HCI_Ins_ExistingLicense_StandDeviceCals','HCI_Ins_ExistingLicense_StandCores','HCI_Ins_ExistingLicense_Comm_Parameter','HCI_Ins_ExistingLicense_ProductOptions','HCI_Ins_ExistingLicense_UserNoEvents','HCI_Ins_ExistingLicense_UserWithEvents','HCI_Ins_ExistingLicense_UserNoEvents_label','HCI_Ins_ExistingLicense_UserNoEvents_ProdOpt','HCI_Ins_ExistingLicense_UserWithEvents_label','HCI_Ins_ExistingLicense_UserWithEvents_ProdOpt']
Insight_SaaS = ['HCI_Insight_SaaS_CollectionRate','HCI_Insight_SaaS_Contract_length','HCI_Insight_SaaS_Data_Type','HCI_Insight_SaaS_EnterTagCount','HCI_Insight_SaaS_ExistingDataMigrate','HCI_Insight_SaaS_Label','HCI_Insight_SaaS_Label_DataManager','HCI_Insight_SaaS_Label_Migration','HCI_Insight_SaaS_Label_TimeSeriesData','HCI_Insight_SaaS_license','HCI_Insight_SaaS_SoftwareLicenseFee','Header_05_open','ATTCON_08_open','ATTCON_08_close','Header_05_close']
ThirdPartyHardware = ['HCI_Thrid_Party_Hardware','Header_06_open','ATTCON_09_open','ATTCON_09_close','Header_06_close']
#Log.Info('ready-->')
get_cf_isr2q=Quote.GetCustomField('IsR2QRequest').Content
isr2q=Quote.GetCustomField('R2QFlag').Content
Trace.Write('r2q cf-->'+str([get_cf_isr2q,Product.Name]))
Product.Attr('R2QRequest').AssignValue(get_cf_isr2q if get_cf_isr2q == "Yes" else '')
Trace.Write('r2q attr---'+str(Product.Attr('R2QRequest').GetValue()))
prd_name = Product.Name
if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
    for hide in HCI_PHD_ExistingLicense:
        Product.Attr(hide).Access = AttributeAccess.Hidden
    for hide in HCI_AFM_ExistingLicense:
        Product.Attr(hide).Access = AttributeAccess.Hidden
    for hide in HCI_Insight_ExistingLicense:
        Product.Attr(hide).Access = AttributeAccess.Hidden
    for hide in Insight_SaaS:
        Product.Attr(hide).Access = AttributeAccess.Hidden
    for hide in ThirdPartyHardware:
        Product.Attr(hide).Access = AttributeAccess.Hidden
if get_cf_isr2q == 'Yes' or isr2q =='Yes':
    if Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "New Implementation":
        Product.Attr('HCI_PHD_Scope').SelectDisplayValue('Upgrade')
        Product.Attr('HCI_PHD_Scope').SelectDisplayValue('New Implementation')
        Product.ApplyRules()
        Product.CalculateLineItemsInResponder
        Product.CalculateLineItemsInResponder='True'
    elif Product.Attr("HCI_PHD_Scope").SelectedValue.Display == "Upgrade":
        Product.Attr('HCI_PHD_Scope').SelectDisplayValue('New Implementation')
        Product.Attr('HCI_PHD_Scope').SelectDisplayValue('Upgrade')
        Product.ApplyRules()
        Product.CalculateLineItemsInResponder
        Product.CalculateLineItemsInResponder='True'
	PHD_Product = Product.Attr("HCI_PHD_Product").SelectedValue.Display
	if 1 == 1:
		Product.Attr('HCI_PHD_BGP_SUPPORT').AssignValue('1')
		Product.Attr("HCI_PHD_BGP_SUPPORT").Access = AttributeAccess.Hidden
		Product.DisallowAttrValues("HCI_PHD_Scope","Expansion")
		Product.Attr('HCI_PHD_RDI_Web_Client').SelectDisplayValue('None')
		Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_Standard_User_CALs").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_Standard_Device_CALs").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_Standard_Cores").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_Label_Commercial_Parameters").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_License_Term").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_UpFront_Payment_Option").Access = AttributeAccess.Hidden
		Product.Attr("HCI_Insight_UpFront_Payment_Option").Access = AttributeAccess.Hidden
		'''Product.Attr("HCI_Insight_Users_WithEvents").SelectDisplayValue('No')
		Trace.Write('aftr calc btn hide-->')
		Product.Attr("HCI_Insight_Events_Single_User").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Five_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Ten_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_TwentyFive_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Fifty_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_Hundred_User_Pack").Access = AttributeAccess.ReadOnly
		Product.Attr("HCI_Insight_Events_250_User_Pack").Access = AttributeAccess.ReadOnly
		#ScriptExecutor.ExecuteGlobal('R2Q_HCI_Attributepermission', {"prd_name":prd_name})
		#Product.Attr("HCI_PHD_ExistingLicense_Label").Access = AttributeAccess.Hidden
		#Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Hidden'''
		for hide in HCI_PHD_ExistingLicense:
			Product.Attr(hide).Access = AttributeAccess.Hidden
		for hide in HCI_AFM_ExistingLicense:
			Product.Attr(hide).Access = AttributeAccess.Hidden
		for hide in HCI_Insight_ExistingLicense:
			Product.Attr(hide).Access = AttributeAccess.Hidden
		for hide in Insight_SaaS:
			Product.Attr(hide).Access = AttributeAccess.Hidden
		for hide in ThirdPartyHardware:
			Product.Attr(hide).Access = AttributeAccess.Hidden