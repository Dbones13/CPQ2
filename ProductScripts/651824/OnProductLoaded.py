Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr('CE_Site_Voltage').AssignValue("120V")
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
def hideContainerColumns(contColumnList):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))
def editContainerColumns(contColumnList):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Editable) )*>'.format(contColumn,col))

nonR2QContColumn = {"SerC_RG_Enhanced_Function_IO_Cont":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR"],"SerC_RG_Enhanced_Function_IO_Cont2":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR","future_red_rly","Future_Red_HV_RLY"],"C300_RG_Universal_IO_cont_1":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR"],"C300_RG_Universal_IO_cont_2":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR","future_red_rly","Future_Red_HV_RLY"]}

nonR2QContColumn2 = {"C300_CG_Universal_IO_Mark_1":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR"],"C300_CG_Universal_IO_Mark_2":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR","future_red_rly","Future_HV_Rly"],"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR"],"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1":["Future_Red_IS","Future_Red_NIS","Future_Red_ISLTR","future_red_rly","Future_HV_Rly"]}

ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
controller = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()

if (controller == 'CN100 CEE') or (ioFamilyType in ("Series-C Mark II","Turbomachinery")):
    Product.DisallowAttr('Dummy_RG_IO_Mounting_Solution')
elif (ioFamilyType == 'Series C') and (controller != 'CN100 CEE'):
    Product.AllowAttr('Dummy_RG_IO_Mounting_Solution')

default_dict = {"Dummy_RG_IO_Mounting_Solution":"Cabinet","SerC_RG_CN100_I/O_HOVE":"Redundant","SerC_RG_Power_System_Vendor":"Phoenix Contact","SerC_RG_Marshalling_Cabinet_Type":"Universal Marshalling"}
for key,value in default_dict.items():
    if (Product.Attr(key).GetValue() == '') or (Product.Attr(key).GetValue() == 'None'):
        if (ioFamilyType in ("Series-C Mark II")) and key=='Dummy_RG_IO_Mounting_Solution' :
            Trace.Write("6")
        else:
            if (ioFamilyType == 'Series C') and (controller == 'CN100 CEE') and key=='Dummy_RG_IO_Mounting_Solution':
                Trace.Write('')
            else:
                Product.Attr(key).SelectDisplayValue(value)
#Log.Info("remote grp mounting:"+str(Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()))
mounting = Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()
if (ioFamilyType == 'Series C') and (controller != 'CN100 CEE'):
    Product.AllowAttr('Dummy_RG_IO_Mounting_Solution')
    if mounting == 'Cabinet':
        Product.Attr('SerC_IO_Mounting_Solution').SelectDisplayValue('Cabinet')
    elif mounting == 'Mounting Panel':
        Product.Attr('SerC_IO_Mounting_Solution').SelectDisplayValue('Mounting Panel')
    elif mounting == 'Universal Process Cab - 1.3M':
        Product.Attr('SerC_IO_Mounting_Solution').SelectDisplayValue('Universal Process Cab - 1.3M')
    else:
        Product.Attr('SerC_IO_Mounting_Solution').SelectDisplayValue('Cabinet')
if Product.Attr('SerC_IO_Mounting_Solution').GetValue() =='Universal Process Cab - 1.3M':
    Product.DisallowAttr('SerC_RG_Marshalling_Cabinet_Type')
    Product.DisallowAttr('SerC_RG_Percentage_SSM_Cabinet (0-100%)')

seriesC_attrlist = ["Header_15_close","Header_15_open","SerC_RG_Enhanced_Function_IO_Cont","SerC_RG_Enhanced_Function_IO_Cont2","C300_RG_Universal_IO_cont_1","C300_RG_Universal_IO_cont_2"]

seriesCM_attrlist=["C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont", "C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1", "C300_CG_Universal_IO_Mark_1", "C300_CG_Universal_IO_Mark_2","Header_03_open","Header_03_close"]
turboM_attrlist=["Header_16_open","Header_16_close","C300_TurboM_IOM_RG_Cont"]

