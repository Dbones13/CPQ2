if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    #Number of years in Price Calculator
	Duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
	ContractExt = Quote.GetCustomField('SC_CF_IS_CONTRACT_EXTENSION').Content
	Remove_str = "years"
	Year = []
	for ele in Duration:
		if ele not in Remove_str:
			Year.append(ele)
	Year = ''.join(Year)
	if ContractExt == "True":
		Year = "1"
	Product.Attr('SC_QCS_Number of Years').Access = AttributeAccess.ReadOnly
	Product.Attr('SC_QCS_Number of Years').AssignValue(Year)