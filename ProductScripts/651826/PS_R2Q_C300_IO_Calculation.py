count = "0"
total_count,ioSum = 0,0
containers_with_fields = {
"C300_CG_Universal_IO_cont_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
"C300_CG_Universal_IO_cont_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
"SerC_CG_Enhanced_Function_IO_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
"SerC_CG_Enhanced_Function_IO_Cont2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
"SerC_CG_FIM_FF_IO_Cont": ["Red_wo_C300","Non_Red_wo_C300","Red_C300","Non_Red_C300"]
}
containers_with_fields_mark = {
"C300_CG_Universal_IO_Mark_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
"C300_CG_Universal_IO_Mark_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
"C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
"C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
"SerC_CG_FIM_FF_IO_Cont": ["Red_wo_C300","Non_Red_wo_C300","Red_C300","Non_Red_C300"]
}
con_grp = Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows
for row in con_grp:
	familytype = row.GetColumnByName('SerC_CG_IO_Family_Type').Value
	if row.Product.Attr("UOC_I/O_IsModified").GetValue() == "True":
		if familytype in ('Series C','Turbomachinery'):
			for container, fields in containers_with_fields.items():
				for field in fields:
					ioSum += int(row.Product.ParseString('<*CTX( Container("{}").Sum("{}") )*>'.format(container,field)))
		elif familytype == "Series-C Mark II":
			for container, fields in containers_with_fields_mark.items():
				for field in fields:
					ioSum += int(row.Product.ParseString('<*CTX( Container("{}").Sum("{}") )*>'.format(container,field)))
		total_count = int(row.Product.Attr('R2Q_UOC_IO_Total').GetValue() or 0)+int(ioSum)
		count = "0" if total_count <=2000 else "15"
Product.Attr('Enter_total_count_of_Typicals/Prototypes (0-500)').AssignValue(count)