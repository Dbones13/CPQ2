# ================================================================================================
# Component: System Group
# Author: Ashok Kandi
# Purpose: This is used to create a adding row in a container having the attributes when product is loaded.
# Date: 02/08/2022
# ================================================================================================

def getContainer(Name):
    return Product.GetContainerByName(Name)


attrs = ["CE_General_Inputs_Cont"]

for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        container.AddNewRow(True)
        container.Calculate()