cabinet_type = Product.Attr('SerC_CG_Marshalling_Cabinet_Type').GetValue()
if cabinet_type == "3rd Party Marshalling":
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
else:
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')

if cabinet_type == 'Universal Marshalling':
	Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').SelectDisplayValue('Yes')
	getval = Product.Attr('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet').GetValue()
	Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').AssignValue(getval)
else:
	Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').SelectDisplayValue('No')
if cabinet_type == 'None':
	Product.Attr('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet').Access = AttributeAccess.Hidden
	Product.Attr('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet').AssignValue('0')
else:
	Product.Attr('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet').Access = AttributeAccess.Editable