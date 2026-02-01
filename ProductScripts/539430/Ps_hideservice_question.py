def ReadOnly(attrname):
    Product.Attr(attrname).Access = AttributeAccess.ReadOnly
if Quote.GetCustomField('EGAP_Proposal_Type').Content =="Budgetary":
	Product.DisallowAttr('FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed')
	Product.DisallowAttr('ATT_FSC_to_SM_IO_In_Office_Eng_hours')
	Product.DisallowAttr('ATT_FSC_to_SM_IO_On_Site_Eng_hours')
	Product.ParseString('<*CTX( Container(FSC_to_SM_IO_Migration_General_Information2).Column(FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report).SetPermission(Hidden) )*>')
    
ReadOnly('FSC_SM_IO_Total_ Calculated_SIC_cables')