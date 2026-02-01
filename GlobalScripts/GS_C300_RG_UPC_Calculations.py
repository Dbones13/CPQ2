#45394 by shivani
def getpart_51202789_900(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FOE=Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').GetValue()
    var17=0
    if Specify_id=='Yes' and len(id_modifier)>5:
        if id_modifier[5]=='T' or id_modifier[5]=='N':
            var17=int(cab_count)*1
    if Specify_id=="No":
        if FOE=='Single Mode x4' or FOE=='Multi Mode x4':
            var17=int(cab_count)*1
    return var17
#Tempo=getpart_51202789_900(Product)
#Trace.Write(Tempo)
#45892
def getpart_CC_SICC_1011(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_Giss=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    GI = Product.Attr('C300_RG_UPC_GI_Bases_Universal_Marshalling_Count').GetValue()
    Universal_io_count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    var=0
    if Specify_id=='Yes' and len(id_modifier)>14:
        if (id_modifier[12] =='G' and id_modifier[13] =='2' and id_modifier[15] =='3') or (id_modifier[12] =='G' and id_modifier[13] =='4' and id_modifier[15] =='6') or (id_modifier[12] =='G' and id_modifier[13] =='6' and id_modifier[15] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='2' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='4' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='0' and id_modifier[14] =='6' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='0' and id_modifier[16] =='3') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='0' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='6' and id_modifier[14] =='0' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='2' and id_modifier[16] =='6') or (id_modifier[12] =='N' and id_modifier[13] =='2' and id_modifier[14] =='4' and id_modifier[16] =='9') or (id_modifier[12] =='N' and id_modifier[13] =='4' and id_modifier[14] =='2' and id_modifier[16] =='9'):
            var=int(cab_count)*2
    if Specify_id=="No":
        if (FTA=='Universal Marshalling, GI only (0-6)' and Giis=='' and Non_Giss=='' and GI=='2' and Universal_io_count=='32') or (FTA=='Universal Marshalling, GI only (0-6)' and Giis=='' and Non_Giss=='' and GI=='4' and Universal_io_count=='64') or (FTA=='Universal Marshalling, GI only (0-6)' and Giis=='' and Non_Giss=='' and GI=='6' and Universal_io_count=='96') or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='0' and Non_Giss=='2' and GI=='' and Universal_io_count=='32') or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='0' and Non_Giss=='4' and GI=='' and Universal_io_count=='64')  :
            var=int(cab_count)*2
        if (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='0' and Non_Giss=='6' and GI=='' and Universal_io_count=='96') or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='0' and GI=='' and Universal_io_count=='32')  or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='0' and GI=='' and Universal_io_count=='64') or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='0' and GI=='' and Universal_io_count=='96')or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='2' and GI=='' and Universal_io_count=='64') or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='4' and GI=='' and Universal_io_count=='96') or (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='2' and GI=='' and Universal_io_count=='96')  :
            var=int(cab_count)*2
            
    return var

#45372
def getpart_51156387_315(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Trace.Write(Cab_type)
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_Giss=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Abu_Dhabi_Bld_Loc=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    
    
    var5=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='0' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='2' and id_modifier[21]=='D' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='4' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='6' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') :
            var5=int(cab_count)*1
        if (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='0' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='2' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='4' and id_modifier[21]=='D' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='6' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') :
            var5=int(cab_count)*1
        if (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='0' and id_modifier[21]=='D' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='2' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='4' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='6' and id_modifier[21]=='D' and id_modifier[22]=='R'and id_modifier[26]=='N') :
            var5=int(cab_count)*1
    if Specify_id=="No":
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='0' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT'and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='2' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='4' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='6' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No'):
            var5=int(cab_count)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='0' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='2' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='4' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='6' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT'and Abu_Dhabi_Bld_Loc=='No' ):
            var5=int(cab_count)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='0' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='2' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT'and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='4' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='6' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT'and Abu_Dhabi_Bld_Loc=='No'):
            var5=int(cab_count)*1
       
            
    return var5

