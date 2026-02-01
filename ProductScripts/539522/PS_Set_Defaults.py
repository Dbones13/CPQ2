# ================================================================================================
# Component: UOC Remote Group
# Author: Ashok Kandi
# Purpose: This is used to create a adding row in a container having the attributes when product is loaded.
# Date: 03/02/2022
# ================================================================================================
import GS_CE_Utils

def getContainer(Name):
    return Product.GetContainerByName(Name)

Product.Messages.Clear()

attrs = [
         "UOC_RG_Controller_Rack_Cont", "UOC_RG_Cabinet_Cont",
         "UOC_RG_PF_IO_Cont",
		 "UOC_RG_Other_IO_Cont"
		]


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

GS_CE_Utils.setContainerDefaults(Product)