if ioFamilyType in ("Series C","Turbomachinery"):
    for attr in seriesC_attrlist:
        Product.AllowAttr(attr)
    for attr in seriesCM_attrlist:
        Product.DisallowAttr(attr)
    if ioFamilyType == "Turbomachinery":
        for attr in turboM_attrlist:
            Product.AllowAttr(attr)
    else:
        for attr in turboM_attrlist:
            Product.DisallowAttr(attr)
else:
    for attr in seriesC_attrlist:
        Product.DisallowAttr(attr)
    for attr in seriesCM_attrlist:
        Product.AllowAttr(attr)
    for attr in turboM_attrlist:
        Product.DisallowAttr(attr)
Product.AllowAttr("Header_21_open")
Product.AllowAttr("Header_21_close")
cabinet_attr = ["Header_06_open","Header_06_close","C300_RG_UPC_Cab_Count","C300_RG_UPC_UIO2_Redundancy","C300_RG_UPC_Universal_IO_Count"]
IO_Mounting = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
if IO_Mounting in ("Cabinet","Mounting Panel") and controller != 'CN100 CEE':
    for attr in cabinet_attr:
        Product.DisallowAttr(attr)
else:
    for attr in cabinet_attr:
        Product.AllowAttr(attr)
    for attr in seriesC_attrlist:
        Product.DisallowAttr(attr)
    for attr in seriesCM_attrlist:
        Product.DisallowAttr(attr)
    for attr in turboM_attrlist:
        Product.DisallowAttr(attr)
    Product.DisallowAttr("Header_21_open")
    Product.DisallowAttr("Header_21_close")
    Product.DisallowAttr("SerC_RG_CN100_I/O_HOVE")
    Product.DisallowAttr("SerC_RG_Power_System_Vendor")
    Product.DisallowAttr("Header_19_open")
    Product.DisallowAttr("SerC_RG_Percent_Installed_Spare(0-100%)")
    Product.DisallowAttr("SerC_RG_Group_label_Defaults_for_Cabinet")
    #Product.Attr('C300_RG_UPC_Universal_IO_Count').SelectValue('3')
    cabCount = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    if cabCount=="":
        Product.Attr('C300_RG_UPC_Cab_Count').AssignValue('1')

if ioFamilyType in ('Series C', 'Turbomachinery'):
    hideContainerColumns(nonR2QContColumn)

elif ioFamilyType == 'Series-C Mark II':
    hideContainerColumns(nonR2QContColumn2)
IO_ContColumn = {"SerC_RG_Enhanced_Function_IO_Cont2":["Red_HV_Rly","Non_Red_HV_Rly"],"C300_RG_Universal_IO_cont_2":["Red_HV_Rly","Non_Red_HV_Rly"],"C300_CG_Universal_IO_Mark_2":["Red_HV_Rly","Non_Red_HV_Rly"],"C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1":["Red_HV_Rly","Non_Red_HV_Rly"]}
if Product.Attr('SerC_RG_Marshalling_Cabinet_Type').GetValue() == "3rd Party Marshalling":
    hideContainerColumns(IO_ContColumn)
else:
    editContainerColumns(IO_ContColumn)

if ioFamilyType =='Series C' and mounting =='Cabinet':
    Product.AllowAttr('SerC_RG_Power_System_Vendor')
elif ioFamilyType =='Series-C Mark II':
    Product.AllowAttr('SerC_RG_Power_System_Vendor')
else:
    Product.DisallowAttr('SerC_RG_Power_System_Vendor')

cabinet_dict = {"Header_19_open","Header_19_close","SerC_RG_Group_label_Defaults_for_Cabinet","SerC_RG_CN100_I/O_HOVE","SerC_RG_Power_System_Vendor","SerC_RG_Percent_Installed_Spare(0-100%)","SerC_RG_Marshalling_Cabinet_Type","SerC_RG_Percentage_SSM_Cabinet (0-100%)"}

if ioFamilyType =='Series C' and mounting =='Cabinet':
    for attr in cabinet_dict:
        Product.AllowAttr(attr)
    if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue() =='':
        Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').AssignValue('0')
    if Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').GetValue() =='':
        Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').AssignValue('0')

