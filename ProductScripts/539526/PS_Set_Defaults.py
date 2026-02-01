# ================================================================================================
# Component: PLC Remote Group
# Author: Ashok Kandi
# Purpose: This is used to create a adding row in a container having the attributes when product is loaded.
# Date: 02/08/2022
# ================================================================================================

import GS_CE_Utils
import GS_DropDown_Implementation
Product.Messages.Clear()
def getContainer(Name):
    return Product.GetContainerByName(Name)

GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)

attrs = [
         "PLC_RG_Other_IO_Cont", "PLC_RG_Additional_Controller_Cont",
         "PLC_RG_Comm_Interface_Cont",
		 "PLC_RG_Cabinet_Cont", "PLC_RG_Controller_Rack_Cont"
		]

for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        container.AddNewRow(True)
        container.Calculate()

#Redundant & Non-Redundant in single container
PLC_RG_UIO_Cont = Product.GetContainerByName("PLC_RG_UIO_Cont")
if PLC_RG_UIO_Cont.Rows.Count == 0:
    for row in range(2):
        PLC_RG_UIO_Cont.AddNewRow(True)
        PLC_RG_UIO_Cont.Calculate()