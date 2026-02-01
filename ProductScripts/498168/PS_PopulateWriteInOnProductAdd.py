import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from GS_AddWriteInProduct import getWriteInProductInfo, PopulateValidPartsCon
def getTotalCostAndPrice():
    groups_count=Product.Attr('TL_Number_of_Travel_Expense_Groups').GetValue()
    groups_count=int(groups_count)
    total_cost = total_list_price = 0
    for i in range(groups_count):
        if Product.GetContainerByName('TL_Expense_Calculation_Cont_'+str(i+1)):
            total_cost = total_cost + float(Product.GetContainerByName('TL_Expense_Calculation_Cont_'+str(i+1)).TotalRow.Columns['Total_Cost'].Value)
            total_list_price = total_list_price + float(Product.GetContainerByName('TL_Expense_Calculation_Cont_'+str(i+1)).TotalRow.Columns['Total_List_Price'].Value)
    return total_cost , total_list_price

labor = "Write-In Travel and Living"

writeInProductInfo = getWriteInProductInfo(labor)
WriteInProduct_container = Product.GetContainerByName("WriteInProduct")
WriteInProduct_container.Rows.Clear()
total_cost, total_list_price = getTotalCostAndPrice()
#Product.Attr('Product_Message').AssignValue('')
if total_cost > 0:
    PopulateValidPartsCon(Product, "Common",labor, "1", "Travel and Living", str(total_list_price), str(total_cost), writeInProductInfo)