from GS_SC_SESP_COST import BurdenRateCostValue
if Product.Name != 'Service Contract Product':
	validModelCont      = Product.GetContainerByName("SC Other Cost Details")
	siteAnnualAuditList = ["System Audit","EMA"]
	burdenrate = BurdenRateCostValue(Quote)
	for i in range(0,2):
		row = validModelCont.AddNewRow(True)
		row["Site Annual Audit"] = siteAnnualAuditList[i]
		if row["Site Annual Audit"] == "System Audit" and row["Labor Hours"]:
			row["Labor Hours"]= '8'
		elif row["Site Annual Audit"] == "EMA":
			row["Labor Hours"]= '6'
		else:
			row["Labor Hours"]= '0'
		#cost as Labor Hours * Burden rate
		row["Cost"] = str(int(row["Labor Hours"]) * burdenrate )