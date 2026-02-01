#CXCPQ-45050
def getpart_50159943_002(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FDAP=Product.Attr('C300_RG_UPC_Ext_FDAP_Comm_Supp').GetValue()
    var7=0
    if Specify_id=='Yes' and len(id_modifier)>6:
        if id_modifier[6]=='S' or id_modifier[6]=='M':
            var7=int(cab_count)*1
    if Specify_id=="No":
        if FDAP=='FDAP Single-Mode' or FDAP=='FDAP Multi-Mode':
            var7=int(cab_count)*1
    return var7
#CXCPQ-45371
def getpart_51156387_329(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS_Universal=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    GIIS_Non_Universal=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    var8=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if id_modifier[1]=='S' and id_modifier[2] =='B' and id_modifier[21] =='Q' and id_modifier[22] =='R' and id_modifier[26] =='Y' and ((id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='6')):
            var8=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and abu_dhabi=='Yes' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '2' and GIIS_Non_Universal=='0') or (GIIS_Universal == '2' and GIIS_Non_Universal=='2') or (GIIS_Universal == '2' and GIIS_Non_Universal=='4') or (GIIS_Universal == '2' and GIIS_Non_Universal=='6') or (GIIS_Universal == '4' and GIIS_Non_Universal=='0') or (GIIS_Universal == '4' and GIIS_Non_Universal=='2') or (GIIS_Universal == '4' and GIIS_Non_Universal=='4') or (GIIS_Universal == '4' and GIIS_Non_Universal=='6') or (GIIS_Universal == '6' and GIIS_Non_Universal=='0') or (GIIS_Universal == '6' and GIIS_Non_Universal=='2') or (GIIS_Universal == '6' and GIIS_Non_Universal=='4') or (GIIS_Universal == '6' and GIIS_Non_Universal=='6')):
            var8=int(cab_count)*1
    return var8

#CXCPQ-45322
def getpart_51156387_310(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS_Universal=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    GIIS_Non_Universal=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    var9=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if id_modifier[1]=='S' and id_modifier[2] =='A' and id_modifier[21] =='R' and id_modifier[22] =='R' and ((id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='6')) and id_modifier[26]=='N':
            var9=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and Power_Supply_type=='20A AC/DC ATDI Supply – Rack Mount' and power_supply_red=='REDUNDANT' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '2' and GIIS_Non_Universal=='0') or (GIIS_Universal == '2' and GIIS_Non_Universal=='2') or (GIIS_Universal == '2' and GIIS_Non_Universal=='4') or (GIIS_Universal == '2' and GIIS_Non_Universal=='6') or (GIIS_Universal == '4' and GIIS_Non_Universal=='0') or (GIIS_Universal == '4' and GIIS_Non_Universal=='2') or (GIIS_Universal == '4' and GIIS_Non_Universal=='4') or (GIIS_Universal == '4' and GIIS_Non_Universal=='6') or (GIIS_Universal == '6' and GIIS_Non_Universal=='0') or (GIIS_Universal == '6' and GIIS_Non_Universal=='2') or (GIIS_Universal == '6' and GIIS_Non_Universal=='4') or (GIIS_Universal == '6' and GIIS_Non_Universal=='6')) and  abu_dhabi=='No':
            var9=int(cab_count)*1
    return var9

