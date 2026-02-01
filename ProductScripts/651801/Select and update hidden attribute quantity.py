def get_attr_value(attr_name, product):
	value = product.Attr(attr_name).GetValue()
	return int(value) if value else 0

def set_attr_quantity(attr_name, value_code, quantity, product):
	attr = product.Attr(attr_name)
	attr.SelectValues(value_code)
	for selected_value in attr.SelectedValues:
		if selected_value.ValueCode == value_code:
			selected_value.Quantity = quantity

def reset_attr(attr_name, product):
	product.ResetAttr(attr_name)

def deselect_attr(attr_name, value_code, product):
	product.DeselectAttrValues(attr_name, value_code)

if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
	number_of_smx_system_for_rt = get_attr_value('Number of SMX System RT', Product)
	number_of_smx_system_for_st = get_attr_value('Number of SMX System ST', Product)
	number_of_smx_system_for_mi = get_attr_value('Number of System MI', Product)
	number_of_years_of_contract = get_attr_value('Number of Years of Contract', Product)
	usb_key_for_st = get_attr_value('USB Key ST Only', Product)

	number_of_years_of_contract_value = (number_of_smx_system_for_st + number_of_smx_system_for_rt + number_of_smx_system_for_mi)

	if number_of_smx_system_for_rt > 0:
		set_attr_quantity('HW_CSS_BOM_SMX_BaseLicenses_RT', 'CS-SMXRTG', number_of_smx_system_for_rt, Product)
	else:
		reset_attr('HW_CSS_BOM_SMX_BaseLicenses_RT', Product)

	if number_of_years_of_contract_value > 0:
		set_attr_quantity('HW_CSS_BOM_SMXMicro_BaseLicenses_Micro', 'CS-SMXIMG-ACT', number_of_years_of_contract_value, Product)
	else:
		deselect_attr('HW_CSS_BOM_SMXMicro_BaseLicenses_Micro', 'CS-SMXIMG-ACT', Product)

	if number_of_smx_system_for_st > 0:
		set_attr_quantity('HW_CSS_BOM_SMXST_BaseLicenses_ST', 'CS-SMXSTG', number_of_smx_system_for_st, Product)
	else:
		deselect_attr('HW_CSS_BOM_SMXST_BaseLicenses_ST', 'CS-SMXSTG', Product)

	if number_of_years_of_contract > 0:
		set_attr_quantity('HW_CSS_BOM_SMX_IndividualLicenses_RT', 'CS-SMXGARD', number_of_years_of_contract, Product)
	else:
		reset_attr('HW_CSS_BOM_SMX_IndividualLicenses_RT', Product)

	if number_of_years_of_contract > 0:
		set_attr_quantity('HW_CSS_BOM_SMX_IndividualLicenses_Maint_RT', 'CS-SMXHWMAINT', number_of_years_of_contract, Product)
	else:
		reset_attr('HW_CSS_BOM_SMX_IndividualLicenses_Maint_RT', Product)

	if usb_key_for_st > 0:
		set_attr_quantity('HW_CSS_BOM_SMXST_USBKey', 'CS-SMXUSBKEY-1XU', usb_key_for_st, Product)
	else:
		reset_attr('HW_CSS_BOM_SMXST_USBKey', Product)