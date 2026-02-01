import GS_CE_Utils

def getContainer(Name):
	return Product.GetContainerByName(Name)

attrs = ["UOC_Common_Questions_Cont", "UOC_Software_Question_Cont","Number_UOC_Control_Groups","UOC_Labor_Details","CE UOC Additional Custom Deliverables"]
setDefault = False
for attr in attrs:
	container = getContainer(attr)
	if container.Rows.Count == 0:
		setDefault = True
		container.AddNewRow(False)
		container.Calculate()

labor_base_cont = getContainer('UOC_Labor_Base_Details')
if labor_base_cont.Rows.Count == 0:
	base_details = SqlHelper.GetList("Select * from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' and Container_Name ='{1}' ".format('ControlEdge UOC System', 'UOC_Labor_Base_Details'))
	for value in base_details:
		base_row = labor_base_cont.AddNewRow(False)
		base_row['Labor_Deliverable'] = value.Cont_ColumnName
		base_row['Less_Than_IO'] = str(value.Min)
		base_row['Greater_Than_IO'] = str(value.Max)
		base_row['Base_Values'] = str(value.Min + value.Max)

nonr2q = Quote.GetCustomField('R2QFlag').Content
if not nonr2q:
	gesLocation = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName('UOC_Ges_Location_Labour').Value
	gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','None':'None','GESEgypt':'EG'}
	gesLocationVC = gesMapping.get(gesLocation)
else:
	gesLocationVC = Quote.GetGlobal('ExGesLocation')
bookingLOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
if setDefault:
	GS_CE_Utils.setContainerDefaults(Product)

labor_cont = Product.GetContainerByName('CE UOC Additional Custom Deliverables')
if bookingLOB != 'LSS':
	labor_cont.Rows[0].GetColumnByName('FO Eng').SetAttributeValue('SYS LE1-Lead Eng')
	labor_cont.Rows[0].Product.Attr('CE_UOC_FO_ENG_LD').SelectDisplayValue('SYS LE1-Lead Eng')
	labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
else:
	labor_cont.Rows[0].GetColumnByName('FO Eng').SetAttributeValue('SVC-ESSS-ST Site Support Spec')
	labor_cont.Rows[0].Product.Attr('CE_UOC_FO_ENG_LD').SelectDisplayValue('SVC-ESSS-ST Site Support Spec')
	labor_cont.Rows[0]['FO Eng']='SVC-ESSS-ST Site Support Spec'
	if gesLocationVC != 'None':
		labor_cont.Rows[0].GetColumnByName('GES Eng').SetAttributeValue('LSS GES Eng-BO-'+gesLocationVC)
		labor_cont.Rows[0].Product.Attr('CE UOC GES Eng').SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
		labor_cont.Rows[0]['GES Eng']='LSS GES Eng-BO-'+gesLocationVC
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Rows[0].Calculate()
labor_cont.Calculate()

if Product.Name == "ControlEdge UOC System Migration":
	Product.Attr("Labor_Percentage_FAT").AssignValue("0")
