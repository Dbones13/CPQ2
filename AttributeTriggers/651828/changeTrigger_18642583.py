EBR_Experion = Product.Attr('Experion Backup & Restore (Experion Server)').GetValue()
EBR_flex = Product.Attr('Experion Backup & Restore (Flex Station ES-F)').GetValue()
if EBR_Experion == 'Yes' or EBR_flex == 'Yes':
    Product.AllowAttr('Server Node Type EBR')
    Product.AllowAttr('EBR Server')
    #Product.Attr('Server Node Type EBR').SelectDisplayValue('SVR_STD_DELL_Tower_RAID1')
else:
    Product.DisallowAttr('Server Node Type EBR')
    Product.DisallowAttr('EBR Server')