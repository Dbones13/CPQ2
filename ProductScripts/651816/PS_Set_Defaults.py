#import GS_CE_Utils

def getContainer(Name):
	return Product.GetContainerByName(Name)
#Product.Messages.Clear()
attrs = ["UOC_CG_Cabinet_Cont", "UOC_CG_Controller_Rack_Cont", "UOC_CG_PF_IO_Cont",
		 "UOC_CG_Additional_Controller_Cont", "UOC_CG_Other_IO_Cont","Number_UOC_Remote_Groups"]
for attr in attrs:
	container = getContainer(attr)
	if container.Rows.Count == 0:
		container.AddNewRow(True)
		container.Calculate()

#Redundant & Non-Redundant in single container
UOC_CG_UIO_Cont = Product.GetContainerByName("UOC_CG_UIO_Cont")
if UOC_CG_UIO_Cont.Rows.Count == 0:
	for row in range(2):
		UOC_CG_UIO_Cont.AddNewRow(True)
		UOC_CG_UIO_Cont.Calculate()

#GS_CE_Utils.setContainerDefaults(Product)
rg_cont = Product.GetContainerByName('Number_UOC_Remote_Groups')
rg_cont.Rows[0].SetColumnValue('Number_UOC_Remote_Groups', '0')
uoc_cg_cabinet= Product.GetContainerByName("UOC_CG_Cabinet_Cont").Rows
if uoc_cg_cabinet.Count:
    if not uoc_cg_cabinet[0]["UOC_Cabinet_Spare_Space"]:
        uoc_cg_cabinet[0].SetColumnValue("UOC_Cabinet_Spare_Space",'0')
        Trace.Write("Product Updated")