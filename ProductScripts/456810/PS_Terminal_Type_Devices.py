Element = Product.Attr('TM Elements').GetValue()
Terminal_Type_Devices = SqlHelper.GetList("select RestrictValue from TM_DEVICES_RULES where Element = '{}'".format(Element))
c= Product.Attr('Terminal_Type_Devices').Values

for v in Terminal_Type_Devices:
    for av in c:
        if av.ValueCode == v.RestrictValue:
            av.Allowed = False
            break
Product.ApplyRules()