#45391 by shivani
def getpart_51202688_104(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    var6=0
    if Specify_id=='Yes' and len(id_modifier)>2:
        if id_modifier[2]=='B' :
            var6=int(cab_count)*1
    if Specify_id=="No":
        if Ambient_Temp=='With Fan, Max Ambient +55°C':
            var6=int(cab_count)*1
    return var6

#45369
def getpart_51156387_328(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_Giss=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Abu_Dhabi_Bld_Loc=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    
    
    var7=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='0' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='2' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='4' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='6' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y'):
            var7=int(cab_count)*1
        if (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='0' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='2' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='4' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='6' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y'):
            var7=int(cab_count)*1
        if (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='0' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='2' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='4' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y') or (id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='6' and id_modifier[21]=='Q' and id_modifier[22]=='R'and id_modifier[26]=='Y'):
            var7=int(cab_count)*1
        
    if Specify_id=="No":
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='0' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes')or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='2' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='4' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='6' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') :
            var7=int(cab_count)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='0' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='2' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='4' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='6' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes'):
            var7=int(cab_count)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='0' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='2' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='4' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='6' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='Yes'):
            var7=int(cab_count)*1
       
            
    return var7


#45325
def getpart_51156387_313(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    Non_Giss=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    Abu_Dhabi_Bld_Loc=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    
    
    var8=0
    if Specify_id=='Yes' and len(id_modifier)>26:
        if (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='0' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='2' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='4' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='6' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N'):
            var8=int(cab_count)*1
        if (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='0' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='2' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='4' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='6' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N'):
            var8=int(cab_count)*1
        if (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='0' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='2' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='4' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N') or (id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='6' and id_modifier[21]=='Q' and id_modifier[22]=='R' and id_modifier[26]=='N'):
            var8=int(cab_count)*1
        
    if Specify_id=="No":
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='0' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' )or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='2' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='4' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='2' and Non_Giss=='6' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) :
            var8=int(cab_count)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='0' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='2' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No') or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='4' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='4' and Non_Giss=='6' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ):
            var8=int(cab_count)*1
        if (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='0' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='2' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No' ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='4' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No'  ) or (Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' and Giis=='6' and Non_Giss=='6' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and Abu_Dhabi_Bld_Loc=='No'):
            var8=int(cab_count)*1

    return var8

#45384
def getpart_51156389_310(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    var9=0
    if Specify_id=='Yes' and len(id_modifier)>21:
        if id_modifier[21]=='D' or id_modifier[20]=='D' or id_modifier[19]=='D' :
            var9=int(cab_count)*1
    if Specify_id=="No":
        if Power_Supply_type=='20A DC/DC QUINT4+ Supply' :
            var9=int(cab_count)*1
    return var9

#45885
def getpart_CC_INWM01(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    CN_Hive=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
    CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
    var10=0
    if Specify_id=='Yes' and len(id_modifier)>7:
        if (id_modifier[4]=='H' and id_modifier[7]=='Y') or (id_modifier[4]=='M' and id_modifier[7]=='Y') or (id_modifier[4]=='A' and id_modifier[7]=='Y') or (id_modifier[4]=='R' and id_modifier[7]=='Y') or (id_modifier[4]=='T' and id_modifier[7]=='Y') or (id_modifier[4]=='B' and id_modifier[7]=='Y'):
            var10=int(cab_count)*2
    if Specify_id=="No":
        if (CN_Hive=='Non-Redundant with SM SFP' and CNM=='Red Pair CNM') or (CN_Hive=='Non-Redundant with MM SFP' and CNM=='Red Pair CNM') or (CN_Hive=='Non-Redundant' and CNM=='Red Pair CNM') or (CN_Hive=='Redundant with SM SFP' and CNM=='Red Pair CNM') or (CN_Hive=='Redundant with MM SFP' and CNM=='Red Pair CNM') or (CN_Hive=='Redundant' and CNM=='Red Pair CNM') :
            var10=int(cab_count)*2
    return var10