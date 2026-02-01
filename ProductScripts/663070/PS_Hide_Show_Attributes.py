SNT = Product.Attr('Supervisory Network Type').GetValue()
ExpServer = Product.Attr('Experion Server Type').GetValue()
Redundancy = Product.Attr('Server Redundancy Requirement?').GetValue()

def update_attribute_access(attr_names, access_type):
	for attr_name in attr_names:
		Product.Attr(attr_name).Access = access_type

def update_attribute_permission(attr_names, allow=True):
	for attr_name in attr_names:
		if allow:
			Product.AllowAttr(attr_name)
			if Product.Attr(attr_name).GetValue() =='':
				Product.Attr(attr_name).AssignValue('0')
		else:
			Product.ResetAttr(attr_name)
			Product.DisallowAttr(attr_name)

if SNT == 'Ethernet' and ExpServer in ('Server', 'Server TPS') and Redundancy == 'Redundant':
	Product.Attr("Additional Backup Control Center Server Location").Access = AttributeAccess.Editable
else:
	Product.Attr('Additional Backup Control Center Server Location').AssignValue('0')
	Product.Attr("Additional Backup Control Center Server Location").Access = AttributeAccess.ReadOnly


selected_products = set(Product.Attr('CE_Selected_Products').GetValue().split('<br>'))
experion_section = ['Experion UOC Digital Points (0-61440)','Experion UOC Analog Points (0-61440)', 'Experion UOC Regulatory Compliance Points (0-61440)', 'Experion UOC Batch Points (0-61440)', 'Experion UOC Advanced Batch Points (0-61440)', 'Experion UOC Composite Device License (0-61440)', 'Experion UOC PROFINET Usage License (0-30)']
split_attr = ['Header_14_open', 'ATTCON_27_open', 'ATTCON_27_CLOSE', 'Header_14_CLOSE']
required_prds = {'Experion Enterprise System', 'ControlEdge UOC System'}
attr_access = AttributeAccess.Hidden
allow_access = False
if required_prds.issubset(selected_products):
	attr_access = AttributeAccess.Editable
	allow_access = True
	#assign_default_value(experion_section)
	Product.ApplyRules()

update_attribute_access(split_attr, attr_access)
update_attribute_permission(experion_section, allow_access)