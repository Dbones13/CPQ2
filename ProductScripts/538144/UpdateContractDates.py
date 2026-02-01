if Product.Name == 'Enabled Services':
	Product.Attr('SC_HWOS_Service_Product').AssignValue('Enabled Services Model')
	Product.Attr('CurrentSupportContract_EnabledService').AssignValue('None')
	if Quote.GetCustomField('EGAP_Contract_Start_Date').Content != "" and Quote.GetCustomField('EGAP_Contract_End_Date').Content != "":
		egap_c_start_date_str = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
		egap_c_end_date_str = Quote.GetCustomField('EGAP_Contract_End_Date').Content
		egap_c_start_date = UserPersonalizationHelper.CovertToDate(egap_c_start_date_str)
		egap_c_end_date = UserPersonalizationHelper.CovertToDate(egap_c_end_date_str)
		Product.Attr('PreviousQuoteCStartDate_EnabledServices').AssignValue(egap_c_start_date_str)
		Product.Attr('PreviousQuoteCEndDate_EnabledServices').AssignValue(egap_c_end_date_str)
		prev_c_start_date = Product.Attr('PreviousQuoteCStartDate_EnabledServices')
		prev_c_end_date = Product.Attr('PreviousQuoteCEndDate_EnabledServices')
		prd_c_start_date = Product.Attr('ContractStartDate_EnabledService')
		prd_c_end_date = Product.Attr('ContractEndDate_EnabledService')

		curr_c_start_date = egap_c_start_date
		curr_c_end_date = egap_c_end_date

		if prev_c_start_date.GetValue():
			if str(UserPersonalizationHelper.ToUserFormat(DateTime.Parse(prev_c_start_date.GetValue()))) != str(UserPersonalizationHelper.ToUserFormat(DateTime.Parse(str(curr_c_start_date)))):
				prd_c_start_date.AssignValue(egap_c_start_date_str)
				prev_c_start_date.AssignValue(egap_c_start_date_str)
			else:
				if prd_c_start_date.GetValue() == '':
					prd_c_start_date.AssignValue(egap_c_start_date_str)
				else:
					pass

		if prev_c_end_date.GetValue():
			if str(UserPersonalizationHelper.ToUserFormat(DateTime.Parse(prev_c_end_date.GetValue()))) != str(UserPersonalizationHelper.ToUserFormat(DateTime.Parse(str(curr_c_end_date)))):
				prd_c_end_date.AssignValue(egap_c_end_date_str)
				prev_c_end_date.AssignValue(egap_c_end_date_str)
			else:
				if prd_c_end_date.GetValue() == '':
					prd_c_end_date.AssignValue(egap_c_end_date_str)
		"""flag = Product.Attr('ContractDatesFlag_EnabledServices').GetValue()
		if flag == True or flag == 'True':
			Product.Attr('ContractStartDate_EnabledService').AssignValue(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)
			Product.Attr('ContractEndDate_EnabledService').AssignValue(Quote.GetCustomField('EGAP_Contract_End_Date').Content)
			duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content.split(' ')[0]
			Product.Attr('DurationOfPlan_enabledServices').AssignValue(str(duration))
			Product.Attr('ContractDatesFlag_EnabledServices').AssignValue('False')"""
#################
if Quote:
	Product.Attr('quoteCurrency_hwos').AssignValue(Quote.SelectedMarket.CurrencyCode)
else:
	Product.Attr('quoteCurrency_hwos').AssignValue('USD')
################Readonly################
Product.Attr('SC_HWOS_Service_Product_ScopeSummary').Access = AttributeAccess.ReadOnly
Product.Attr('EnabledService_Entitlement').Access = AttributeAccess.ReadOnly
Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').Access = AttributeAccess.ReadOnly
Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').Access = AttributeAccess.ReadOnly
Product.Attr('Matrix License').Access = AttributeAccess.ReadOnly
Product.Attr("DurationOfPlan_enabledServices").Access = AttributeAccess.ReadOnly
