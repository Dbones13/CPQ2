def container_dict(row,container_name):

	container_name_dict = {}
	con = row.Product.GetContainerByName(container_name)

	for col in con.Rows:

		for i in col.Columns:

			if i.Name in container_name_dict:
				val = i.Value if i.Value else 0
				container_name_dict[i.Name] = container_name_dict[i.Name]+int(val)
				
			else:
				container_name_dict[i.Name] = int(i.Value) if i.Value else 0

	return container_name_dict

def combined_dict(CG_Dict,RG_Dict):

	combined_dict = {}

	for d in [CG_Dict, RG_Dict]:
		for k, v in d.items():
			combined_dict[k] = combined_dict.get(k, 0) + v

	return combined_dict

def control_remote_dict(U_Io_dict,I_Io_dict):

	control_remote_dict = {}

	for d in [U_Io_dict, I_Io_dict]:
		control_remote_dict.update(d)

	if 'PLC_Communication_Interface_Mod_485232' in control_remote_dict:
		del control_remote_dict['PLC_Communication_Interface_Mod_485232']

	return control_remote_dict

def Io_Type_Cnt(Product):
	
	final_dict = {}
	control_remote_dict_list = []

	CG_container = Product.GetContainerByName('PLC_ControlGroup_Cont')
	
	for cg_row in CG_container.Rows:

		# Get control group IOs
		PLC_CG_UIO_Cont = container_dict(cg_row,'PLC_CG_UIO_Cont')
		PLC_CG_Other_IO_Cont = container_dict(cg_row,'PLC_CG_Other_IO_Cont')

		# --- Initialize empty Remote Group totals ---
		PLC_RG_UIO_total = {}
		PLC_RG_Other_total = {}

		# --- Only loop if RG_container has rows ---
		if cg_row.Product.GetContainerByName('PLC_RemoteGroup_Cont').Rows.Count > 0:
			for rg_row in cg_row.Product.GetContainerByName('PLC_RemoteGroup_Cont').Rows:
				PLC_RG_UIO_Cont = container_dict(rg_row,'PLC_RG_UIO_Cont')
				PLC_RG_Other_IO_Cont = container_dict(rg_row,'PLC_RG_Other_IO_Cont')

				PLC_RG_UIO_total = combined_dict(PLC_RG_UIO_total, PLC_RG_UIO_Cont)
				PLC_RG_Other_total = combined_dict(PLC_RG_Other_total, PLC_RG_Other_IO_Cont)
		
		# Merge Control & Remote I/O dicts    
		Universal_Io_dict = combined_dict(PLC_CG_UIO_Cont,PLC_RG_UIO_total)
		Individual_Io_dict = combined_dict(PLC_CG_Other_IO_Cont,PLC_RG_Other_total)

		# Get combined dict for this CG row
		ctrl_remote_dict = control_remote_dict(Universal_Io_dict,Individual_Io_dict)

		# Store in list
		control_remote_dict_list.append(ctrl_remote_dict)

	# Combine all CG-level dicts into one final dict    
	for d in control_remote_dict_list:
		for k, v in d.items():
			final_dict[k] = final_dict.get(k, 0) + v
			
	Trace.Write("final_dict----->"+str(final_dict))

	# Count keys where value > 0        
	cnt = len([v for v in final_dict.values() if v > 0])

	return cnt

Io_type_cnt = Io_Type_Cnt(Product)
Product.Attr('Number of Total IO Types').AssignValue(str(Io_type_cnt))