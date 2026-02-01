import GS_ItemCalculations as ic

def getCFValue(field):
	return Quote.GetCustomField(field).Content

def setCFValue(field, value):
	Quote.GetCustomField(field).Content = value
if Session["prevent_execution"] != "true":
	setCFValue('Published Lead Time', '0')
	Trace.Write("Published Lead Time1  = " +str(getCFValue('Published Lead Time')))
	for item in Quote.Items:
		ic.calculatePublishedLeadTime(Quote , item)

	if not getCFValue('Published Lead Time'):
		setCFValue('Published Lead Time', '0')
	Trace.Write("Published Lead Time2  = " +str(getCFValue('Published Lead Time')))