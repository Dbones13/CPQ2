#45353 By Shivani Kothari
def get51156387_324(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Abu_Dhabi_Bld_Loc=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    Giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_Giss=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    var=0
    if Specify_id=='Yes'and len(id_modifier)>24:
        Trace.Write("AA")
        if (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='0'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y') or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='2'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y')or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='4'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y')or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='6'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y') :
            var=int(cab_cnt)*1
        if (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='0'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y') or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='2'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y')or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='4'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y')or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='6'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y'):
            var=int(cab_cnt)*1
        if (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='0'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y') or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='2'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y')or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='4'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y')or (id_modifier[1]=='S'and id_modifier[2]=='A'and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='6'and id_modifier[21]=='A' and id_modifier[22]=='R' and id_modifier[26]=='Y'):
            var=int(cab_cnt)*1
    if Specify_id=='No':
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='0' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or(Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='2' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='4' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes')  :
            var=int(cab_cnt)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='6' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='0' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='2' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='4' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes'):
            var=int(cab_cnt)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='6' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='0' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='2' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='4' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='6' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes'):
            var=int(cab_cnt)*1
            
    Trace.Write("var= "+str(var))
    return var
'''Value=get51156387_324(Product)
Trace.Write(Value)'''


#12K. #CXCPQ-45897
def getC300UPC_45897(Product):
    MIB = Product.Attr('MIB Configuration Required?').GetValue()
    IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FTA = Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS = Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_GIIS = Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    GI = Product.Attr('C300_RG_UPC_GI_Bases_Universal_Marshalling_Count').GetValue()
    Uni_Count = Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    
    val_12=0
    
    if ID_Specify=='Yes' and len(ID_Modify)> 16:
        if ID_Modify[12]=='G' and ID_Modify[13]=='6' and ID_Modify[15]=='9':
            val_12=int(Num_Cabinet) * 2
        elif ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='6' and ID_Modify[16]=='9':
            val_12=int(Num_Cabinet) * 2
        elif ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='0' and ID_Modify[16]=='9':
            val_12=int(Num_Cabinet) * 2
        elif ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='4' and ID_Modify[16]=='9':
            val_12=int(Num_Cabinet) * 2
        elif ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='2' and ID_Modify[16]=='9':
            val_12=int(Num_Cabinet) * 2
    elif ID_Specify=='No':
        if FTA=="Universal Marshalling, GI only (0-6)" and GI=="6" and Uni_Count=="96":
            val_12=int(Num_Cabinet) * 2
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="0" and Non_GIIS=="6" and Uni_Count=="96":
            val_12=int(Num_Cabinet) * 2
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="0" and Uni_Count=="96":
            val_12=int(Num_Cabinet) * 2
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="4" and Uni_Count=="96":
            val_12=int(Num_Cabinet) * 2
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="2" and Uni_Count=="96":
            val_12=int(Num_Cabinet) * 2
    return int(val_12)

#Value_12=getC300UPC_45897(Product)
#Trace.Write(Value_12)

#13K. #CXCPQ-45319
def getC300UPC_45319(Product):
    MIB = Product.Attr('MIB Configuration Required?').GetValue()
    IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_temp = Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    FTA = Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS = Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_GIIS = Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    Abu_Dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    val_13=0
    
    if ID_Specify=='Yes' and len(ID_Modify)> 26:
        if ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='0' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='2' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='4' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='6' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='0' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='2' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='4' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='6' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='0' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='2' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='4' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='6' and ID_Modify[21]=='A' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_13=int(Num_Cabinet) * 1
    elif ID_Specify=='No':
        if Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="0" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="2" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="4" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="6" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="0" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="2" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="4" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="6" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="0" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="2" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="4" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="6" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_13=int(Num_Cabinet) * 1

    return int(val_13)

#Value_13=getC300UPC_45319(Product)
#Trace.Write(Value_13)

#14K. #CXCPQ-45324
def getC300UPC_45324(Product):
    MIB = Product.Attr('MIB Configuration Required?').GetValue()
    IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_temp = Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    FTA = Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS = Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_GIIS = Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    Abu_Dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    val_14=0
    
    if ID_Specify=='Yes' and len(ID_Modify)> 26:
        if ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='0' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='2' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='4' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='6' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='0' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='2' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='4' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='6' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='0' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='2' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='4' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='A' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='6' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='N':
            val_14=int(Num_Cabinet) * 1
    elif ID_Specify=='No':
        if Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="0" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="2" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="4" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="6" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="0" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="2" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="4" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="6" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="0" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="2" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="4" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="6" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi=="No":
            val_14=int(Num_Cabinet) * 1

    return int(val_14)

#Value_14=getC300UPC_45324(Product)
#Trace.Write(Value_14)

#15K. #CXCPQ-45376
def getC300UPC_45376(Product):
    MIB = Product.Attr('MIB Configuration Required?').GetValue()
    IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_temp = Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    FTA = Product.Attr('C300_RG_UPC_FTA').GetValue()
    GIIS = Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_GIIS = Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    AbuD_Loc = Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    
    val_15=0
    
    if ID_Specify=='Yes' and len(ID_Modify)> 26:
        if ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='0' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='2' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='4' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='6' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='0' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='2' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='4' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='6' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='0' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='2' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='4' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
        elif ID_Modify[1]=='S' and ID_Modify[2]=='B' and ID_Modify[12]=='N' and ID_Modify[13]=='6' and ID_Modify[14]=='6' and ID_Modify[21]=='D' and ID_Modify[22]=='R' and ID_Modify[26]=='Y':
            val_15=int(Num_Cabinet) * 1
    elif ID_Specify=='No':
        if Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="0" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="2" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="4" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="6" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="0" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="2" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="4" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="6" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="0" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="2" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="4" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
        elif Cab_type=="Stainless Steel, IP66" and Ambient_temp=="With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="6" and Non_GIIS=="6" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and AbuD_Loc=="Yes":
            val_15=int(Num_Cabinet) * 1
            
    return int(val_15)


def getC300UpsCals_51202684_51202699(Product):

    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    UIO_Cnt=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()

    qty=0

    if Specify_id=='Yes' and len(id_modifier)> 14:
        if (id_modifier[12] == 'M' and id_modifier[14] == '3'):
            qty=int(cab_cnt)*2
        if (id_modifier[12] == 'M' and id_modifier[14]== '6'):
            qty=int(cab_cnt)*4
        if (id_modifier[12] == 'M' and id_modifier[14]== '9'):
            qty=int(cab_cnt)*6

    if Specify_id=='No':
        if (UIO_Cnt == '32' and FTA == 'Weidmuller Marshalling'):
            qty=int(cab_cnt)*2
        if (UIO_Cnt == '64' and FTA == 'Weidmuller Marshalling'):
            qty=int(cab_cnt)*4
        if (UIO_Cnt == '96' and FTA == 'Weidmuller Marshalling'):
            qty=int(cab_cnt)*6

    return qty


#Value_15=getC300UPC_45376(Product)
#Trace.Write(Value_15)