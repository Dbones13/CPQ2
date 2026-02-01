def quotefield(yspectable):
    yspec_quote = SqlHelper.GetList("SELECT DISTINCT Sub_Option FROM {}".format(yspectable))
    st_it = '<select id = "yspec_subopt"  class="form-control" style="width: 50%;"><option value="">No option selected</option>'
    for qt in yspec_quote:
        st_it +='<option value="'+ qt.Sub_Option +'">'+ qt.Sub_Option +'</option>'
    return st_it
def quotefieldexist(yspecfc,yspectable):
    yspec_quote = SqlHelper.GetList("SELECT DISTINCT Sub_Option FROM {} WHERE Yspecial_Quote = '{}'".format(yspectable,yspecfc))
    st_it = '<select id = "yspec_subopt" onchange= "addrowyspec(this)" class="form-control" style="width: 50%;"><option value="">No option selected</option>'
    for qt in yspec_quote:
        st_it +='<option value="'+ qt.Sub_Option +'">'+ qt.Sub_Option +'</option>'
    return st_it
yspecfc = Param.yspecitm
if Quote.GetCustomField('Sales Area').Content == "1109":
    yspectable = "YSpecial_US"
else:
    yspectable = "YSpecial"
sotn = '<div class="fiori3-container-label flex col-md-6" ><span class="label-range-hint-wrapper flex"><label style="display: inline-block" >Choose Yspec SubOption</label></span></div><div class="fiori3-input-group" id = "selelst">'
if yspecfc == "":
    Log.Info("yspecfc---->"+str(yspecfc))
    spec_qt = quotefield(yspectable)
    ApiResponse = ApiResponseFactory.JsonResponse(str(spec_qt))
else:
    spec_qt = quotefieldexist(yspecfc,yspectable)
    ApiResponse = ApiResponseFactory.JsonResponse(sotn+str(spec_qt)+'</div>')