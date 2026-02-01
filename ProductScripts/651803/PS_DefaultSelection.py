if Session['Scope'] == 'HW/SW/LABOR':
    Product.Attr('Onsite Support Implementation Services').SelectDisplayValue('Yes')
if Session['Scope'] == 'HW/SW':
    if Product.Attr('Onsite Support Implementation Services').GetValue() == '':
        Product.DisallowAttr('Empty Section for MSS')
        Product.DisallowAttr('Execution Country')
        '''Product.DisallowAttr('FAT Document Verification and Execution')
        Product.DisallowAttr('FDS & DDS Documentation Required')
        Product.DisallowAttr('SAT Document Verification and Execution')'''
        Product.Attr('FDS & DDS Documentation Required').Access = AttributeAccess.Hidden
        Product.Attr('FAT Document Verification and Execution').Access = AttributeAccess.Hidden
        Product.Attr('SAT Document Verification and Execution').Access = AttributeAccess.Hidden
        Product.GetContainerByName('Activities').Rows.Clear()
        Product.DisallowAttr('Activities')