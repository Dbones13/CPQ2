import math
Duration=0
years=months='0'
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
	Trace.Write(Product.Attr('ContractEndDate_EnabledService').GetValue())
	if Product.Attr('ContractEndDate_EnabledService').GetValue() !='' and Product.Attr('ContractStartDate_EnabledService').GetValue() !='':
		Duration =(DateTime.Parse(Product.Attr('ContractEndDate_EnabledService').GetValue()).Subtract(DateTime.Parse(Product.Attr('ContractStartDate_EnabledService').GetValue())).Days )
		years = str(int(math.ceil(Duration // 365.2425)))
		years_r = Duration  % 365.2425
		days_r = int(math.ceil(years_r % 30.436875))
		if days_r <= 15:
			months = str(int(math.ceil(years_r // 30.436875)))
		else:
			months = str(int(math.ceil(years_r // 30.436875)) + 1)
		if int(months) == 12:
			years = str(int(years)+1)
			months = str(0)
		if int(Duration) < 0 or int(Duration) == 0:
			years = '0'
			months = '0'
			Product.ResetAttr('ContractEndDate_EnabledService')
			Trace.Write("lahu")
	Product.Attr('DurationOfPlan_enabledServices').AssignValue(str(years + "." + months))
	Trace.Write(str(years + "." + months))