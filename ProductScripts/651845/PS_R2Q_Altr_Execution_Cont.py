pole = Quote.GetCustomField('R2Q_Booking_Pole').Content
if pole == 'APAC':
	allowlist = ['India','None']
elif pole == 'EMEA':
	allowlist = ['France', 'Finland', 'Italy', 'United Kingdom','None']
elif pole == 'AMER':
	allowlist = ['United States', 'Canada','None']
else:
	allowlist = []

disallowlist = []
Prj_cont = Product.GetContainerByName("R2Q_Project_Questions_Cont")
for row in Prj_cont.Rows:
	attr_val = row.Product.Attr("R2Q_Alternate_Execution_Country").Values
	disallowlist = [i.ValueCode for i in attr_val if i.ValueCode not in allowlist]
	row.Product.DisallowAttrValues("R2Q_Alternate_Execution_Country", *disallowlist)
	if row["R2Q_Alternate_Execution_Country"] == '' :
		row["R2Q_Alternate_Execution_Country"] = "None"
		row.Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue("None")
	Trace.Write("R2Q_Alternate_Execution_Country==:"+str(row["R2Q_Alternate_Execution_Country"]))

Product.DisallowAttrValues("R2Q_Alternate_Execution_Country", *disallowlist)