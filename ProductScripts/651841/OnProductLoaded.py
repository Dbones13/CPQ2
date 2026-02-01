# ================================================================================================
# Component: PLC System
# Author: Ashok Kandi
# Purpose: This is used to create a adding row in a container having the attributes when product is loaded.
# Date: 02/08/2022
# ================================================================================================
import GS_DropDown_Implementation

GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)

def getContainer(Name):
    return Product.GetContainerByName(Name)

attrs = ["PLC_Common_Questions_Cont", "PLC_Software_Question_Cont","PLC_Labour_Details", "Number_PLC_Control_Groups","CE PLC Additional Custom Deliverables","CE_PLC_System_Hardware"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        container.AddNewRow(True)
        container.Calculate()