Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

def getContainer(Name):
	return Product.GetContainerByName(Name)

attrs = ["UOC_RG_Controller_Rack_Cont", "UOC_RG_Cabinet_Cont","UOC_RG_PF_IO_Cont","UOC_RG_Other_IO_Cont"]
for attr in attrs:
	container = getContainer(attr)
	if container.Rows.Count == 0:
		container.AddNewRow(True)
		container.Calculate()

#Redundant & Non-Redundant in single container
UOC_RG_UIO_Cont = Product.GetContainerByName("UOC_RG_UIO_Cont")
if UOC_RG_UIO_Cont.Rows.Count == 0:
	for row in range(2):
		UOC_RG_UIO_Cont.AddNewRow(True)
		UOC_RG_UIO_Cont.Calculate()