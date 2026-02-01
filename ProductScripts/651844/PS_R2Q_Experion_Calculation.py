import math
from GS_R2Q_Product_Attribute_ContColms import ExperionCalculationAttributesContainerColumns as CLM

def c300_iosum(cont,row):
	total = 0
	for container, fields in cont.items():
		for field in fields:
			total += int(row.Product.ParseString('<*CTX( Container("{}").Sum("{}") )*>'.format(container,field)))
	return total
def sum_UOCIO(cont,row):
	total = 0
	if row.Product.GetContainerByName(cont):
		for row in row.Product.GetContainerByName(cont).Rows:
			for val in row.Columns:
				total += int(val.Value or 0)
	return total
def sum_SMgroup(cont,col,row):
	total = 0
	if not isinstance(col, list):
		col = [col]
	if row.Product.GetContainerByName(cont):
		for row in row.Product.GetContainerByName(cont).Rows:
			total += sum(int(row[ccol] if row[ccol].isdigit() else 0 or 0) for ccol in col)
	return total

def process_containers(rows, control_group_container=None, remote_group_container=None, control_group_data=None, remote_group_data=None, sumfunc=None):
	total = 0
	for group_row in rows.Product.GetContainerByName(control_group_container).Rows:
		for cont,col in control_group_data.items():
			total += sumfunc(cont,col, group_row)

		if remote_group_container and group_row.Product.GetContainerByName(remote_group_container):
			for remote_row in group_row.Product.GetContainerByName(remote_group_container).Rows:
				for cont,col in remote_group_data.items():
					total += sumfunc(cont,col, remote_row)
	return total
def process_iofamily(cnrows,cont_fields='',cont_fields_mark=''):
	total = 0
	iofamily = cnrows.Product.Attr("SerC_CG_IO_Family_Type").GetValue()
	if iofamily in ("Series C","Turbomachinery"):
		total += c300_iosum(cont_fields,cnrows)
	elif iofamily == "Series-C Mark II":
		total += c300_iosum(cont_fields_mark,cnrows)
	return total

ioSum = 0
cn_cont_with_fields = CLM.cn_cont_with_fields
cn_cont_with_fields_mark = CLM.cn_cont_with_fields_mark
rm_cont_with_fields = CLM.rm_cont_with_fields
rm_cont_with_fields_mark = CLM.rm_cont_with_fields_mark
con_UOC = CLM.con_UOC
rem_UOC = CLM.rem_UOC
con_SM = CLM.con_SM
rem_SM = CLM.rem_SM
scada_cont = CLM.scada_cont

container = Product.GetContainerByName('R2Q CE_System_Cont')
for rows in container.Rows:
	if rows['Selected_Products'] ==  'R2Q C300 System':
		controlgrp_cont = rows.Product.GetContainerByName('Series_C_Control_Groups_Cont')
		for cnrows in controlgrp_cont.Rows:
			remotegrp_cont = cnrows.Product.GetContainerByName('Series_C_remote_Groups_Cont')
			ioSum += process_iofamily(cnrows,cont_fields=cn_cont_with_fields,cont_fields_mark=cn_cont_with_fields_mark)
			if remotegrp_cont:
				for rmrows in remotegrp_cont.Rows:
					ioSum += process_iofamily(rmrows,cont_fields=rm_cont_with_fields,cont_fields_mark=rm_cont_with_fields_mark)

	if rows['Selected_Products'] ==  'R2Q ControlEdge UOC System':
		for uoc_cnrows in rows.Product.GetContainerByName('UOC_ControlGroup_Cont').Rows:
			for cont in con_UOC:
				ioSum += sum_UOCIO(cont,uoc_cnrows)
			if uoc_cnrows.Product.GetContainerByName('UOC_RemoteGroup_Cont'):
				for uoc_rmrows in uoc_cnrows.Product.GetContainerByName('UOC_RemoteGroup_Cont').Rows:
					for cont in rem_UOC:
						ioSum += sum_UOCIO(cont,uoc_rmrows)
	if rows['Selected_Products'] in ('R2Q Safety Manager ESD','R2Q Safety Manager FGS'):
		ioSum += process_containers(
			rows=rows,
			control_group_container='SM_ControlGroup_Cont',
			remote_group_container='SM_RemoteGroup_Cont',
			control_group_data=con_SM,
			remote_group_data=rem_SM,
			sumfunc=sum_SMgroup
		)
	if rows['Selected_Products'] == "R2Q 3rd Party Devices/Systems Interface (SCADA)":
		ioSum += process_containers(
			rows=rows,
			control_group_container='Scada_CCR_Unit_Cont',
			control_group_data=scada_cont,
			sumfunc=sum_SMgroup
		)
no_dispalys = math.ceil(ioSum/35.0)
Quote.SetGlobal('total_display',str(no_dispalys))
for rows in container.Rows:
	if rows['Selected_Products'] ==  'R2Q Experion Enterprise System':
		exp_dict = {'Total Number of Displays':no_dispalys}
		for attr,val in exp_dict.items():
			rows.Product.Attr(attr).AssignValue(str(val))
#Log.Info("number of displays " +str(no_dispalys)+" global="+str(Quote.GetGlobal('total_display')))