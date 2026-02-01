import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from GS_AddWriteInProduct import getWriteInProductInfo, PopulateValidPartsCon
def getFloat(val):
    try:
        return float(val)
    except:
        return 0.00
def getTotalCostAndPrice():
    total_cost = total_list_price = 0
    for r in Product.GetContainerByName("Staging_and_Integration_Expense_Cont").Rows:
        total_cost = total_cost + getFloat(r['Total_Cost'])
        total_list_price = total_list_price + getFloat(r['Total_List_Price'])
    return total_cost , total_list_price
def updateWriteinData(containerRow,unitListPrice, unitRegionalCost):
    containerRow["Price"]               = str(unitListPrice)
    containerRow["Cost"]                = str(unitRegionalCost)
    containerRow.Product.ApplyRules()
    containerRow.ApplyProductChanges()
    WriteInProduct_container.Calculate()
WriteInProduct_container = Product.GetContainerByName("WriteInProduct")
rowTobeDeleted = ''
def integrationRowtobedeleted(WriteInProduct_container,rowTobeDeleted):
    for row in WriteInProduct_container.Rows:
        if row["ExtendedDescription"] == "Integration Center Costs":
            rowTobeDeleted = row.RowIndex
            break
    if rowTobeDeleted !='':
        WriteInProduct_container.DeleteRow(rowTobeDeleted)
if Product.GetContainerByName('New_exp_common_prj_input').Rows.Count>0 and Product.GetContainerByName('New_exp_common_prj_input').Rows[0].Columns['Staging_Integration Required'].Value == 'Yes':
    labor = "Write-In Integration Center"
    writeInProductInfo = getWriteInProductInfo(labor)
    #WriteInProduct_container.Rows.Clear()
    total_cost, total_list_price = getTotalCostAndPrice()
    integrationRowtobedeleted(WriteInProduct_container,rowTobeDeleted)
    PopulateValidPartsCon(Product, "Common",labor, "1", "Integration Center Costs", str(total_list_price), str(total_cost), writeInProductInfo)
    '''for row in WriteInProduct_container.Rows:
        if row["ExtendedDescription"] == "Integration Center Costs":
            updateWriteinData(row,total_list_price, total_cost)
            break
    else:
        PopulateValidPartsCon(Product, "Common",labor, "1", "Integration Center Costs", str(total_list_price), str(total_cost), writeInProductInfo)'''
else:
    integrationRowtobedeleted(WriteInProduct_container,rowTobeDeleted)