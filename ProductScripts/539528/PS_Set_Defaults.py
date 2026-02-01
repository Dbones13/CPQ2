# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)

Product.Messages.Clear()
def getContainer(Name):
    return Product.GetContainerByName(Name)

# attrs = ["RTU_CG_Cabinet_Cntr_Cont", "RTU_CG_IO_Container","RTU_CG_Sofware_Cont","RTU_CG_AdditionalController_Ques_Cont","RTU_CG_Labor_Cont"]
attrs = ["RTU_CG_Cabinet_Cont","RTU_CG_Controller_Cont", "RTU_CG_IO_Container","RTU_CG_Sofware_Cont","RTU_CG_AdditionalController_Ques_Cont","RTU_CG_Labor_Cont"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        row = container.AddNewRow(False)
        if attr == 'RTU_CG_Cabinet_Cont':
            row.GetColumnByName('Cabinet_Type').SetAttributeValue('Dual')
            #row.SetColumnValue('Cabinet_Door_Type', 'Standard')
            #row.GetColumnByName('Cabinet_Door_Type').SetAttributeValue('Standard')
            row.SetColumnValue('Cabinet_Base_Size', '100mm')
            row.SetColumnValue('Cabinet_Door_Keylock', 'Standard')
            row.SetColumnValue('Cabinet_Power_Entry', 'None')
            row.GetColumnByName('Cabinet_Power_Entry').SetAttributeValue('None')
            row.SetColumnValue('Cabinet_Thermostat', 'No')
            row.SetColumnValue('Cabinet_Light', 'No')
            row.GetColumnByName('Cabinet_Light').SetAttributeValue('No')
            row.GetColumnByName('Cabinet_Thermostat').SetAttributeValue('No')
            row.SetColumnValue('Cabinet_Spare_space', '0')            
            row.SetColumnValue('Integrated_Marshalling_Cabinet', 'No')
            row.GetColumnByName('Integrated_Marshalling_Cabinet').SetAttributeValue('No')            
        elif attr =='RTU_CG_Controller_Cont':
            row.SetColumnValue('Replica_configurations', '1')
            row.SetColumnValue('IO_Spare_Percentage', '0')
            row.SetColumnValue('Power_Supply_Type', 'Redundant')
            row.GetColumnByName('Power_Supply_Type').SetAttributeValue('Redundant')
            row.SetColumnValue('Power_Supply_Model','Meanwell')
            row.GetColumnByName('Power_Supply_Model').SetAttributeValue('Meanwell')
            row.SetColumnValue('Controller_Redundancy', 'Redundant')
            row.GetColumnByName('Controller_Redundancy').SetAttributeValue('Redundant')
        elif attr == 'RTU_CG_IO_Container':
            for col in row.Columns:
                if col.Name == 'FIM_devices_segment_withOpen_loop':
                    row[col.Name] = '10'
                else:
                    row[col.Name] = '0'
        elif attr in ['RTU_CG_Sofware_Cont', 'RTU_CG_AdditionalController_Ques_Cont']:
            for col in row.Columns:
                row[col.Name] = '0'
        elif attr == 'RTU_CG_Labor_Cont':
            row.SetColumnValue('Marshalling_Cabinet_Count', '0')
            row.SetColumnValue('AGA_Calculation_present', 'Yes')
            row.GetColumnByName('AGA_Calculation_present').SetAttributeValue('Yes')
        row.Calculate()
        container.Calculate()