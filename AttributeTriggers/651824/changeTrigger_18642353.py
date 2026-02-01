cabinet_type = Product.Attr('SerC_RG_Marshalling_Cabinet_Type').GetValue()
if cabinet_type in ('3rd Party Marshalling','None'):
	if cabinet_type == 'None':
		Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').Access = AttributeAccess.Hidden
		Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').AssignValue('0')
	Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').SelectDisplayValue('No')
else:
	Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').SelectDisplayValue('Yes')
	Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').Access = AttributeAccess.Editable

if cabinet_type == "3rd Party Marshalling":
	Product.ParseString('<*CTX( Container(SerC_RG_Enhanced_Function_IO_Cont2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(SerC_RG_Enhanced_Function_IO_Cont2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_RG_Universal_IO_cont_2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_RG_Universal_IO_cont_2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').Access = AttributeAccess.Editable
else:
	Product.ParseString('<*CTX( Container(SerC_RG_Enhanced_Function_IO_Cont2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SerC_RG_Enhanced_Function_IO_Cont2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_RG_Universal_IO_cont_2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_RG_Universal_IO_cont_2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')