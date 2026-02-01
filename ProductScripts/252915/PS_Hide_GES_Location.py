if Product.Attr('MIgration_Scope_Choices').GetValue()=='HW/SW':
    Product.Attr('MSID_GES_Location').Allowed=False

else:
      Product.Attr('MSID_GES_Location').Allowed=True