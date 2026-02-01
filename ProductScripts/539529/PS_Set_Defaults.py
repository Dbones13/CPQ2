# ================================================================================================
# Component: PLC Control Group
# Author: Ashok Kandi
# Purpose: This is used to create a adding row in a container having the attributes when product is loaded.
# Date: 02/08/2022
# ================================================================================================
import GS_CE_Utils
import GS_DropDown_Implementation

GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)
Product.Messages.Clear()
def getContainer(Name):
    return Product.GetContainerByName(Name)

attrs = [
         "PLC_CG_Comm_Interface_Cont", "PLC_CG_Cabinet_Cont","PLC_CG_Controller_Rack_Cont",
         "PLC_CG_Other_IO_Cont", "PLC_CG_Additional_Controller_Cont",
		 "PLC_CG_Software_Cont", "Number_PLC_Remote_Groups"
		]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        container.AddNewRow(True)
        container.Calculate()

#Redundant & Non-Redundant in single container
PLC_CG_UIO_Cont = Product.GetContainerByName("PLC_CG_UIO_Cont")
if PLC_CG_UIO_Cont.Rows.Count == 0:
    for row in range(2):
        PLC_CG_UIO_Cont.AddNewRow(True)
        PLC_CG_UIO_Cont.Calculate()

GS_CE_Utils.setContainerDefaults(Product)
Product.Attr('isProductLoaded').AssignValue('True')

isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Quote.GetCustomField('R2QFlag').Content == "Yes" and Checkproduct == "PRJT R2Q":
    rg_cont = Product.GetContainerByName('Number_PLC_Remote_Groups')
    rg_cont.Rows[0].SetColumnValue('Number_PLC_Remote_Groups', '0')