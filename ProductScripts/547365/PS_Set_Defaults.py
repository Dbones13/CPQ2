import GS_CE_Utils

def getContainer(Name):
	return Product.GetContainerByName(Name)

attrs = ["Number_CN900_Control_Groups","CN900_Labor_Details","CE CN900 Additional Custom Deliverables"]
setDefault = False
for attr in attrs:
	container = getContainer(attr)
	if container.Rows.Count == 0:
		setDefault = True
		container.AddNewRow(False)
		container.Calculate()

attrs = ["CN900_Common_Questions_Cont"]
#setDefault = False
for attr in attrs:
	container = getContainer(attr)
	if container.Rows.Count == 0:
		setDefault = True
		container.AddNewRow('CN900_System_cpq',False)
		container.Calculate()

labor_cont = Product.GetContainerByName('CE CN900 Additional Custom Deliverables')
labor_cont.Rows[0].Product.Attr('CE_CN900_FO_ENG_LD').SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Rows[0].Calculate()
labor_cont.Calculate()

if setDefault:
	GS_CE_Utils.setContainerDefaults(Product)