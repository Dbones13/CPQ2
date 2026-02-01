#CXCPQ-45899
def getpartTUIO31(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    #Trace.Write(id_modifier)
    #Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    #Trace.Write(cab_cnt)
    UIO_Count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    #Trace.Write(UIO_Count)
    UIO2_Redundancy=Product.Attr('C300_RG_UPC_UIO2_Redundancy').GetValue()
    #Trace.Write(UIO2_Redundancy)
    var=var1=var2=var3=0
    i,j=14,15
    if len(id_modifier)==26:
        i,j=15,16
    if len(id_modifier)==27:
        i,j=16,17
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[i]=='3' and id_modifier[j]=='N':
            var1=int(cab_cnt)*1
        if id_modifier[i]=='6' and id_modifier[j]=='N':
            var2=int(cab_cnt)*2
        if id_modifier[i]=='9' and id_modifier[j]=='N':
            var3=int(cab_cnt)*3
    if Specify_id=='No':
        if UIO_Count=="32" and UIO2_Redundancy=="Non-Redundant":
            var1=int(cab_cnt)*1
        if UIO_Count=="64" and UIO2_Redundancy=="Non-Redundant":
            var2=int(cab_cnt)*2
        if UIO_Count=="96" and UIO2_Redundancy=="Non-Redundant":
            var3=int(cab_cnt)*3
    var=var1+var2+var3
    return var
#Trace.Write(getpartTUIO31(Product))
#CXCPQ-45888
def getpartPUIO31(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    #Trace.Write(id_modifier)
    #Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    #Trace.Write(cab_cnt)
    UIO_Count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    #Trace.Write(UIO_Count)
    UIO2_Redundancy=Product.Attr('C300_RG_UPC_UIO2_Redundancy').GetValue()
    #Trace.Write(UIO2_Redundancy)
    var=var1=var2=var3=0
    i,j=14,15
    if len(id_modifier)==26:
        i,j=15,16
    if len(id_modifier)==27:
        i,j=16,17
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[i]=='3' and id_modifier[j]=='N':
            var=int(cab_cnt)*1
        if id_modifier[i]=='6' and id_modifier[j]=='N':
            var=int(cab_cnt)*2
        if id_modifier[i]=='9' and id_modifier[j]=='N':
            var=int(cab_cnt)*3
        if id_modifier[i]=='3' and id_modifier[j]=='R':
            var=int(cab_cnt)*2
        if id_modifier[i]=='6' and id_modifier[j]=='R':
            var=int(cab_cnt)*4
        if id_modifier[i]=='9' and id_modifier[j]=='R':
            var=int(cab_cnt)*6
    if Specify_id=='No':
        if UIO_Count=="32" and UIO2_Redundancy=="Non-Redundant":
            var=int(cab_cnt)*1
        if UIO_Count=="64" and UIO2_Redundancy=="Non-Redundant":
            var=int(cab_cnt)*2
        if UIO_Count=="96" and UIO2_Redundancy=="Non-Redundant":
            var=int(cab_cnt)*3
        if UIO_Count=="32" and UIO2_Redundancy=="Redundant":
            var=int(cab_cnt)*2
        if UIO_Count=="64" and UIO2_Redundancy=="Redundant":
            var=int(cab_cnt)*4
        if UIO_Count=="96" and UIO2_Redundancy=="Redundant":
            var=int(cab_cnt)*6
    return var
#Trace.Write(getpartPUIO31(Product))
#CXCPQ-46090
def getpartCCUPTA01(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Trace.Write(id_modifier)
    Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    fts=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Trace.Write(fts)
    giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    ngiis=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    UIO_Count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    i,j,k,m=12,13,14,16
    var=0
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[i]=='N'and id_modifier[j]=='0'and id_modifier[k]=='2' and id_modifier[m]=='3':
            var=int(cab_cnt)*32
        if id_modifier[i]=='N'and id_modifier[j]=='0'and id_modifier[k]=='4' and id_modifier[m]=='6':
            var=int(cab_cnt)*64
        if id_modifier[i]=='N'and id_modifier[j]=='0'and id_modifier[k]=='6' and id_modifier[m]=='9':
            var=int(cab_cnt)*96
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='2' and id_modifier[m]=='6':
            var=int(cab_cnt)*32
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='4' and id_modifier[m]=='9':
            var=int(cab_cnt)*64
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='2' and id_modifier[m]=='9':
            var=int(cab_cnt)*32
    if Specify_id=='No':
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="0" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*32
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="0" and ngiis=="4" and UIO_Count=="64":
            var=int(cab_cnt)*64
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="0" and ngiis=="6" and UIO_Count=="96":
            var=int(cab_cnt)*96
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="2" and UIO_Count=="64":
            var=int(cab_cnt)*32
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="4" and UIO_Count=="96":
            var=int(cab_cnt)*64
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="2" and UIO_Count=="96":
            var=int(cab_cnt)*32
    return var
#Trace.Write(getpartCCUPTA01(Product))
#CXCPQ-45359
def getpart51156387326(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Trace.Write(id_modifier)
    Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    #Trace.Write(Supply_Type)
    Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    #Trace.Write(Supply_Red)
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    #Trace.Write(Cab_type)
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    #Trace.Write(Ambient_Temp)
    Abu_Dhabi_Bld_Loc=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    #Trace.Write(Abu_Dhabi_Bld_Loc)
    fts=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Trace.Write(fts)
    giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    ngiis=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    UIO_Count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    var=0
    i,j,k,m,n,o=12,13,14,21,22,26
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[m]=='R' and id_modifier[n]=='R' and id_modifier[o]=='Y':
            if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='0':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='2':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='4':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='6':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='0':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='2':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='4':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='6':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='0':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='2':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='4':
                var=int(cab_cnt)*1
            if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='6':
                var=int(cab_cnt)*1
    if Specify_id=='No':
        if Cab_type=="Stainless Steel, IP66" and Ambient_Temp=="Without Fan, Max Ambient +40°C" and Supply_Type=="20A AC/DC ATDI Supply – Rack Mount" and Supply_Red=="REDUNDANT" and Abu_Dhabi_Bld_Loc=="Yes" and fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)":
            if giis=="2" and ngiis=="0":
                var=int(cab_cnt)*1
            if giis=="2" and ngiis=="2":
                var=int(cab_cnt)*1
            if giis=="2" and ngiis=="4":
                var=int(cab_cnt)*1
            if giis=="2" and ngiis=="6":
                var=int(cab_cnt)*1
            if giis=="4" and ngiis=="0":
                var=int(cab_cnt)*1
            if giis=="4" and ngiis=="2":
                var=int(cab_cnt)*1
            if giis=="4" and ngiis=="4":
                var=int(cab_cnt)*1
            if giis=="4" and ngiis=="6":
                var=int(cab_cnt)*1
            if giis=="6" and ngiis=="0":
                var=int(cab_cnt)*1
            if giis=="6" and ngiis=="2":
                var=int(cab_cnt)*1
            if giis=="6" and ngiis=="4":
                var=int(cab_cnt)*1
            if giis=="6" and ngiis=="6":
                var=int(cab_cnt)*1
    return var
#Trace.Write(getpart51156387326(Product))
def getpart51121566101(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Trace.Write(id_modifier)
    Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    fts=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Trace.Write(fts)
    giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    ngiis=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    UIO_Count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    i,j,k,m=12,13,14,16
    var=0
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='0' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='2' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='4' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='6' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='0' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='2' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='4' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='6' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='0' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='2' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='4' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='6' and id_modifier[m]=='3':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='0' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='2' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='4' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='6' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='0' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='2' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='4' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='6' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='0' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='2' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='4' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='6' and id_modifier[m]=='6':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='0' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='2' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='4' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='6' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='0' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='2' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='4' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='6' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='0' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='2' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='4' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='6' and id_modifier[m]=='9':
            var=int(cab_cnt)*1
    if Specify_id=='No':
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="0" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="4" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="6" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="0" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="4" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="6" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="0" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="4" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="6" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="0" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="4" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="6" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="0" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="4" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="6" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="0" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="2" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="4" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="6" and UIO_Count=="32":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="0" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="2" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="4" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="6" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="0" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="2" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="4" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="6" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="0" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="2" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="4" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="6" and UIO_Count=="64":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="0" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="2" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="4" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="2" and ngiis=="6" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="0" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="2" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="4" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="4" and ngiis=="6" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="0" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="2" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="4" and UIO_Count=="96":
            var=int(cab_cnt)*1
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="6" and ngiis=="6" and UIO_Count=="96":
            var=int(cab_cnt)*1

    return var
#Trace.Write(getpart51121566101(Product))
#CXCPQ-45884
def getpartCCINAM01(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Trace.Write(id_modifier)
    Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
    Trace.Write(CN100)
    var=0
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[4]=='H':
            var=int(cab_cnt)*2
        if id_modifier[4]=='M':
            var=int(cab_cnt)*2
        if id_modifier[4]=='A':
            var=int(cab_cnt)*2
        if id_modifier[4]=='R':
            var=int(cab_cnt)*2
        if id_modifier[4]=='T':
            var=int(cab_cnt)*2
        if id_modifier[4]=='B':
            var=int(cab_cnt)*2
    if Specify_id=='No':
        if CN100=="Non-Redundant with SM SFP":
            var=int(cab_cnt)*2
        if CN100=="Non-Redundant with MM SFP":
            var=int(cab_cnt)*2
        if CN100=="Non-Redundant":
            var=int(cab_cnt)*2
        if CN100=="Redundant with SM SFP":
            var=int(cab_cnt)*2
        if CN100=="Redundant with MM SFP":
            var=int(cab_cnt)*2
        if CN100=="Redundant":
            var=int(cab_cnt)*2
    return var
#Trace.Write(getpartCCINAM01(Product))
#CXCPQ-45883
def getpartCCIION01(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Trace.Write(id_modifier)
    Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Trace.Write(cab_cnt)
    CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
    Trace.Write(CN100)
    var=0
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[4]=='H':
            var=int(cab_cnt)*1
        if id_modifier[4]=='M':
            var=int(cab_cnt)*1
        if id_modifier[4]=='A':
            var=int(cab_cnt)*1
        if id_modifier[4]=='R':
            var=int(cab_cnt)*2
        if id_modifier[4]=='T':
            var=int(cab_cnt)*2
        if id_modifier[4]=='B':
            var=int(cab_cnt)*2
    if Specify_id=='No':
        if CN100=="Non-Redundant with SM SFP":
            var=int(cab_cnt)*1
        if CN100=="Non-Redundant with MM SFP":
            var=int(cab_cnt)*1
        if CN100=="Non-Redundant":
            var=int(cab_cnt)*1
        if CN100=="Redundant with SM SFP":
            var=int(cab_cnt)*2
        if CN100=="Redundant with MM SFP":
            var=int(cab_cnt)*2
        if CN100=="Redundant":
            var=int(cab_cnt)*2
    return var
#Trace.Write(getpartCCIION01(Product))
#CXCPQ-45893
def getpartCCSICC1011LR10(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    Trace.Write(id_modifier)
    Trace.Write(len(id_modifier))
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    fts=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Trace.Write(fts)
    giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    ngiis=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
    ugiis=Product.Attr('C300_RG_UPC_GI_Bases_Universal_Marshalling_Count').GetValue()
    UIO_Count=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    i,j,k,m=12,13,0,14
    if len(id_modifier)==26:
        i,j,k,m=12,13,14,15
    if len(id_modifier)==27:
        i,j,k,m=12,13,14,16
    var=0
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[i]=='G'and id_modifier[j]=='4' and id_modifier[m]=='6':
            var=int(cab_cnt)*2
        if id_modifier[i]=='G'and id_modifier[j]=='6' and id_modifier[m]=='9':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='0'and id_modifier[k]=='4' and id_modifier[m]=='6':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='0'and id_modifier[k]=='6' and id_modifier[m]=='9':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='0' and id_modifier[m]=='6':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='6'and id_modifier[k]=='0' and id_modifier[m]=='9':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='2' and id_modifier[m]=='6':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='2'and id_modifier[k]=='4' and id_modifier[m]=='9':
            var=int(cab_cnt)*2
        if id_modifier[i]=='N'and id_modifier[j]=='4'and id_modifier[k]=='2' and id_modifier[m]=='9':
            var=int(cab_cnt)*2
    if Specify_id=='No':
        if fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)":
            if giis=="0" and ngiis=="4" and UIO_Count=="64":
                var=int(cab_cnt)*2
            if giis=="0" and ngiis=="6" and UIO_Count=="96":
                var=int(cab_cnt)*2
            if giis=="4" and ngiis=="0" and UIO_Count=="64":
                var=int(cab_cnt)*2
            if giis=="6" and ngiis=="0" and UIO_Count=="96":
                var=int(cab_cnt)*2
            if giis=="2" and ngiis=="2" and UIO_Count=="64":
                var=int(cab_cnt)*2
            if giis=="2" and ngiis=="4" and UIO_Count=="96":
                var=int(cab_cnt)*2
            if giis=="4" and ngiis=="2" and UIO_Count=="96":
                var=int(cab_cnt)*2
        if fts=="Universal Marshalling, GI only (0-6)":
            if ugiis=="4" and UIO_Count=="64":
                var=int(cab_cnt)*2
            if ugiis=="6" and UIO_Count=="96":
                var=int(cab_cnt)*2
    return var
#Trace.Write(getpartCCSICC1011LR10(Product))
def getC300UpsCals_51202676_100(Product):

    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    UIO_Cnt=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    WRO=Product.Attr('C300_RG_UPC_WRO').GetValue()
    LLAI_cnt=Product.Attr('C300_RG_UPC_LLAI_Count').GetValue()

    qty=0
    i,j,k= 13,14,16

    if len(id_modifier)==26:
        i,j,k=14,15,17
    if len(id_modifier)==27:
        i,j,k=15,16,18

    if Specify_id=='Yes' and len(id_modifier)> k:
            if (id_modifier[i] == 'N' and (id_modifier[j] == '3' or id_modifier[j] == '6') and id_modifier[k] == '0'):
                qty=int(cab_cnt)*4
            if (id_modifier[i] == 'N' and id_modifier[j]== '9' and id_modifier[k] == '0'):
                qty=int(cab_cnt)*6
            if (id_modifier[i] == 'N' and id_modifier[j] == '0' and (id_modifier[k] == '1' or id_modifier[k] == '2' or id_modifier[k] == '3' or id_modifier[k] == '4')):
                qty=int(cab_cnt)*3
            if (id_modifier[i] == 'N' and id_modifier[j] == '0' and (id_modifier[k] == '5' or id_modifier[k] == '6' or id_modifier[k] == '7' or id_modifier[k] == '8')):
                qty=int(cab_cnt)*7

    if Specify_id=='No':
        if (WRO == 'No Panduit' and (UIO_Cnt == '32' or UIO_Cnt == '64') and LLAI_cnt == '0'):
            qty=int(cab_cnt)*4
        if (WRO == 'No Panduit' and UIO_Cnt== '96' and LLAI_cnt == '0'):
            qty=int(cab_cnt)*6
        if (WRO == 'No Panduit' and UIO_Cnt== '0' and (LLAI_cnt == '1' or LLAI_cnt == '2' or LLAI_cnt == '3' or LLAI_cnt == '4')):
            qty=int(cab_cnt)*3
        if (WRO == 'No Panduit' and UIO_Cnt== '0' and (LLAI_cnt == '5' or LLAI_cnt == '6' or LLAI_cnt == '7' or LLAI_cnt == '8')):
            qty=int(cab_cnt)*7

    return qty
def getC300UpsCals_51509194_500(Product):

    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    UIO_Cnt=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
    WRO=Product.Attr('C300_RG_UPC_WRO').GetValue()
    LLAI_cnt=Product.Attr('C300_RG_UPC_LLAI_Count').GetValue()

    qty=0
    i,j,k= 13,14,16

    if len(id_modifier)==26:
        i,j,k=14,15,17
    if len(id_modifier)==27:
        i,j,k=15,16,18

    if Specify_id=='Yes' and len(id_modifier)> k:
            if (id_modifier[i] == 'P' and (id_modifier[j] == '3' or id_modifier[j] == '6')):
                qty=int(cab_cnt)*1
            if (id_modifier[i] == 'P' and id_modifier[j]== '9'):
                qty=int(cab_cnt)*1
            if (id_modifier[i] == 'P' and (id_modifier[k] == '1' or id_modifier[k] == '2' or id_modifier[k] == '3' or id_modifier[k] == '4' or id_modifier[k] == '5' or id_modifier[k] == '6' or id_modifier[k] == '7' or id_modifier[k] == '8' )):
                qty=int(cab_cnt)*1

    if Specify_id=='No':
        if (WRO == 'Panduit' and (UIO_Cnt == '32' or UIO_Cnt == '64')):
            qty=int(cab_cnt)*1
        if (WRO == 'Panduit' and UIO_Cnt== '96'):
            qty=int(cab_cnt)*1
        if (WRO == 'Panduit' and (LLAI_cnt == '1' or LLAI_cnt == '2' or LLAI_cnt == '3' or LLAI_cnt == '4' or LLAI_cnt == '5' or LLAI_cnt == '6' or LLAI_cnt == '7' or LLAI_cnt == '8')):
            qty=int(cab_cnt)*1

    return qty


def getC300UpsCals_51156387_303(Product):

    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    CMT=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    ATR=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    PST=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    PSR=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    fts=Product.Attr('C300_RG_UPC_FTA').GetValue()
    Trace.Write(fts)
    giis=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
    ABD=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()

    qty=0
    i,j,k= 19,20,24

    if len(id_modifier)==26:
        i,j,k=20,21,25
    if len(id_modifier)==27:
        i,j,k=21,22,26

    if Specify_id=='Yes' and len(id_modifier)> j:
        if((id_modifier[12]=="N" and id_modifier[13]=="0" and (id_modifier[14]=="0" or id_modifier[14]=="2" or id_modifier[14]=="4" or id_modifier[14]=="6")) or (id_modifier[12]=="G" and (id_modifier[13]=="0" or id_modifier[13]=="2" or id_modifier[13]=="4" or id_modifier[13]=="6")) or id_modifier[12]=="X") and (id_modifier[1] == 'S' and id_modifier[2] == 'B' and id_modifier[i] == 'R' and id_modifier[j] == 'R' and id_modifier[k]== "N"):
            qty=int(cab_cnt)*1

    if Specify_id=='No':
        if ((fts=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and giis=="0") or fts=="Universal Marshalling, GI only (0-6)" or fts=="No Treatment") and (CMT == 'Stainless Steel, IP66' and ATR == 'With Fan, Max Ambient +55°C' and PST == '20A AC/DC ATDI Supply – Rack Mount' and PSR == 'REDUNDANT' and ABD=="No"):
            qty=int(cab_cnt)*1
    return qty

def getC300UpsCals_50154548_004(Product):

    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    PST=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    PSR=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()

    qty=0
    i,j= 19,20

    if len(id_modifier)==26:
        i,j=20,21
    if len(id_modifier)==27:
        i,j=21,22

    if Specify_id=='Yes' and len(id_modifier)> j:
            if (id_modifier[i] == 'R' and id_modifier[j] == 'R'):
                qty=int(cab_cnt)*1

    if Specify_id=='No':
        if (PST == '20A AC/DC ATDI Supply – Rack Mount' and PSR == 'REDUNDANT'):
                qty=int(cab_cnt)*1
    return qty

def getC300UpsCals_50185149_001(Product):

    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
    CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
    CNM_Exp=Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
    CNM_SFP=Product.Attr('C300_RG_UPC_CNM_Uplink_SFP_Type').GetValue()

    qty=0
    i,j,k,l= 4,7,8,9

    if Specify_id=='Yes' and len(id_modifier) > l :
        if ((id_modifier[i] == 'M' and id_modifier[j] == 'Y' and id_modifier[k] == 'Y' and id_modifier[l] == 'D') or (id_modifier[i] == 'T' and id_modifier[j] == 'Y' and id_modifier[k] == 'Y' and id_modifier[l] == 'D') or (id_modifier[i] == 'A' and id_modifier[j] == 'Y' and id_modifier[k] == 'Y' and id_modifier[l] == 'D') or (id_modifier[i] == 'B' and id_modifier[j] == 'Y' and id_modifier[k] == 'Y' and id_modifier[l] == 'D') or
        (id_modifier[i] == 'M' and id_modifier[j] == 'Y' and id_modifier[k] == 'N' and id_modifier[l] == 'D') or
        (id_modifier[i] == 'T' and id_modifier[j] == 'Y' and id_modifier[k] == 'N' and id_modifier[l] == 'D') or
        (id_modifier[i] == 'A' and id_modifier[j] == 'Y' and id_modifier[k] == 'N'and id_modifier[l] ==  'D') or
        (id_modifier[i] == 'B' and id_modifier[j] == 'Y' and id_modifier[k] == 'N'and id_modifier[l] ==  'D')):
            qty=int(cab_cnt)*2

    if Specify_id=='No':
        if ((CN100 == 'Non-Redundant with MM SFP' and  CNM == 'Red Pair CNM' and CNM_Exp == 'No Expansion Module' and CNM_SFP == 'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Redundant with MM SFP' and CNM == 'Red Pair CNM' and CNM_Exp == 'No Expansion Module' and CNM_SFP == 'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Non-Redundant' and CNM == 'Red Pair CNM' and CNM_Exp == 'No Expansion Module' and CNM_SFP == 'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Redundant' and CNM == 'Red Pair CNM' and CNM_Exp == 'No Expansion Module' and CNM_SFP == 'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Non-Redundant with MM SFP' and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules' and CNM_SFP == 'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Redundant with MM SFP' and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules' and  CNM_SFP ==  'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Non-Redundant' and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules'and CNM_SFP ==  'Red Pair CNM with MM 1G SFP, 300-500m')
        or
        (CN100 == 'Redundant' and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules'and CNM_SFP ==  'Red Pair CNM with MM 1G SFP, 300-500m')):
            qty=int(cab_cnt)*2

    return qty

def getC300UpsCals_50159943_004(Product):
    Specify_id = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_cnt = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()

    LLAI_cnt = Product.Attr('C300_RG_UPC_LLAI_Count').GetValue()

    qty = 0
    i = 16

    if len(id_modifier)==26:
        i=17
    if len(id_modifier)==27:
        i=18

    if Specify_id == 'Yes' and len(id_modifier) > i:
        if id_modifier[i] in ('0','1','2'):
            qty = int(cab_cnt)
    if Specify_id=='No':
        if LLAI_cnt in ('0', '1', '2'):
            qty = int(cab_cnt)
    return qty