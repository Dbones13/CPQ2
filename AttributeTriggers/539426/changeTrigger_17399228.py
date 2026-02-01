def getContainer(Name):
    return Product.GetContainerByName(Name)

def setDefaultValue(container,Row):
    ColumnSet1 = {'Orion_Auxiliary_Equipment_Unit_AEU_Turret_Type':'None','Orion_Monitor_Type':'55-inch', 'Orion_Membrane_Keyboard_Type':'None', 'Orion_Advanced_Solution_Pack_license_required':'No', 'Orion_Turret_Position_for_the_Left_Ext_Aux_Equip_Unit':'Wide', 'Orion_Turret_Position_for_the_Right_Ext_Aux_Equip_Unit':'Wide', 'Orion_Turret_Position_for_the_Center_Curved_Ext_Aux_Equip_Unit':'Wide', 'Orion_Remote_Peripheral_Solution_RPS_Type':'None', 'Orion_Extended_Heigh_Alarm_Ligth_Panel':'No', 'Orion_Console_Alarm_Light_Custom_Logo':'No','Orion_Alarm_Sounds':'No'}
    ColumnSet2 = {'Orion_Number_of_console_bases_with_same_configuration':"0",'Orion_Number_of_2_Position_Base_Unit':"0",'Orion_Number_of_3_Position_Base_Unit':"0",'Orion_Number_of_Left_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Right_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Straight_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Curved_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Curved_Extended_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Joining_Unit':"0",'Orion_Number_of_Jack_Lift_&_Ramps_System_needed':"0",'Orion_Number_of_Additional_23_monitors':"0",'Orion_Number_of_Additional_Monitor_Mounting_Arm_for_23':"0",'Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit':"0",'Orion_Display_Devices_per_position':'1'}
    columnList = []
    Container = getContainer(container)
    for col in Row.Columns:
        if col.Name in ColumnSet1:
            col.SetAttributeValue(ColumnSet1[col.Name])
        elif col.Name in ColumnSet2:
            Row.SetColumnValue(col.Name,ColumnSet2[col.Name])

NoOfOrion = Product.Attr('Attr_NoOfOrion Console').GetValue()
newValue = 0 if NoOfOrion == '' else int(NoOfOrion)
container = Product.GetContainerByName('Orion_Station_Configuration')
oldValue = container.Rows.Count
Trace.Write("oldValue = " +str(oldValue) + " newValue = " +str(newValue))
if newValue <=5:
    if newValue == 0:
        Product.GetContainerByName('Orion_Station_Configuration').Rows.Clear()
        Product.Attr('Attr_NoOfOrion Console').AssignValue(str(0))
    elif newValue > oldValue:
        difference = (newValue - oldValue)
        '''if container.Rows.Count == 0:
            difference = (newValue - oldValue)+1
        else:
            difference = (newValue - oldValue)'''
        for i in range(difference):
            row = container.AddNewRow()
            setDefaultValue('Orion_Station_Configuration', row)
    elif newValue < oldValue:
        difference = oldValue - newValue
        for i in range(oldValue, newValue, -1):
            Product.GetContainerByName('Orion_Station_Configuration').DeleteRow(i-1)
    if newValue!=0:
        Product.Attributes.GetByName('IncompleteOrionCheck').AssignValue(str(True))
    else:
        Product.Attributes.GetByName('IncompleteOrionCheck').AssignValue(str(False))
else:
    Product.Attr('Attr_NoOfOrion Console').AssignValue(str(0))
    Product.GetContainerByName('Orion_Station_Configuration').Rows.Clear()
    Trace.Write("1....oldValue = " +str(oldValue) + " newValue = " +str(newValue))