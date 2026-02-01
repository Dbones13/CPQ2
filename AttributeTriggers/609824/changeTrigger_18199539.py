validPartsCon = Product.GetContainerByName("HPS_PU_Valid_Parts")
if validPartsCon:
    if Product.Attr('HPS_PU_SelectValidParts').SelectedValue:
        validPartsCon.MakeAllRowsSelected()
    else:
        for row in validPartsCon.Rows:
            row.IsSelected = False
    validPartsCon.Calculate()