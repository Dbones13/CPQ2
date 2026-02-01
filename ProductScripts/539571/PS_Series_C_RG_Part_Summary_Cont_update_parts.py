import GS_SerC_Part_Calcs
if Product.Name == "Series-C Remote Group":
    if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
        Product.ApplyRules()
        Product.ParseString('<* ExecuteScript(PS_RG_label_parts) *>')
        Product.ParseString('<* ExecuteScript(PS_SerC_C300_RG_Parts) *>')
        Product.ParseString('<* ExecuteScript(PS_SerC_C300_RG_Parts_2) *>')
        Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_RG) *>')
        Product.ParseString('<* ExecuteScript(PS_mcar_part_add_RG) *>')
        Product.ParseString('<* ExecuteScript(SerC_PowerSupply_Parts) *>')
        Product.ApplyRules()
        Product.ParseString('<* ExecuteScript(PS_C300_UMC_Parts) *>')
        Product.ParseString('<* ExecuteScript(PS_C300_CNM_PartCals) *>')
        Product.ParseString('<* ExecuteScript(PS_C300_UMC_Parts) *>')
        Product.ParseString('<* ExecuteScript(PS_mcar_part_add_RG) *>')
        if Product.Attr('total_family_CG_ios_doc').GetValue() < "1" and Product.Attr('pmio_ioss').GetValue() < "1":
            Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_RG) *>')
            Product.ParseString('<* ExecuteScript(SerC_PowerSupply_Parts) *>')
            #Product.ApplyRules()

    isR2QRequest= Quote.GetCustomField("isR2QRequest").Content
    if isR2QRequest or Product.Tabs.GetByName('Part Summary').IsSelected==True:
        cont = Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
        if cont:
            for row in cont.Rows:
                update=False
                if int(row["Final_Quantity"]) > 0:
                    if row.IsSelected == False:
                        row.IsSelected = True
                        row.Calculate()
                        update=True
                    if row.Product.Attributes.GetByName('ItemQuantity'):
                        if int(row["Final_Quantity"]) !=  row.Product.Attr('ItemQuantity').GetValue():
                            row.Product.Attr('ItemQuantity').AssignValue(row["Final_Quantity"])
                            update=True
                    else:
                        Product.ErrorMessages.Add('Item Quantity missing from part number {}, please contact the Admin'.format(row.Product.PartNumber))
                    if update == True:
                        row.ApplyProductChanges
                else:
                    if row.IsSelected == True:
                        row.IsSelected = False
            cont.Calculate()
        Product.ApplyRules()
        Product.Attr('PERF_ExecuteScripts').AssignValue('')