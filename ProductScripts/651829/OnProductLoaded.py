if Product.Attr("Total Number of Displays").GetValue() == '':
	Product.Attr("Total Number of Displays").AssignValue("0")
Product.Attr("Total Number of Displays").Access = AttributeAccess.ReadOnly
Product.Attr("R2QRequest").AssignValue("Yes")
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
loc_dict = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","None":"None","null":"None"}
gesloc = Quote.GetGlobal('ExGesLocation')
if gesloc is not None and gesloc != "":
	ges_location = loc_dict.get(gesloc)
	Product.Attr('Experion_HS_Ges_Location_Labour').SelectDisplayValue(ges_location)
else:
	Product.Attr('Experion_HS_Ges_Location_Labour').SelectDisplayValue('None')

attrList = ["Number of Operator Console Sections", "Number of Server Types", "Number of Modbus Interfaces", "Number of OPC Interfaces", "Number of Fieldbus Devices", "Number of Profibus Devices", "Number of EtherNet IP Devices", "Number of EtherNet IP Interface Cards", "Number of Profibus Interface Cards", "Number of FTE Communities", "Number of FTE Community Locations", "Number of Locations with FTE Switches", "Number of Modbus Interfaces Types", "Number of Profibus Interface Types", "Number of EtherNet IP Interface Types", "Number of OPC Interface Types","Experion_HS_Ges_Location_Labour"]

for attr in attrList:
	Product.Attr(attr).Access = AttributeAccess.Hidden