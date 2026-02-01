R2QRequest= Product.Attr('R2QRequest').GetValue()
prd_name = str(Param.prd_name) if hasattr(Param,'prd_name') else ''
Trace.Write('permsn--'+str([R2QRequest,prd_name,Product.Name]))
if prd_name == Product.Name:#R2QRequest == 'Yes':
	#General Questions
	Product.DisallowAttrValues('HCI_PHD_Scope', 'Expansion')
	Product.Attr('HCI_PHD_BGP_SUPPORT').AssignValue('')
	Product.Attr("HCI_PHD_BGP_SUPPORT").Access = AttributeAccess.Hidden
	Product.DisallowAttrValues('HCI_PHD_LicenseModel', 'Term', 'SaaS')
	Product.DisallowAttrValues('HCI_PHD_OrderType', 'Modify Existing Std Commercial License Options', 'Competitive Replacement')
	Product.Attr('SC_Central_Managed_SQL').SelectDisplayValue('No')
	Product.Attr("SC_Central_Managed_SQL").Access = AttributeAccess.Hidden
	Product.Attr('Trace_Software_Do_you_need_hardware').SelectDisplayValue('No')
	#Product.Attr("Trace_Software_Do_you_need_hardware").Access = AttributeAccess.Hidden
	Trace.Write('PRD--'+str(Product.Attr('HCI_PHD_Product').GetValue()))
	if Product.Attr('HCI_PHD_Product').GetValue() == "Process History Database (PHD)":
		hide_phd_att = ["Trace_Software_Additional_Media_Kits","HCI_PHD_Standard_User_CALs","HCI_PHD_Standard Device","HCI_PHD_Standard_Cores","HCI_PHD_SQL_Cluster","HCI_Insight_License_Term","HCI_PHD_UpFront_Payment","HCI_PHD_Tags_Base_Size","HCI_PHD_Peer_Tags_Lincensed","HCI_PHD_RDI_Web_Client","HCI_PHD_Scout_Express","HCI_PHD_Clustering_Option"]
		Product.Attr('Trace_Software_Additional_Media_Kits').AssignValue('0')
		Product.Attr('HCI_PHD_Standard_User_CALs').AssignValue('')
		Product.Attr('HCI_PHD_Standard Device').AssignValue('')
		Product.Attr('HCI_PHD_Standard_Cores').AssignValue('')
		Product.Attr('HCI_PHD_SQL_Cluster').SelectDisplayValue('No')

		#PENDING -- Base System Size: NEED TO IMPLEMENT  Hide this question and it should be calculated as mentioned in F27.(Total of Cells C79 to D79 from R2Q Labor UI should be rounded off to nearest drop down of R2Q SW & HW UI cell C27)

		Product.Attr('HCI_PHD_Tags_Base_Size').AssignValue('0')
		Product.Attr('HCI_PHD_Peer_Tags_Lincensed').AssignValue('0')
		Product.Attr('HCI_PHD_RDI_Web_Client').SelectDisplayValue('None')
		Product.Attr('HCI_PHD_Scout_Express').SelectDisplayValue('No')
		Product.Attr('HCI_PHD_Clustering_Option').SelectDisplayValue('No')
		for hid in hide_phd_att:
			Product.Attr(hid).Access = AttributeAccess.Hidden
	if Product.Attr('HCI_PHD_Product').GetValue() == "Advanced Formula Manager (AFM)":
		Product.Attr('HCI_AFM_Additional_Media').AssignValue('0')
		Product.Attr("HCI_AFM_Additional_Media").Access = AttributeAccess.Hidden

	if Product.Attr('HCI_PHD_Product').GetValue() == "Insight":
		hide_insight_att = ["HCI_Insight_Additional_Media_Copies","HCI_Insight_Standard_User_CALs","HCI_Insight_Standard_Device_CALs","HCI_Insight_Standard_Cores","HCI_Insight_License_Term","HCI_Insight_UpFront_Payment_Option"]
		Product.Attr('HCI_Insight_Additional_Media_Copies').AssignValue('0')
		Product.Attr('HCI_Insight_Standard_User_CALs').AssignValue('')
		Product.Attr('HCI_Insight_Standard_Device_CALs').AssignValue('')
		Product.Attr('HCI_Insight_Standard_Cores').AssignValue('')

		for hid in hide_insight_att:
			Product.Attr(hid).Access = AttributeAccess.Hidden

		'''if Product.Attr('HCI_PHD_CEJ_Required').GetValue() == 'Yes':
			Product.Attr('HCI_Insight_Users_NoEvents').SelectDisplayValue('No')
			Product.Attr('HCI_Insight_Users_WithEvents').SelectDisplayValue('Yes')
		if Product.Attr('HCI_PHD_CEJ_Required').GetValue() == 'No':
			Product.Attr('HCI_Insight_Users_NoEvents').SelectDisplayValue('Yes')
			Product.Attr('HCI_Insight_Users_WithEvents').SelectDisplayValue('No') '''