Product.GetContainerByName('Write-In Entitlements for Cyber').Rows.Clear()
from GS_PCN_Populate_Write_Ins import updateWriteIn
if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
	updateWriteIn(Product)
	Product.Attr('CyberChildFlag').AssignValue('True')