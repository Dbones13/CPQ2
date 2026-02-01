if Quote.GetCustomField('EGAP_Proposal_Type').Content =="Budgetary":
	Product.DisallowAttr('FSC_to_SM_Has_the_System_Audit_been_performed')
	Product.DisallowAttr('ATT_FSC_to_SM_On_Site_Eng_hours')
	Product.DisallowAttr('ATT_FSC_to_SM_In_Office_Eng_hours')
	Product.ParseString('<*CTX( Container(FSC_to_SM_3rd_Party_Items).Column(FSC_to_SM_3rd_Party_Hardware_per_Audit_Report).SetPermission(Hidden) )*>')