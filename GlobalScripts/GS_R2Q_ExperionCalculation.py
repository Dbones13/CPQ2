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
	if row.Product.GetContainerByName(cont):
		for row in row.Product.GetContainerByName(cont).Rows:
			total += int(row[col] or 0)
	return total
def sum_modbus(cont,col,row):
	modbus = opc = 0
	if row.Product.GetContainerByName(cont):
		for row in row.Product.GetContainerByName(cont).Rows:
			if row["Third_Party_Devices_Systems_Interface_SCADA"] in ["Modbus TCP/IP (0-50)","Modbus RTU (0-50)","Modbus Plus, ASCII (0-50)","Enron Modbus Interface (0-50)"]:
				modbus += int(row[col] or 0)
			else:
				opc += int(row[col] or 0)
	return modbus,opc
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

def calculate_profibus_incards(cnrows):
	profibus_nonred = int(cnrows.Product.Attr("SerC_Number_of_Profibus_DP_Slave_devices - Non_Red").GetValue() or 0)
	profibus_red = int(cnrows.Product.Attr("SerC_Number_of_Profibus_DP_Slave_devices - Red").GetValue() or 0)
	profibus_devices = int(cnrows.Product.Attr("SerC_Number_of_Devices_per_Profibus_Network (0-32)").GetValue() or 0)

	if profibus_devices > 0:
		profibus_incards = (((profibus_nonred + profibus_devices - 1) / profibus_devices) + 2 - 1) / 2
		profibus_incards += 2 * (((profibus_red + profibus_devices - 1) / profibus_devices) + 2 - 1) / 2
		return profibus_incards
	return 0


ioSum = FIM_count = Profibus_count = ethernet_count = modbus_count = opc_count = servercount =profibus_incards = ethernet_incards= red_count = nonred_count = sum_switch = 0
fim_required = profibus_required = ethernet_required = "No"
cn_cont_with_fields = CLM.cn_cont_with_fields
cn_cont_with_fields_mark = CLM.cn_cont_with_fields_mark
Fim_cont = CLM.Fim_cont
rm_cont_with_fields = CLM.rm_cont_with_fields
rm_cont_with_fields_mark = CLM.rm_cont_with_fields_mark
con_UOC = CLM.con_UOC
rem_UOC = CLM.rem_UOC
con_SM = CLM.con_SM
rem_SM = CLM.rem_SM
scada_cont = CLM.scada_cont
selected_products = CLM.selected_products
red_attr = CLM.red_attr
nonRed_attr =CLM.nonRed_attr
container = Product.GetContainerByName('R2Q CE_System_Cont')
for rows in container.Rows:
	if rows['Selected_Products'] in selected_products:
		servercount += 1
	if rows['Selected_Products'] ==  'R2Q C300 System':
		controlgrp_cont = rows.Product.GetContainerByName('Series_C_Control_Groups_Cont')
		for cnrows in controlgrp_cont.Rows:
			fim_required = cnrows.Product.Attr("SerC_CG_Foundation_Fieldbus_Interface_required").GetValue()
			profibus_required = cnrows.Product.Attr("SerC_GC_Profibus_Gateway_Interface").GetValue()
			ethernet_required = cnrows.Product.Attr("SerC_CG_Ethernet_Interface").GetValue()
			remotegrp_cont = cnrows.Product.GetContainerByName('Series_C_remote_Groups_Cont')
			ioSum += process_iofamily(cnrows,cont_fields=cn_cont_with_fields,cont_fields_mark=cn_cont_with_fields_mark)
			if remotegrp_cont:
				for rmrows in remotegrp_cont.Rows:
					ioSum += process_iofamily(rmrows,cont_fields=rm_cont_with_fields,cont_fields_mark=rm_cont_with_fields_mark)

			Profibus_count = sum(int(cnrows.Product.Attr(attr).GetValue() or 0)
				for attr in ["SerC_Number_of_Profibus_DP_Slave_devices - Non_Red", "SerC_Number_of_Profibus_DP_Slave_devices - Red"])
			ethernet_count = sum(int(cnrows.Product.Attr(attr).GetValue() or 0)
				for attr in ["SerC_Number_of_Rockwell_ControlLogix_Processors", "SerC_Number of Process Connected I/O Devices 1", "SerC_NO of Rock Ctrl Processors Redundant0-999NEW", "SerC_Nu of Proc Conn I/O Devi (Redundant ) (0-999)"])
			FIM_count = c300_iosum(Fim_cont,cnrows)
			
			for at in red_attr:
				red_count += int(cnrows.Product.Attr(at).GetValue() or 0)
			for at in nonRed_attr:
				nonred_count += int(cnrows.Product.Attr(at).GetValue() or 0)
			ethernet_incards=2*red_count+nonred_count
			profibus_incards = calculate_profibus_incards(cnrows)
			
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
		for scada_cnrows in rows.Product.GetContainerByName('Scada_CCR_Unit_Cont').Rows:
			modbus_count, opc_count = sum_modbus("Modbus/OPC Interfaces","SCADA Points",scada_cnrows)

