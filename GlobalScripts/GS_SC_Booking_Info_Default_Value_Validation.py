def getCFValue(quote , cfName):
	return quote.GetCustomField(cfName).Content

Quote_Type = getCFValue(Quote,'Quote Type')

if Quote_Type in ['Contract New','Contract Renewal']:
    Quote.GetCustomField('ProfitCentre').Required = True
    if getCFValue(Quote,'SC_CF_Do_not_send_Survey') == 'true':
        Quote.GetCustomField('SC_CF_1st_Survey_Month').Visible = False
        Quote.GetCustomField('SC_CF_2nd_Survey_Month').Visible = False
    else:
        Quote.GetCustomField('SC_CF_1st_Survey_Month').Visible = True
        Quote.GetCustomField('SC_CF_2nd_Survey_Month').Visible = True

    first_year_survey = TagParserQuote.ParseString('<* TABLE ( SELECT Survey_Month_1 FROM CT_SC_Survey_Months WHERE Renewal_Months = <*CTX( Quote.CustomField(SC_CF_CURANNDELSTDT).Format(MM) )*>) *>')
    Quote.GetCustomField('SC_CF_1st_Survey_Month').Content = first_year_survey 
    CurrAnulDeli_St_Dt = UserPersonalizationHelper.CovertToDate(getCFValue(Quote,'SC_CF_CURANNDELSTDT'))
    CurrAnulDeli_Ed_Dt = UserPersonalizationHelper.CovertToDate(getCFValue(Quote,'SC_CF_CURANNDELENDT'))

    if CurrAnulDeli_St_Dt.Year == CurrAnulDeli_Ed_Dt.Year:
    	month_diff = abs(int(CurrAnulDeli_St_Dt.Month) - int(CurrAnulDeli_Ed_Dt.Month))
    else:
        month_diff = 0
        
    if month_diff >= 8 or month_diff ==0:
    	SecMonth = TagParserQuote.ParseString("<* TABLE ( SELECT Survey_Month_2 FROM CT_SC_Survey_Months WHERE Renewal_Months = <*CTX( Quote.CustomField(SC_CF_CURANNDELSTDT).Format(MM) )*>) *>")
    	Quote.GetCustomField('SC_CF_2nd_Survey_Month').Content = str(SecMonth) 
    else:
    	SecMonth = TagParserQuote.ParseString("<* TABLE ( SELECT Survey_Month_2 FROM CT_SC_Survey_Months WHERE Survey_Month_2_No = <*CTX( Quote.CustomField(SC_CF_CURANNDELENDT).Format(MM) )*>) *>")
    Quote.GetCustomField('SC_CF_2nd_Survey_Month').Content = str(SecMonth)

OrderAttrValues = Quote.GetCustomField('SC_CF_ORDER_REASON').AttributeValues
if Quote_Type == 'Contract New':
    for value in OrderAttrValues:
		if value.DisplayValue == "716 CS - Service Contract Renewals":
			value.Allowed = False

if Quote_Type == 'Contract Renewal':
    for value in OrderAttrValues:
		if value.DisplayValue == "700 CS - Service Contract Booking":
			value.Allowed = False