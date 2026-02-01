laborCont = Product.GetContainerByName('Winest Labor Container')
laborRows = laborCont.Rows
prod = TagParserProduct.ParseString('<* Value(Winest Labor Productivity) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        calc = float(row.GetColumnByName('Calculated Hrs').Value)
        if calc > 0:
            row.GetColumnByName('Productivity').Value = prod
            final = calc * float(prod)
            row.GetColumnByName('Final Hrs').Value = str(round(final))
            updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
ScriptExecutor.Execute('PS_Show_Error_Deliverables')