if controller == 'CN100 CEE':
    for attr in cabinet_dict:
        Product.DisallowAttr(attr)
    if  ioFamilyType =='Series C':
        Product.Attr('SerC_IO_Mounting_Solution').SelectDisplayValue('Universal Process Cab - 1.3M')
    else:
        Product.DisallowAttr('SerC_IO_Mounting_Solution')
    if Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue() =='':
        Product.Attr('C300_RG_UPC_Universal_IO_Count').SelectDisplayValue('32')
    if Product.Attr('C300_RG_UPC_UIO2_Redundancy').GetValue() =='':
        Product.Attr('C300_RG_UPC_UIO2_Redundancy').SelectDisplayValue('Redundant')
    Product.Attr('C300_RG_UPC_FTA').SelectDisplayValue('No Treatment')

elif ioFamilyType == 'Series-C Mark II':
    for attr in cabinet_dict:
        if attr !='SerC_RG_CN100_I/O_HOVE':
            Product.AllowAttr(attr)
    if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue() =='':
        Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').AssignValue('0')
    if Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').GetValue() =='':
        Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').AssignValue('0')
if ioFamilyType =='Series C' and mounting =='Cabinet':
    Product.AllowAttr('SerC_RG_CN100_I/O_HOVE')
else:
    Product.DisallowAttr('SerC_RG_CN100_I/O_HOVE')

if ioFamilyType =='Series C' and controller:
    Product.Attr('C300_RG_UPC_CNM').SelectDisplayValue('No CNM')
    Product.Attr('C300_RG_UPC_FTA').SelectDisplayValue('No Treatment')
    Product.Attr('SerC_RG_Cabinet_Base_(Plinth)').SelectDisplayValue('No')
    Product.Attr('SerC_RG_Cabinet_Thermostat_Default').SelectDisplayValue('No')
    Product.Attr('SerC_RG_Cabinet_Light_Default').SelectDisplayValue('No')
    Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').SelectDisplayValue('')
    Product.Attr('C300_RG_UPC_CN100_IO_HIVE').SelectDisplayValue('')
    Product.Attr('C300_RG_UPC_Controlled_IO_License_Count').SelectDisplayValue('')
    if controller == 'C300 CEE':
        Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').SelectDisplayValue('Single Mode x2')
        Product.Attr('C300_RG_UPC_CN100_IO_HIVE').SelectDisplayValue('None')
    elif controller == 'CN100 CEE':
        Product.Attr('C300_RG_UPC_Controlled_IO_License_Count').SelectDisplayValue('240 IO Control')

elif ioFamilyType !='Series C':
    Product.Attr('C300_RG_UPC_CNM').SelectDisplayValue('')
    Product.Attr('C300_RG_UPC_FTA').SelectDisplayValue('')
    Product.Attr('SerC_RG_Cabinet_Base_(Plinth)').SelectDisplayValue('')
    Product.Attr('SerC_RG_Cabinet_Thermostat_Default').SelectDisplayValue('')
    Product.Attr('SerC_RG_Cabinet_Light_Default').SelectDisplayValue('')
    Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').SelectDisplayValue('')
    Product.Attr('C300_RG_UPC_CN100_IO_HIVE').SelectDisplayValue('')
    Product.Attr('C300_RG_UPC_Controlled_IO_License_Count').SelectDisplayValue('')
if ioFamilyType =='Turbomachinery':
    cabinet_dict_turbo = {"Header_19_open","Header_19_close","SerC_RG_Group_label_Defaults_for_Cabinet","SerC_RG_Percent_Installed_Spare(0-100%)","SerC_RG_Marshalling_Cabinet_Type"}
    for attr in cabinet_dict_turbo:
        Product.AllowAttr(attr)
    if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue() =='':
        Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').AssignValue('0')
attrList = ['C300_RG_UPC_CNM', 'C300_RG_UPC_FTA', 'SerC_RG_Cabinet_Base_(Plinth)', 'SerC_RG_Cabinet_Thermostat_Default', 'SerC_RG_Cabinet_Light_Default', 'C300_RG_UPC_Fiber_Optic_Extender', 'C300_RG_UPC_CN100_IO_HIVE', 'C300_RG_UPC_Controlled_IO_License_Count']

for attr in attrList:
    Product.Attr(attr).Access = AttributeAccess.Hidden