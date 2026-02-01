'''err_msg = ""
license_periond = TagParserProduct.ParseString('<* Value(SC_License_period_Year) *>')
if license_periond == "None":
    err_msg = "License period should be mandatory in case of term Base."
Product.Attr('Error_Message').AssignValue(err_msg)'''