#CXCPQ-45332
def getpart_51156387_318(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    var10=0
    i,j,k=19,20,24
    lrn=len(id_modifier)
    Trace.Write("lrn "+str(lrn))
    if len(id_modifier)==26:
        Trace.Write("26")
        i,j,k= 20,21,25
    elif len(id_modifier)==25:
        Trace.Write("25")
        i,j,k=19,20,24
    elif len(id_modifier)==27:
        Trace.Write("27")
        i,j,k=21,22,26
    if Specify_id=='Yes' and len(id_modifier)>24:
        if id_modifier[1]=='S' and id_modifier[2]=='A' and (id_modifier[12]=='X' or (id_modifier[12]=='G' and id_modifier[13]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='4') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='6') or (id_modifier[12]=='G' and id_modifier[13]=='2') or (id_modifier[12]=='G' and id_modifier[13]=='4') or (id_modifier[12]=='G' and id_modifier[13]=='6') ) and id_modifier[i]=='R' and id_modifier[j]=='R' and id_modifier[k]=='Y':
            var10=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and Power_Supply_type=='20A AC/DC ATDI Supply – Rack Mount' and power_supply_red=='REDUNDANT' and abu_dhabi=='Yes' and (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' or FTA=='Universal Marshalling, GI only (0-6)' or FTA == 'No Treatment'):
            var10=int(cab_count)*1
    return var10

#CXCPQ-46088
def getpart_CC_UGIA01(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS_Universal=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    GIIS_Non_Universal=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Universal_io_count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    var11=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='0'and id_modifier[16]=='3') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='2' and id_modifier[16]=='6') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='4' and id_modifier[16]=='9'):
            var11=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='0' and id_modifier[16]=='6') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='2' and id_modifier[16]=='9'):
            var11=int(cab_count)*4
        if(id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='0'):
            var11=int(cab_count)*6
    if Specify_id=="No":
        if FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '2' and GIIS_Non_Universal=='0' and Universal_io_count=='32') or (GIIS_Universal == '2' and GIIS_Non_Universal=='2' and Universal_io_count=='64') or (GIIS_Universal == '2' and GIIS_Non_Universal=='4' and Universal_io_count=='96')):
            var11=int(cab_count)*2
        if FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '4' and GIIS_Non_Universal=='0' and Universal_io_count=='64') or (GIIS_Universal == '4' and GIIS_Non_Universal=='2' and Universal_io_count=='96')):
            var11=int(cab_count)*4
        if FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and GIIS_Universal == '6' and GIIS_Non_Universal=='0' and Universal_io_count=='96':
            var11=int(cab_count)*6
    return var11

#CXCPQ-45360
def getpart_51156387_327(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS_Universal=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    GIIS_Non_Universal=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    var13=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if id_modifier[1]=='S' and id_modifier[2] =='B' and id_modifier[21] =='R' and id_modifier[22] =='R' and id_modifier[26] =='Y' and ((id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='6')):
            var13=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='20A AC/DC ATDI Supply – Rack Mount' and power_supply_red=='REDUNDANT' and abu_dhabi=='Yes' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '2' and GIIS_Non_Universal=='0') or (GIIS_Universal == '2' and GIIS_Non_Universal=='2') or (GIIS_Universal == '2' and GIIS_Non_Universal=='4') or (GIIS_Universal == '2' and GIIS_Non_Universal=='6') or (GIIS_Universal == '4' and GIIS_Non_Universal=='0') or (GIIS_Universal == '4' and GIIS_Non_Universal=='2') or (GIIS_Universal == '4' and GIIS_Non_Universal=='4') or (GIIS_Universal == '4' and GIIS_Non_Universal=='6') or (GIIS_Universal == '6' and GIIS_Non_Universal=='0') or (GIIS_Universal == '6' and GIIS_Non_Universal=='2') or (GIIS_Universal == '6' and GIIS_Non_Universal=='4') or (GIIS_Universal == '6' and GIIS_Non_Universal=='6')):
            var13=int(cab_count)*1
    return var13

