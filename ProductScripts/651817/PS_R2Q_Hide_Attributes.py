#to hide the container columns and set default values

from GS_R2Q_SafetyManagerContainerColumns import UOCContainerColumns as uoc

def hideContainerColumns():
	for contColumn in uoc.nonR2QContColumn:
		for col in uoc.nonR2QContColumn[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def set_defaultVal(cont_name, col_list):
	UOC_CG_rows = Product.GetContainerByName(cont_name).Rows
	if UOC_CG_rows.Count > 0:
		UOC_CG_cont = UOC_CG_rows[0]
		for key,value in col_list.items():
			UOC_CG_cont.GetColumnByName(key).Value = value

#nonR2QContColumn = {"UOC_Common_Questions_Cont":["UOC_Shielded_Terminal_Strip","UOC_IO_Filler_Module","UOC_Cluster","UOC_Starter_Kit","UOC_Starter_ Kit_with_Experion_License"],"UOC_Labor_Details":["UOC_Impl_Method_Labour","UOC_Ges_Location_Labour","UOC_Marshalling_Cabinet_Cont_Labour","UOC_Num_Peer_PCDI_Labour","UOC_Num_Peer_CDA_Labour","UOC_Num_Peer_to_Peer","UOC_Enter_Total_Count_Labour","UOC_Num_New_Typicals","UOC_Num_SCADA_Node_Type","UOC_Num_Complex_Loops_Labour","UOC_Num_ProfiNet_Devices_Labour","UOC_Num_ProfiNet_Devices_IO_Labour","UOC_Num_EtherNet_Devices_Labour","UOC_Num_EtherNet_Devices_IO_Labour","UOC_Input_Quality_Specific_Labour","UOC_Num_Complex_SCMs_Per_Unit_Labour","UOC_Num_Complex_Operations_Per_Product_Labour","UOC_Percentage_Pre_FAT"]}

col_list = {"UOC_Impl_Method_Labour":"Standard Build Estimate","UOC_Input_Quality_Specific_Labour":"Function Plan available(One revision) 40 %","UOC_Num_Complex_SCMs_Per_Unit_Labour":"1","UOC_Marshalling_Cabinet_Cont_Labour":"0","UOC_Num_Complex_Operations_Per_Product_Labour":"1","UOC_Ges_Location_Labour":Product.Attr('MSID_GES_Location').GetValue(),"UOC_Num_SCADA_Node_Type":"0","UOC_Num_ThirdParty_SoftIO":"0"}

set_defaultVal("UOC_Labor_Details", col_list)
hideContainerColumns()

UOC_controlgrpRows = Product.GetContainerByName('Number_UOC_Control_Groups').Rows
if UOC_controlgrpRows.Count > 0:
	UOC_controlgrp = UOC_controlgrpRows[0]
	UOC_controlgrp.GetColumnByName('Number_UOC_Control_Groups').HeaderLabel = "Number of CE UOC Control Groups (1-10)"


loc_dict = {"IN":"GESIndia","CN":"GESChina","RO":"GESRomania","UZ":"GESUzbekistan","None":"None","null":"None"}
ges_loc = Quote.GetGlobal('ExGesLocation')
ges_location = loc_dict.get(ges_loc)
cont = Product.GetContainerByName('UOC_Labor_Details')
if cont.Rows.Count > 0:
	for conrow in cont.Rows:
		conrow['UOC_Ges_Location_Labour'] = ges_location
		Product.GetContainerByName('UOC_Labor_Details').Rows[0].SetColumnValue('UOC_Ges_Location_Labour',str(ges_location))
		#conrow.GetColumnByName('UOC_Ges_Location_Labour').SetAttributeValue(str(ges_location))
#Session["curr_ges_loc"] = ""