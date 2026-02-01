ioSum = 0
containers_with_fields = {
	"SerC_RG_Enhanced_Function_IO_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],"SerC_RG_Enhanced_Function_IO_Cont2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],"C300_RG_Universal_IO_cont_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],"C300_RG_Universal_IO_cont_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"]}
containers_with_fields_mark = {"C300_CG_Universal_IO_Mark_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],"C300_CG_Universal_IO_Mark_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"]}
con_grp = Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows
for row in con_grp:
	familytype = row.GetColumnByName('IO_Family_Type').Value
	if row.Product.Attr("UOC_I/O_IsModified").GetValue() == "True":
		if familytype in ('Series C','Turbomachinery'):
			for container, fields in containers_with_fields.items():
				for field in fields:
					ioSum += int(row.Product.ParseString('<*CTX( Container("{}").Sum("{}") )*>'.format(container,field)))
		elif familytype == "Series-C Mark II":
			for container, fields in containers_with_fields.items():
				for field in fields:
					ioSum += int(row.Product.ParseString('<*CTX( Container("{}").Sum("{}") )*>'.format(container,field)))
Product.Attr('R2Q_UOC_IO_Total').AssignValue(str(int(ioSum)))