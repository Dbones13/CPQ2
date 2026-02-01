# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)

def getContainer(Name):
    return Product.GetContainerByName(Name)

attrs = ["RTU_Software_Labor_Container1", "RTU_Software_Labor_Container2","Number_RTU_Control_Groups", "CE RTU Additional Custom Deliverables"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        row = container.AddNewRow(False)
        if attr == 'RTU_Software_Labor_Container1':
            row.SetColumnValue('RTU_System_Software_Release', '182')
            row.GetColumnByName('RTU_System_Software_Release').SetAttributeValue('182')
            row.SetColumnValue('RTU_Base_Media_delivery', 'ED')
            row.GetColumnByName('RTU_Base_Media_delivery').SetAttributeValue('ED')
            row.SetColumnValue('RTU_Builder_Client', '0')
            row.SetColumnValue('RTU_Engineering_Stations', '0')
            row.SetColumnValue('RTU_Gas_Liquid_Metering_Calcs', 'No')
            row.GetColumnByName('RTU_Gas_Liquid_Metering_Calcs').SetAttributeValue('No')
        elif attr == 'RTU_Software_Labor_Container2':
            row.SetColumnValue('RTU_Application_Type','None')
            row.GetColumnByName('RTU_Application_Type').SetAttributeValue('None')
            row.SetColumnValue('RTU_GES_Location','None')
            row.GetColumnByName('RTU_GES_Location').SetAttributeValue('None')
            row.SetColumnValue('RTU_Loop_Typical', '0')
            row.SetColumnValue('RTU_Switches', '0')
        elif attr == 'Number_RTU_Control_Groups':
            row.SetColumnValue('Number_RTU_Control_Groups','1')
        elif attr == 'CE RTU Additional Custom Deliverables':
            row.GetColumnByName('FO Eng').SetAttributeValue('SYS LE1-Lead Eng')
            row['FO Eng']='SYS LE1-Lead Eng'
            row.Product.Attr('CE_UOC_FO_ENG_LD').SelectDisplayValue('SYS LE1-Lead Eng')
            #row['FO Eng']='SYS LE1-Lead Eng'
            row.ApplyProductChanges()
        row.Calculate()
        container.Calculate()