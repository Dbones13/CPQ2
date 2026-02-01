try:
    scope = Product.Attr('Scope').SelectedValue.Display
except:
    scope = Product.Attributes.GetByName('Scope').GetValue()

def getContainer(containerName):
    return Product.GetContainerByName(containerName)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0
if scope == 'LABOR':
	third_party_cont = Product.GetContainerByName("C200_Third_Party_Items_Cont")
	third_party_cont.Clear()
incomplete = []
c200MigrationgeneralQns = getContainer('C200_Migration_General_Qns_Cont')
c200migrationScenario = Product.Attr('C200_Select_Migration_Scenario').GetValue()
c200Configurations = getContainer('C200_Migration_Config_Cont')
rowScenario = Product.Attributes.GetByName('C200_Select_Migration_Scenario').GetValue()
if c200MigrationgeneralQns.Rows.Count>0:
    rowsGQns = c200MigrationgeneralQns.Rows[0]
    rowC200Migrations = str(rowsGQns['C200_How_many_C200s_are_we_migrating'])
    rowC200Colocated = str(rowsGQns['C200_How_many_co_located_C200_groups_exists'])
    if str(rowC200Migrations) in ['0','0.0'] or str(rowC200Migrations) == '':
        incomplete.append("C200_How_many_C200s")
    if (rowC200Colocated in ['0','0.0'] or str(rowC200Colocated) == '')and (rowScenario == 'C200 to ControlEdge UOC') and (scope == 'HW/SW' or scope == 'HW/SW/LABOR'):
        incomplete.append("C200_How_many_Co_located")
if c200Configurations.Rows.Count>0:
    rowsConfig = c200Configurations.Rows
    for configrow in rowsConfig:
        rowPMIOMs = getFloat(configrow['C200_Number_of_PM_IOMs'])
        row1756IOMs = getFloat(configrow['C200_Number_of_1756_IOMs'])
        rowABIOMs = getFloat(configrow['C200_Number_of_Serial_Interface_Allen_Bradley_IOMs'])
        rowABPoints = getFloat(configrow['C200_Number_of_Serial_Interface_Allen_Bradley_points'])
        rowModbusIOMs = getFloat(configrow['C200_Number_of_Serial_Interface_Modbus_IOMs'])
        rowModbusPoints = getFloat(configrow['C200_Number_of_Serial_Interface_Modbus_points'])
        rowSIIOMs = getFloat(configrow['C200_Number_of_Serial_Interface_IOMs'])
        rowSIPoints = getFloat(configrow['C200_Number_of_Serial_Interface_points'])
        rowAIORacks = getFloat(configrow['C200_C300_Number_of_Series_A_IO_Racks'])
        rowAIOUOCRacks =  getFloat(configrow['C200_UOC_Number_of_Series_A_IO_Racks'])
        if (str(rowPMIOMs) in ['0','0.0'] or str(rowPMIOMs) == '') and (str(row1756IOMs) in ['0','0.0'] or str(row1756IOMs) == '') and (str(rowScenario )== 'C200 to C300') and (str(scope) == 'HW/SW' or str(scope) == 'HW/SW/LABOR'):
            incomplete.append("C200_Both_questions_PMIOMs_1756IOMs")
        if (rowABIOMs > 0 and str(rowABIOMs) != '' and rowABIOMs != 0) and (rowABPoints == 0 or str(rowABPoints) == '') and (rowScenario == 'C200 to C300') and (scope == 'LABOR' or scope == 'HW/SW/LABOR'):
            incomplete.append("C200_Serial_Interface_Allen_Bradley")
        if (rowModbusIOMs > 0 and rowModbusIOMs != '' and rowModbusIOMs != 0) and (rowModbusPoints == 0 or str(rowModbusPoints) == '') and (rowScenario == 'C200 to C300') and (scope == 'LABOR' or scope == 'HW/SW/LABOR'):
            incomplete.append("C200_Serial_Interface_Modbus")
        if (rowSIIOMs > 0 and str(rowSIIOMs) != '' and rowSIIOMs != 0) and (rowSIPoints == 0 or str(rowSIPoints) == '') and (rowScenario == 'C200 to ControlEdge UOC') and (rowScenario != 'C200 to C300') and (scope == 'LABOR' or scope == 'HW/SW/LABOR'):
            incomplete.append("C200_Serial_Interface")
        if (row1756IOMs > 0 and str(row1756IOMs) != '' and row1756IOMs != 0) and (rowAIORacks == 0 or str(rowAIORacks) == '') and (rowScenario == 'C200 to C300') and (scope == 'HW/SW' or scope == 'HW/SW/LABOR'):
            incomplete.append("C200_A_IO_Racks")
        if (row1756IOMs > 0 and str(row1756IOMs) != '' and row1756IOMs != 0) and (rowAIOUOCRacks == 0 or str(rowAIOUOCRacks) == '') and (rowScenario == 'C200 to ControlEdge UOC') and (scope == 'HW/SW' or scope == 'HWSWLABOR'):
            incomplete.append("C200_A_IO_Racks")


if Product.Attributes.GetByName('Incomplete'):
    Product.Attr('Incomplete').AssignValue(",".join(incomplete))