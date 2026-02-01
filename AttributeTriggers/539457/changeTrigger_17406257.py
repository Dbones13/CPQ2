gesLocation = TagParserProduct.ParseString('<* Value(Virtualization_Ges_Location) *>')

if gesLocation <> "None":
    laborRows = Product.GetContainerByName('Virtualization_Additional_Custom_Deliverables').Rows
    gesPerc = Product.Attr('Virtualization_Labor_GES_Additonal_Perct').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))


#ScriptExecutor.Execute('PS_Populate_Prices')