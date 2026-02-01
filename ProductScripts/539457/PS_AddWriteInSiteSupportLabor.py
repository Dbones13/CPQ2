from GS_AddWriteInProduct import getWriteInProductInfo, PopulateValidPartsCon

labor = "Write-in Third Party Hardware & Software"
mapping_dict = {"Integrated Automation Assessment Non SESP + SPB":"IAA & SPB for Non-SESP MSIDs", "Integrated Automation Assessment SESP Plus + SPB":"IAA & SPB for SESP Plus MSIDs", "Integrated Automation Assessment SESP Flex + SPB":"IAA & SPB for SESP Flex MSIDs"}

writeInProductInfo = getWriteInProductInfo(labor)
pricing_container = Product.GetContainerByName("Virtualization_Third_party_items")
#pricing_container_list = Product.GetContainerByName("Virtualization_Third_party_items").Rows.ToList()
WriteInProduct_container = Product.GetContainerByName("WriteInProduct")
WriteInProduct_container.Rows.Clear()
#Product.Attr('Product_Message').AssignValue('')
for row in pricing_container.Rows:
    if float(row['Price'] if row['Price'] != '' else 0 ) > 0  and float(row['Cost'] if row['Cost'] != '' else 0) > 0:
        PopulateValidPartsCon(Product, "LSS",labor, "1", row['Extended Description'], str(row['Price']), str(row['Cost']), writeInProductInfo)
    if (float(row['Price'] if row['Price'] != '' else 0 ) > 0 and float(row['Cost'] if row['Cost'] != '' else 0) == 0) or (float(row['Cost'] if row['Cost'] != '' else 0 ) > 0 and float(row['Price'] if row['Price'] != '' else 0) == 0):
        #Product.Attr('Product_Message').AssignValue('When there is price entered then cost also need to be entered and vice versa.')
        pass