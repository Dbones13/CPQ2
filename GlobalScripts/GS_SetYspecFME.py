fmeinput = Param.fmeinput
sfmeinput = Param.sfmeinput
Trace.Write('sfmeinput:'+str(sfmeinput))
if Quote and sfmeinput!='':
    Quote.SetGlobal('gv_short_fme',sfmeinput.upper())
elif Quote:
    Quote.SetGlobal('gv_short_fme','')
ySpecOption=''
Trace.Write('sfmeinput'+ str(sfmeinput))
if Quote and fmeinput!='':
    Trace.Write('gv_short_fme'+str(str(Quote.GetGlobal('gv_short_fme'))))
    for i in Product.Attributes:
        if i.SystemId == "V_SPECIAL_OPTIONS":
            for ySpecValue in Product.Attributes.GetBySystemId("V_SPECIAL_OPTIONS").SelectedValues:
                ySpecOption=ySpecValue.ValueCode
                if ySpecOption == 'Y':
                    Product.Attributes.GetBySystemId("V_SPECIAL_OPTIONS").SelectValue("Y")
                    if fmeinput[0].upper() == "Y":
                        Quote.SetGlobal('Yspec_Fme', fmeinput.upper())
                    else:
                        Quote.SetGlobal('Yspec_Fme', 'Y' + fmeinput.upper())
                else:
                    if str(Quote.GetGlobal('Yspec_Fme')) != "":
                        Quote.SetGlobal('Yspec_Fme', '')