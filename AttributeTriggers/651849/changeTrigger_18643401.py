if Product.Attr('FDM Client Stations required').GetValue() == 'No':
    Product.Attr('FDM Client Station Qty (0-10)').Access = AttributeAccess.Hidden
    Product.Attr('FDM Client Station Qty (0-10)').AssignValue('0')
else:
    Product.Attr('FDM Client Station Qty (0-10)').Access = AttributeAccess.Editable