#Attribute 'Additional_CustomDev_GES %' Change Trigger 
#Populate each selected container row with the 'GES Eng % Split' value

gesLocation = TagParserProduct.ParseString('Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()')
updateFlag = 0
if gesLocation <> "None":
    laborRows = Product.GetContainerByName('Additional_CustomDev_Labour_Container').Rows
    gesPerc = Product.Attr('Additional_CustomDev_GES').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('Show_Experion_Ent_Sys_Error_Deliverables')