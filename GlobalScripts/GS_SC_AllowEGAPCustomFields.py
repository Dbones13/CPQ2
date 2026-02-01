def SC_AllowEGAPCustomFields(Quote):
	Quote_Type = Quote.GetCustomField("Quote Type").Content

	if  Quote_Type in ("Contract New","Contract Renewal"):
		#To show the EGAP fields for contract quotes.
		Quote.CustomFields.Allow('EGAP_Proposal_Type','EGAP_Contract_Start_Date','EGAP_Contract_End_Date','EGAP_Project_Duration_Months')

		#To se the default values if quote type is contract new
		if  Quote_Type == "Contract New":
			if Quote.GetCustomField("SC_CF_CURANNDELSTDT").Content == '':
				Quote.GetCustomField("SC_CF_CURANNDELSTDT").Content  = UserPersonalizationHelper.ToUserFormat(Quote.EffectiveDate)

			if Quote.GetCustomField("EGAP_Contract_Start_Date").Content == '':
				Quote.GetCustomField("EGAP_Contract_Start_Date").Content = str(Quote.GetCustomField("SC_CF_CURANNDELSTDT").Content)

			if not Quote.GetCustomField("SC_CF_AGREEMENT_TYPE").Content:
				Quote.GetCustomField("SC_CF_AGREEMENT_TYPE").Content = 'None'

			if not Quote.GetCustomField('SC_CF_ORDER_REASON').Content:
				Quote.GetCustomField('SC_CF_ORDER_REASON').Content = '700 CS - Service Contract Booking'

		#To se the default value,hide field and hide dropdown if quote type is contract renewal
		elif Quote_Type == "Contract Renewal":
			if not Quote.GetCustomField('SC_CF_ORDER_REASON').Content:
				Quote.GetCustomField('SC_CF_ORDER_REASON').Content = '716 CS - Service Contract Renewals'

			Quote.GetCustomField('Language').Visible = False
			#CXCPQ-107719 As a part of this story commented a below code.
			'''AgreemntAttrVals = Quote.GetCustomField('SC_CF_AGREEMENT_TYPE').AttributeValues
			for value in AgreemntAttrVals:
				if value.DisplayValue == "ISA":
					value.Allowed = False
					break'''