#CXCPQ-46095
def getpart_FS_CCI_HSE_03(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    CN_Hive=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
    CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
    EIM=Product.Attr('C300_RG_UPC_EIM').GetValue()
    var14=0
    if Specify_id=='Yes' and len(id_modifier)>10:
        if id_modifier[7] =='Y'and id_modifier[10] =='Y' and (id_modifier[4] =='H' or id_modifier[4] =='M' or id_modifier[4] =='A' or id_modifier[4] =='R' or id_modifier[4] =='T' or id_modifier[4] =='B'):
            var14=int(cab_count)*1
    if Specify_id=="No":
        if CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM' and ((CN_Hive=='Non-Redundant with SM SFP') or (CN_Hive=='Redundant with SM SFP') or (CN_Hive=='Non-Redundant') or (CN_Hive=='Non-Redundant with MM SFP') or (CN_Hive=='Redundant with MM SFP') or (CN_Hive=='Redundant')):
            var14=int(cab_count)*1
    return var14
#CXCPQ-45321
def getpart_51156387_311(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS_Universal=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    GIIS_Non_Universal=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    var15=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if id_modifier[1]=='S' and id_modifier[2] =='B' and id_modifier[21] =='R' and id_modifier[22] =='R' and ((id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='6')) and id_modifier[26]=='N':
            var15=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='20A AC/DC ATDI Supply – Rack Mount' and power_supply_red=='REDUNDANT' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '2' and GIIS_Non_Universal=='0') or (GIIS_Universal == '2' and GIIS_Non_Universal=='2') or (GIIS_Universal == '2' and GIIS_Non_Universal=='4') or (GIIS_Universal == '2' and GIIS_Non_Universal=='6') or (GIIS_Universal == '4' and GIIS_Non_Universal=='0') or (GIIS_Universal == '4' and GIIS_Non_Universal=='2') or (GIIS_Universal == '4' and GIIS_Non_Universal=='4') or (GIIS_Universal == '4' and GIIS_Non_Universal=='6') or (GIIS_Universal == '6' and GIIS_Non_Universal=='0') or (GIIS_Universal == '6' and GIIS_Non_Universal=='2') or (GIIS_Universal == '6' and GIIS_Non_Universal=='4') or (GIIS_Universal == '6' and GIIS_Non_Universal=='6')) and abu_dhabi=="No":
            var15=int(cab_count)*1
    return var15

#CXCPQ-45898
def get_CC_TAIL51(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    LLAI_cnt=Product.Attr('C300_RG_UPC_LLAI_Count').GetValue()
    var16=0
    i=16
    if len(id_modifier)>25:
        i=17
    if len(id_modifier)>26:
        i=18
    if len(id_modifier)>27:
        i=19
    if Specify_id=='Yes' and len(id_modifier)>16:
        if id_modifier[i]=='1':
            var16=int(cab_cnt)*1
        if id_modifier[i]=='2':
            var16=int(cab_cnt)*2
        if id_modifier[i]=='3':
            var16=int(cab_cnt)*3
        if id_modifier[i]=='4':
            var16=int(cab_cnt)*4
        if id_modifier[i]=='5':
            var16=int(cab_cnt)*5
        if id_modifier[i]=='6':
            var16=int(cab_cnt)*6
        if id_modifier[i]=='7':
            var16=int(cab_cnt)*7
        if id_modifier[i]=='8':
            var16=int(cab_cnt)*8
    if Specify_id=='No':
        if LLAI_cnt=='1':
            var16=int(cab_cnt)*1
        if LLAI_cnt=='2':
            var16=int(cab_cnt)*2
        if LLAI_cnt=='3':
            var16=int(cab_cnt)*3
        if LLAI_cnt=='4':
            var16=int(cab_cnt)*4
        if LLAI_cnt=='5':
            var16=int(cab_cnt)*5
        if LLAI_cnt=='6':
            var16=int(cab_cnt)*6
        if LLAI_cnt=='7':
            var16=int(cab_cnt)*7
        if LLAI_cnt=='8':
            var16=int(cab_cnt)*8
    return var16

#CXCPQ-45320
def getpart_51156387_309(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS_Universal=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    GIIS_Non_Universal=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    var17=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if id_modifier[1]=='S' and id_modifier[2] =='B' and id_modifier[21] =='A' and id_modifier[22] =='R' and ((id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='2'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='4'and id_modifier[14] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='0') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='2') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='4') or (id_modifier[12] =='N' and id_modifier[13] =='6'and id_modifier[14] =='6')) and id_modifier[26]=='N':
            var17=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and ((GIIS_Universal == '2' and GIIS_Non_Universal=='0') or (GIIS_Universal == '2' and GIIS_Non_Universal=='2') or (GIIS_Universal == '2' and GIIS_Non_Universal=='4') or (GIIS_Universal == '2' and GIIS_Non_Universal=='6') or (GIIS_Universal == '4' and GIIS_Non_Universal=='0') or (GIIS_Universal == '4' and GIIS_Non_Universal=='2') or (GIIS_Universal == '4' and GIIS_Non_Universal=='4') or (GIIS_Universal == '4' and GIIS_Non_Universal=='6') or (GIIS_Universal == '6' and GIIS_Non_Universal=='0') or (GIIS_Universal == '6' and GIIS_Non_Universal=='2') or (GIIS_Universal == '6' and GIIS_Non_Universal=='4') or (GIIS_Universal == '6' and GIIS_Non_Universal=='6')) and abu_dhabi == 'No':
            var17=int(cab_count)*1
    return var17
