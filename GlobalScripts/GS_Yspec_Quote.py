def quotefield(yspectable):
    yspec_quote = SqlHelper.GetList("SELECT DISTINCT Yspecial_Quote FROM {} WHERE Part_Number = '{}'".format(yspectable,Product.PartNumber))
    if yspec_quote:
        st_it = '<select id="yspec_quote_input"  onChange="subopt()"><option value="none" selected disabled hidden>Select an Option</option>'
        for qt in yspec_quote:
            st_it +='<option value="'+ qt.Yspecial_Quote +'">'+ qt.Yspecial_Quote +'</option>'
    	return st_it
    else:
    	#yspec_quote = SqlHelper.GetList("SELECT DISTINCT Yspecial_Quote FROM {}".format(yspectable))
    	st_it = '<select id="yspec_quote_input"  onChange="subopt()"><option value="none" selected disabled hidden>Select an Option</option>'
    	#for qt in yspec_quote:
        	#st_it +='<option value="'+ qt.Yspecial_Quote +'">'+ qt.Yspecial_Quote +'</option>'
    	return st_it
def quotefieldexist(yspecfc,yspectable):
    yspec_quote = SqlHelper.GetList("SELECT DISTINCT Yspecial_Quote FROM {} WHERE Yspecial_Quote != '{}' AND Part_Number = '{}'".format(yspectable,yspecfc,Product.PartNumber))
    if yspec_quote:
    	st_it = '<select id="yspec_quote_input"  onChange="subopt()"><option value="none" selected disabled hidden>Select an Option</option><option value="'+ yspecfc +'">'+ yspecfc +'</option>'
    	for qt in yspec_quote:
        	st_it +='<option value="'+ qt.Yspecial_Quote +'">'+ qt.Yspecial_Quote +'</option>'
    	return st_it
    else:
    	#yspec_quote = SqlHelper.GetList("SELECT DISTINCT Yspecial_Quote FROM {} WHERE Yspecial_Quote != '{}'".format(yspectable,yspecfc))
    	st_it = '<select id="yspec_quote_input"  onChange="subopt()"><option value="none" selected disabled hidden>Select an Option</option><option value="'+ yspecfc +'">'+ yspecfc +'</option>'
    	#for qt in yspec_quote:
        	#st_it +='<option value="'+ qt.Yspecial_Quote +'">'+ qt.Yspecial_Quote +'</option>'
    	return st_it
yspecfc = Param.yspecitm
if Quote and Quote.GetCustomField('Sales Area').Content == "1109":
    yspectable = "YSpecial_US"
else:
    yspectable = "YSpecial"
if yspecfc == "":
    Trace.Write("yspecfc---->"+str(yspecfc))
    spec_qt = quotefield(yspectable)
    ApiResponse = ApiResponseFactory.JsonResponse(str(spec_qt))
else:
    spec_qt = quotefieldexist(yspecfc,yspectable)
    ApiResponse = ApiResponseFactory.JsonResponse(str(spec_qt))