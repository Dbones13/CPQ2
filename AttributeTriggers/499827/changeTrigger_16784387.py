gesLocation = gesLocation = TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Row(1).Column(GES_Location).GetDisplayValue )*>')
if gesLocation <> "None":
    laborCont = Product.GetContainerByName('PM_Additional_Custom_Deliverables_Labor_Container')
    gesPerc = Product.Attr('Project_Additinoal_GES_%').GetValue()
    for row in laborCont.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            row.Calculate()
ScriptExecutor.Execute('PS_Refresh_Custom_Deliverables_Labor_Container')