#46903 By Shivani
def getpart_CC_TEIM01(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    CN_Hive=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
    CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
    EIM=Product.Attr('C300_RG_UPC_EIM').GetValue()
    var12=0
    if Specify_id=='Yes' and len(id_modifier)>10:
        if (id_modifier[4] =='H' and id_modifier[7] =='Y'and id_modifier[10] =='Y') or (id_modifier[4] =='M' and id_modifier[7] =='Y'and id_modifier[10] =='Y') or (id_modifier[4] =='A' and id_modifier[7] =='Y'and id_modifier[10] =='Y') or (id_modifier[4] =='R' and id_modifier[7] =='Y'and id_modifier[10] =='Y') or (id_modifier[4] =='T' and id_modifier[7] =='Y'and id_modifier[10] =='Y') or (id_modifier[4] =='B' and id_modifier[7] =='Y'and id_modifier[10] =='Y'):
            var12=int(cab_count)*2
    if Specify_id=="No":
        if (CN_Hive=='Non-Redundant with SM SFP' and CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM') or (CN_Hive=='Redundant with SM SFP' and CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM') or (CN_Hive=='Non-Redundant' and CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM') or (CN_Hive=='Non-Redundant with MM SFP' and CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM') or (CN_Hive=='Redundant with MM SFP' and CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM') or (CN_Hive=='Redundant' and CNM == 'Red Pair CNM' and EIM =='Yes, Red pair EIM') :
            var12=int(cab_count)*2
    return var12
#Tempo=getpart_CC_TEIM01(Product)
#Trace.Write(Tempo)
#45400 By Shivani
def getpart_51202692_200(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Universal_io_count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    var13=0
    if Specify_id=='Yes' and len(id_modifier)>14:
        if (id_modifier[12] =='M' and id_modifier[14] =='3') or (id_modifier[12] =='M' and id_modifier[14] =='6') or (id_modifier[12] =='M' and id_modifier[14] =='9'):
            var13=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='3') :
            var13=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='0' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='3'):
            var13=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='6') :
            var13=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='0' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='6'):
            var13=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='9') :
            var13=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='0' and id_modifier[15] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='9'):
            var13=int(cab_count)*2
    if Specify_id=="No":
        if (FTA=='Weidmuller Marshalling' and Universal_io_count == '32')  or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Universal_io_count == '32') or (FTA=='Universal Marshalling, GI only (0-6)' and Universal_io_count == '32') or (FTA=='Weidmuller Marshalling' and Universal_io_count == '64')  or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Universal_io_count == '64') or (FTA=='Universal Marshalling, GI only (0-6)' and Universal_io_count == '64') or (FTA=='Weidmuller Marshalling' and Universal_io_count == '96')  or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Universal_io_count == '96') or (FTA=='Universal Marshalling, GI only (0-6)' and Universal_io_count == '96')  :
            var13=int(cab_count)*2
    return var13
#45843 By Shivani
def getpart_51121566_102(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Universal_io_count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    var14=0
    if Specify_id=='Yes' and len(id_modifier)>14:
        if (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='3') :
            var14=int(cab_count)*1
        if (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='4' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='6' and id_modifier[16] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='0' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='3'):
            var14=int(cab_count)*1
        if (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='6') :
            var14=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='6' and id_modifier[16] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='0' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='6'):
            var14=int(cab_count)*2
        if (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='9') :
            var14=int(cab_count)*3
        if (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='2' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='0' and id_modifier[15] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='9') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='9'):
            var14=int(cab_count)*3
    if Specify_id=="No":
        if (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Universal_io_count == '32') or (FTA=='Universal Marshalling, GI only (0-6)' and Universal_io_count == '32'): 
            var14=int(cab_count)*1
        if (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Universal_io_count == '64') or (FTA=='Universal Marshalling, GI only (0-6)' and Universal_io_count == '64'):
            var14=int(cab_count)*2
        if (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Universal_io_count == '96') or (FTA=='Universal Marshalling, GI only (0-6)' and Universal_io_count == '96'):
            var14=int(cab_count)*3
            
    return var14