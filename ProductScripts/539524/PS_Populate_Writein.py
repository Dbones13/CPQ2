#import clr
import System
#clr.AddReference("System.Core")
#clr.ImportExtensions(System.Linq)
from GS_AddWriteInProduct import getWriteInProductInfo, PopulateValidPartsCon

labor = "Write-In Site Support Labor"

writeInProductInfo = getWriteInProductInfo(labor)
third_part_container = Product.GetContainerByName("SCADA_CG_Part_Summary_Cont_3rd_Party")
WriteInProduct_container = Product.GetContainerByName("WriteInProduct")
WriteInProduct_container.Rows.Clear()
for row in third_part_container.Rows:
    if float(row['Unit_Price'] if row['Unit_Price'] != '' else 0 ) > 0  and float(row['Unit_Cost'] if row['Unit_Cost'] != '' else 0) > 0:
        PopulateValidPartsCon(Product, "PAS",row['PartNumber'], str(row['Final_Quantity']), row['Part_Description'], str(float(row['Unit_Price'])), str(float(row['Unit_Cost'])), writeInProductInfo)