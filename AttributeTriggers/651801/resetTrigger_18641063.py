val1 = int(Product.Attr('Number of SMX System RT').GetValue())
val2 = int(Product.Attr('Number of SMX System ST').GetValue())
val3 = int(Product.Attr('Number of Years of Contract').GetValue())
if val3 < (val1 + val2):
	Product.Attr('Number of Years of Contract').AssignValue(str(val1 + val2))
if Product.Attr("R2QRequest").GetValue() == 'Yes':
    attributes = [
        "Number of SMX System RT",
        "Number of SMX System ST",
        "Number of Years of Contract",
        "USB Key ST Only"
    ]

    val = sum(int(Product.Attr(attr).GetValue() or 0) for attr in attributes)

    if val > 0:
    	Product.Attr("Required_Attribute").AssignValue("1")
    else:
        Product.ResetAttr('Required_Attribute')