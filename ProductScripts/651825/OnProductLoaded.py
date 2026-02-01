import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)
Product.Attr('SerC_CG_IO_Family_Type').SelectDisplayValue('Series C')
Product.Attr('SerC_CG_Type_of_Controller_Required').SelectValue('CN100 I/O HIVE - C300 CEE')
family_ty = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
UIO_Cont1 = Product.GetContainerByName("C300_CG_Universal_IO_cont_1")
UIO_Cont2 = Product.GetContainerByName("C300_CG_Universal_IO_cont_2")
EnhancedIO_Cont1 = Product.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont")
EnhancedIO_Cont2 = Product.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont2")
UIO_Mark1 = Product.GetContainerByName("C300_CG_Universal_IO_Mark_1")
UIO_Mark2 = Product.GetContainerByName("C300_CG_Universal_IO_Mark_2")
EnhancedIO_Mark1 = Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont")
EnhancedIO_Mark2 = Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1")
TurboM_Cont = Product.GetContainerByName("C300_TurboM_IOM_CG_Cont")
Fim_Cont = Product.GetContainerByName("SerC_CG_FIM_FF_IO_Cont")

Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').AssignValue('0')
Product.Attr('Number_of_Series_C_Remote_Groups').AssignValue('0')
Product.Attr('CE_Site_Voltage').AssignValue("120V")
Product.Attr("FIM_FF_IOs_with_Power_conditioner").SelectDisplayValue("No")
Product.Attr("FIM_Type").SelectDisplayValue("FIM8")
Product.Attr("FIM_Power_Conditioner_Scope").SelectDisplayValue("Honeywell")

Universal_Enhanc_contattr = ["Header_03_close","Header_03_open","C300_CG_Universal_IO_cont_1","C300_CG_Universal_IO_cont_2","Header_04_close","Header_04_open","SerC_CG_Enhanced_Function_IO_Cont","SerC_CG_Enhanced_Function_IO_Cont2"]
cont_attr_cl = ["C300_CG_Universal_IO_cont_1","C300_CG_Universal_IO_cont_2","SerC_CG_Enhanced_Function_IO_Cont","SerC_CG_Enhanced_Function_IO_Cont2"]
turbo_cont = ["C300_TurboM_IOM_CG_Cont","Header_05_close","Header_05_open"]
gen_attr = ["SerC_CG_Ethernet_Interface","SerC_CG_Foundation_Fieldbus_Interface_required","SerC_CG_Controller_Memory_Backup","SerC_GC_Profibus_Gateway_Interface"]
mark_cont = ["C300_CG_Universal_IO_Mark_1","C300_CG_Universal_IO_Mark_2","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont","Header_06_close","Header_06_open"]
mark_cont_cl = ["C300_CG_Universal_IO_Mark_1","C300_CG_Universal_IO_Mark_2","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1","C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont"]

if family_ty in ["Series C","Turbomachinery"]:
	for attr in Universal_Enhanc_contattr:
		Product.AllowAttr(attr)
	if family_ty == "Series C":
		Product.AllowAttr('SerC_CG_Type_of_Controller_Required')
	if UIO_Cont1.Rows.Count == 0:
		UIO_Cont1.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr from Universal_IO_count WHERE IO_Type!=''",'Code')
	if UIO_Cont2.Rows.Count == 0:
		UIO_Cont2.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr,future_red_isltr,non_red_isltr,red_rly,future_red_rly,non_red_rly from Universal_IO_count_1 WHERE IO_Type!=''",'Code')
	if EnhancedIO_Cont1.Rows.Count == 0:
		EnhancedIO_Cont1.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr from Enhanced_Function_IO WHERE IO_Type!=''",'Code')
	if EnhancedIO_Cont2.Rows.Count == 0:
		EnhancedIO_Cont2.LoadFromDatabase("Select top 30 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr, red_rly, future_red_rly, non_red_rly, Parent_Product from Enhanced_Function_IO2 WHERE Parent_Product ='Control Group'",'Code')
	if family_ty == "Turbomachinery" and TurboM_Cont.Rows.Count == 0:
		TurboM_Cont.LoadFromDatabase("Select IO_Type, Red_IOM from C300_TurboM_IOM",'Code')

else:
	if UIO_Mark1.Rows.Count == 0:
		UIO_Mark1.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr from Universal_IO_Mark_1 WHERE IO_Type!=''",'Code')
	if UIO_Mark2.Rows.Count == 0:
		UIO_Mark2.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr,red_rly,future_red_rly,non_red_rly from Universal_IO_Mark_2 WHERE IO_Type!=''",'Code')
	if EnhancedIO_Mark1.Rows.Count == 0:
		EnhancedIO_Mark1.LoadFromDatabase("SELECT IO_Type FROM Enhanced_function1 WHERE Container_Name = 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont'",'Code')
	if EnhancedIO_Mark2.Rows.Count == 0:
		EnhancedIO_Mark2.LoadFromDatabase("SELECT IO_Type FROM Enhanced_function WHERE Container_Name = 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1'",'Code')
	for cnt in cont_attr_cl:
		Product.GetContainerByName(cnt).Rows.Clear()
	for attr in Universal_Enhanc_contattr:
		Product.DisallowAttr(attr)
if Fim_Cont.Rows.Count == 0 and Product.Attr('SerC_CG_Foundation_Fieldbus_Interface_required').GetValue() == "Yes":
	Fim_Cont.LoadFromDatabase("SELECT IO_Type, Identifiers FROM FIM_FF_IO WHERE Container_Name = 'SerC_CG_FIM_FF_IO_Cont'",'Code')

control_typ = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
if family_ty == "Series C" and control_typ != "C300 CEE":
	for atr in gen_attr:
		Product.DisallowAttr(atr)
else:
	for atr in gen_attr:
		Product.AllowAttr(atr)