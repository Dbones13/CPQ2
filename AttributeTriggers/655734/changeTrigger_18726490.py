Web_Portal_required=Product.Attr('Terminal_Web_Portal_required?').GetValue()
if Web_Portal_required=="Yes":
    Product.AllowAttr('Mobile_UI')
    Product.Attr('Mobile_UI').SelectValue('No')
    Product.SetRequired('Mobile_UI')
else:
    Product.DisallowAttr('Mobile_UI')
    Product.SetOptional('Mobile_UI')