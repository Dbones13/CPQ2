#if Product.Name == "Series-C Control Group":
if (Product.Tabs.GetByName('Part Summary') and Product.Tabs.GetByName('Part Summary').IsSelected==True) or Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
    Trace.Write("PERF_ExecuteScripts----")
    Product.ApplyRules()
    Product.ParseString('<* ExecuteScript(PS_SerC_C300_CG_Parts) *>')
    Product.ParseString('<* ExecuteScript(PS_UMC_parts) *>')
    Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_CG) *>')
    Product.ParseString('<* ExecuteScript(PS_SerC_C300_CG_Parts_2) *>')
    Product.ParseString('<* ExecuteScript(PS_UMC_parts) *>')
    Product.ParseString('<* ExecuteScript(SerC_CG_PowerSupply_Parts) *>')
    Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG) *>')
    Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG2) *>')
    Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_CG) *>')
    Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG) *>')
    Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG2) *>')
    Product.ApplyRules()
    if Product.Attr('total_family_CG_ios_doc').GetValue() < "1" and Product.Attr('pmio_ioss').GetValue() < "1":
        Trace.Write("less")
        Product.ParseString('<* ExecuteScript(PS_SerC_C300_CG_Parts) *>')
        Product.ParseString('<* ExecuteScript(PS_UMC_parts) *>')
        Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_CG) *>')
        Product.ParseString('<* ExecuteScript(PS_SerC_C300_CG_Parts_2) *>')
        Product.ParseString('<* ExecuteScript(PS_UMC_parts) *>')
        Product.ParseString('<* ExecuteScript(SerC_CG_PowerSupply_Parts) *>')
        Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG) *>')
        Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG2) *>')
        #Product.ParseString('<* ExecuteScript(SerC_CG_PowerSupply_Parts) *>')
        Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_CG) *>')
        Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG) *>')
        Product.ParseString('<* ExecuteScript(PS_mcar_part_add_CG2) *>')

	Product.Attr('PERF_ExecuteScripts').AssignValue('')
    cont = Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
    if cont:
        if cont.Rows.Count > 0:
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

import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)