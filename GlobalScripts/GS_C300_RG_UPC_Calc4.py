def getpartsUPC(Product):
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
    fts=Product.Attr('C300_RG_UPC_FTA').GetValue()
    #Trace.Write(Abu_Dhabi_Bld_Loc)
    a,b,h,i,j,k=12,0,0,19,20,24
    if len(id_modifier)==26:
        a,b,h,i,j,k=12,13,0,20,21,25
    if len(id_modifier)==27:
        a,b,h,i,j,k=12,13,14,21,22,26
    var=var1=var2=var3=var4=var5=var6=var7=0
    if Specify_id=='Yes'and len(id_modifier)>21:
        if id_modifier[i]=='Q' and id_modifier[j]=='R':
            var=int(cab_cnt)*1
        if (id_modifier[a]=='X' or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='0')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='2') or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='4')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='6') or (id_modifier[a]=='G' and id_modifier[b]=='0') or (id_modifier[a]=='G' and id_modifier[b]=='2') or (id_modifier[a]=='G' and id_modifier[b]=='4') or (id_modifier[a]=='G' and id_modifier[b]=='6')):
            if id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[i]=='D' and id_modifier[j]=='R' and id_modifier[k]=='Y':
                var1=int(cab_cnt)*1
        if id_modifier[i]=='A' and id_modifier[j]=='R':
            var2=int(cab_cnt)*1
        if (id_modifier[a]=='X' or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='0')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='2') or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='4')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='6') or (id_modifier[a]=='G' and id_modifier[b]=='0') or (id_modifier[a]=='G' and id_modifier[b]=='2') or (id_modifier[a]=='G' and id_modifier[b]=='4') or (id_modifier[a]=='G' and id_modifier[b]=='6')):
            if id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[i]=='D' and id_modifier[j]=='R' and id_modifier[k]=='N':
                var3=int(cab_cnt)*1
        if id_modifier[1]=='S':
            var4=int(cab_cnt)*1
        #CXCPQ-45313
        if (id_modifier[a]=='X' or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='0')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='2') or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='4')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='6') or (id_modifier[a]=='G' and id_modifier[b]=='0') or (id_modifier[a]=='G' and id_modifier[b]=='2') or (id_modifier[a]=='G' and id_modifier[b]=='4') or (id_modifier[a]=='G' and id_modifier[b]=='6')):
            if id_modifier[1]=='S' and id_modifier[2]=='B' and id_modifier[i]=='A' and id_modifier[j]=='R'and id_modifier[k]=='N':
                var5=int(cab_cnt)*1
        #CXCPQ-45333
        if (id_modifier[a]=='X' or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='0')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='2') or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='4')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='6') or (id_modifier[a]=='G' and id_modifier[b]=='0') or (id_modifier[a]=='G' and id_modifier[b]=='2') or (id_modifier[a]=='G' and id_modifier[b]=='4') or (id_modifier[a]=='G' and id_modifier[b]=='6')):
            if id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[i]=='Q' and id_modifier[j]=='R' and id_modifier[k]=='Y':
                var6=int(cab_cnt)*1
        #CXCPQ-45329
        if (id_modifier[a]=='X' or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='0')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='2') or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='4')or (id_modifier[a]=='N' and id_modifier[b]=='0' and id_modifier[h]=='6') or (id_modifier[a]=='G' and id_modifier[b]=='0') or (id_modifier[a]=='G' and id_modifier[b]=='2') or (id_modifier[a]=='G' and id_modifier[b]=='4') or (id_modifier[a]=='G' and id_modifier[b]=='6')):
            if id_modifier[1]=='S' and id_modifier[2]=='A' and id_modifier[i]=='A' and id_modifier[j]=='R' and id_modifier[k]=='Y':
                var7=int(cab_cnt)*1
    if Specify_id=='No':
        var4=int(cab_cnt)*1
        if Supply_Type=="20A AC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT":
            var=int(cab_cnt)*1
        if fts!="Weidmuller Marshalling":
            if Cab_type=="Stainless Steel, IP66" and Ambient_Temp=="With Fan, Max Ambient +55°C" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi_Bld_Loc=="Yes":
                var1=int(cab_cnt)*1
        if Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT":
            var2=int(cab_cnt)*1
        if fts!="Weidmuller Marshalling":
            if Cab_type=="Stainless Steel, IP66" and Ambient_Temp=="Without Fan, Max Ambient +40°C" and Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi_Bld_Loc=="No":
                var3=int(cab_cnt)*1
        #CXCPQ-45313
        if fts!="Weidmuller Marshalling":
            if Cab_type=="Stainless Steel, IP66" and Ambient_Temp=="With Fan, Max Ambient +55°C" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi_Bld_Loc=="No":
                var5=int(cab_cnt)*1
        #CXCPQ-45333
        if fts!="Weidmuller Marshalling":
            if Cab_type=="Stainless Steel, IP66" and Ambient_Temp=="Without Fan, Max Ambient +40°C" and Supply_Type=="20A AC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi_Bld_Loc=="Yes":
                var6=int(cab_cnt)*1
        #CXCPQ-45329
        if fts!="Weidmuller Marshalling":
            if Cab_type=="Stainless Steel, IP66" and Ambient_Temp=="Without Fan, Max Ambient +40°C" and Supply_Type=="25A AC/DC ATDI Supply" and Supply_Red=="REDUNDANT" and Abu_Dhabi_Bld_Loc=="Yes":
                var7=int(cab_cnt)*1
    return var,var1,var2,var3,var4,var5,var6,var7
#Trace.Write(getpartsUPC(Product))