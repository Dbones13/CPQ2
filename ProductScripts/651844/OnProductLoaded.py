import datetime
current_year = datetime.datetime.now().year
yearlist = [str(current_year+i) for i in range(0,3)]
removelang=['Korean','Portuguese']
attrs = ["R2Q_Project_Questions_Cont","Labor_details_newexapnsion_cont2","R2Q_Project_Questions_TAS_Cont"]
for attr in attrs:
	container = Product.GetContainerByName(attr)
	if container.Rows.Count == 0:
		container.AddNewRow(False)

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))
def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

nonR2QAttr = ["Is Modbus Interface in Scope?","Is OPC Interface in Scope?"]
scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope=="":
	Product.Attr('CE_Scope_Choices').SelectDisplayValue('HW/SW + LABOR')
nonR2QContColumn = {
	"R2Q_Project_Questions_Cont": ["Project Type","Project Category","Contracting Parties","Internal Parties","Project Exeuction Locations","Project Team Size","Estimated_Project_Value_Cost"],"Labor_details_newexapnsion_cont2":['Is System Network Engineering in Scope','Is HMI Engineering in Scope','Is Fieldbus Interface in Scope','Is Profibus Interface in Scope','Is EtherNet IP Interface in Scope','Is HART Interface in Scope','Is Terminal Server Interface in Scope','Is DeviceNet Interface in Scope']
}
hideContainerColumns(nonR2QContColumn)
proplang = Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content
Prj_cont = Product.GetContainerByName("R2Q_Project_Questions_Cont")
for row in Prj_cont.Rows:
	row["MIB Configuration Required?"] = "No"
	a=row.Product.Attr("Project_Execution_Year").Values
	removelist = [i.ValueCode for i in a if i.ValueCode not in yearlist]
	row.Product.DisallowAttrValues("Project_Execution_Year",*removelist)
	row.Product.DisallowAttrValues("R2Q_PRJT_Proposal Language",*removelang)
	row.Product.Attr("Languages").SelectDisplayValue("English")
	row["Languages"] = "English"
	row["R2Q_PRJT_Proposal Language"] = "English"
	row.Product.Attributes.GetByName('Languages').AssignValue("English")
	row.Product.Attributes.GetByName('Languages').SelectDisplayValue("English")
	row.Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').AssignValue("English")
	row.Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').SelectDisplayValue("English")
	if proplang != '' and proplang != row.Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').GetValue():
		row.Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').SelectDisplayValue(proplang)
	row.Calculate()
Product.Attributes.GetByName('Languages').AssignValue('English')
Product.DisallowAttrValues("Project_Execution_Year",*removelist)
Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').AssignValue('English')
Product.DisallowAttrValues("R2Q_PRJT_Proposal Language",*removelang)
Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('R2Q_Project_Questions_Cont','Languages'))
Product.Attr('CE_Site_Voltage').AssignValue("120V")
# Assign Value for Excahnge Rate Custom Field
res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
if Quote.GetCustomField('Exchange Rate').Content == '':
	Quote.GetCustomField('Exchange Rate').Content = res.Exchange_Rate