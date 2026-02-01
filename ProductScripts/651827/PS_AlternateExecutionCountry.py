import datetime
getvalpar = Product.Attr('AR_HCI_GES Participation %').GetValue()
if not getvalpar:
    Product.Attr('AR_HCI_GES Participation %').AssignValue('0')
#if Quote.GetCustomField('IsR2QRequest').Content:
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

attr_val = Product.Attr("R2Q_Alternate_Execution_Country").Values
disallowlist = [i.ValueCode for i in attr_val if i.ValueCode not in allowlist]
Product.DisallowAttrValues("R2Q_Alternate_Execution_Country", *disallowlist)
alncntry_length = len(allowlist)
if Product.Attr("R2Q_Alternate_Execution_Country").GetValue() != Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content and alncntry_length != 2:
	Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue("None")
else:
	if alncntry_length == 2 and allowlist[1] == 'None':
		Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(allowlist[0])
	else:
		Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content)
# Execution Years restriction
current_year = datetime.datetime.now().year
yearlist = [str(current_year+i) for i in range(0,3)]
a=Product.Attr("Project_Execution_Year").Values
removelist = [i.ValueCode for i in a if i.ValueCode not in yearlist]
Product.DisallowAttrValues("Project_Execution_Year",*removelist)