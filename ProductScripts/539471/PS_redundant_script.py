nonredunant = Product.Attr('TPS_EX_Non_Reduntant_Conversion_ESVT').GetValue()
if nonredunant == '':
	Product.Attr('TPS_EX_Non_Reduntant_Conversion_ESVT').SelectDisplayValue('No')
elif nonredunant == 'Yes':
    Product.Attr('TPS_EX_Redundant_Conversion_ESVT').Access = AttributeAccess.Hidden
redundant = Product.Attr('TPS_EX_Redundant_Conversion_ESVT').GetValue()
if redundant == '' :
    Product.Attr('TPS_EX_Redundant_Conversion_ESVT').SelectDisplayValue('No')
elif redundant == 'Yes':
    Product.Attr('TPS_EX_Non_Reduntant_Conversion_ESVT').Access = AttributeAccess.Hidden