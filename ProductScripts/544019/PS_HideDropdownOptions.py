def attrAccess(ke_AttrList):
	for attr in ke_AttrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

ke_Prd = Product.Attr('K&E Selected Model').GetValue()
if ke_Prd == '':
	ke_AttrList = ['Cancel Package','KE_Part_Number','KE_Part_Name','KE_Software_Release','KE_SESP','KE_Remote_Peripheral_Solution_Type','KE_Quad_Display','KE_Node_Type','KE_Key_Board_Type','KE_ISA_Adapter_Required','KE_Hardware_Selection','KE_Experion_Base_Media_Delivery','KE_EBR_Required','KE_EBR_Release','KE_EBR_Media_Delivery','KE_Does_installed_APP','KE_Controller Experion peer to peer connectivity','KE_Control_Solver_License','KE_COA_License_Type','KE_C300_Horizontal_Mounting_Kit','KE_Additional_Hard_Disk','KE_Controller P2P Connectivity Licenses']
	attrAccess(ke_AttrList)