no_dispalys = math.ceil(ioSum/35)
if ioSum < 1000:
	prj_duration = "17"
	fat_duration = "2"
elif ioSum < 2500:
	prj_duration = "28"
	fat_duration = "3"
elif ioSum < 4000:
	prj_duration = "38"
	fat_duration = "4"
else:
	prj_duration = "52"
	fat_duration = "5"

modbus_required = "Yes" if modbus_count > 0 else "No"
opc_required = "Yes" if opc_count > 0 else "No"

new_exp_dict = {'Is Fieldbus Interface in Scope?':fim_required,'Is Profibus Interface in Scope?':profibus_required,'Is EtherNet IP Interface in Scope?':ethernet_required, 'Is Modbus Interface in Scope?':modbus_required,'Is OPC Interface in Scope?':opc_required,'Estimated Project Value (Cost)':"$1M - $5M",'Labor_Loop_Drawings':"Yes",'Labor_Marshalling_Database':"Yes",'FAT Duration in weeks':fat_duration,'Project Duration (in weeks)':prj_duration}
for attr,val in new_exp_dict.items():
	Product.Attr(attr).SelectDisplayValue(val) if Product.Attr(attr).DisplayType == "DropDown" else Product.Attr(attr).AssignValue(val)
stations = ['CMS Flex Station Qty 0_60', 'DMS Flex Station Qty 0_60', 'Flex Station Qty (0-60)', 'Additional Stations']
ebr = ['Experion Backup & Restore (Experion Server)', 'Experion Backup & Restore (Flex Station ES-F)']
flexqty = ['CMS Flex Station Qty 0_60', 'DMS Flex Station Qty 0_60', 'Flex Station Qty (0-60)']
sum_station = sum_server = 0
for rows in container.Rows:
	if rows['Selected_Products'] ==  'R2Q Experion Enterprise System':
		for exp_cnrows in rows.Product.GetContainerByName('Experion_Enterprise_Cont').Rows:
			sum_switch += (
			(1 if exp_cnrows.Product.Attr('L2 Switch Required').GetValue() == "Yes" else 0)
			+ servercount
			+ (1 if any(
				str(exp_cnrows.Product.Attr(attr).GetValue()).isdigit() and int(exp_cnrows.Product.Attr(attr).GetValue()) > 0
				for attr in flexqty) else 0))
			for att in stations:
				sum_station += int(exp_cnrows.Product.Attr(att).GetValue() or 0)
			for att in ebr:
				sum_server += 1 if exp_cnrows.Product.Attr(att).GetValue() == "Yes" else 0
			sum_server += 2 if exp_cnrows.Product.Attr("Server Redundancy Requirement?").GetValue() == "Redundant" else 1
			sum_server += int(exp_cnrows.Product.Attr("Additional Servers").GetValue() or 0)
		consolesection = sum_station + sum_server

		exp_dict = {'Number of Operator Console Sections':consolesection,'Number of Server Types':servercount,'Number of Types of Network Devices':sum_switch,'Total Number of Displays':no_dispalys,'Number of Modbus Interfaces':modbus_count,'Number of OPC Interfaces':opc_count,'Number of Fieldbus Devices':FIM_count,'Number of Profibus Devices':Profibus_count,'Number of EtherNet IP Devices':ethernet_count,'Number of EtherNet IP Interface Cards':ethernet_incards,'Number of Profibus Interface Cards':profibus_incards,'Number of FTE Communities': '1','Number of FTE Community Locations': '1','Number of Locations with FTE Switches': '1','Number of Modbus Interfaces Types': '1', 'Number of Profibus Interface Types': '1','Number of EtherNet IP Interface Types': '1','Number of OPC Interface Types': '1'}
		for attr,val in exp_dict.items():
			rows.Product.Attr(attr).AssignValue(str(val))
Quote.SetGlobal('PerformanceUpload', "Yes")