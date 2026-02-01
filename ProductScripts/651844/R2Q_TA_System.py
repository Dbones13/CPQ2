category = Product.Attr('R2Q Select Category').GetValue()
if category == 'TA System':
	Product.Attr('R2Q_Project_Questions_TAS_Cont').Access = AttributeAccess.Editable
else:
	Product.Attr('R2Q_Project_Questions_TAS_Cont').Access = AttributeAccess.Hidden