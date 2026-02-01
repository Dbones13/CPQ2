#CXCPQ-45310
def getpart_51156387_302(Product):
    Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
    Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
    Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
    power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
    FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
    abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
    var6=0
    i,j=19,20
    i,j,k=19,20,24
    if len(id_modifier)>24:
        i,j,k= 19,20,24
    if len(id_modifier)>25:
        i,j,k= 20,21,25
    if len(id_modifier)>26:
        i,j,k=21,22,26
    if Specify_id=='Yes' and len(id_modifier)>20:
        if id_modifier[1]=='S' and id_modifier[2]=='A' and (id_modifier[12]=='X' or (id_modifier[12]=='G' and id_modifier[13]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='6') or (id_modifier[12]=='G' and id_modifier[13]=='2') or (id_modifier[12]=='G' and id_modifier[13]=='4') or (id_modifier[12]=='G' and id_modifier[13]=='6') ) and id_modifier[i]=='R' and id_modifier[j]=='R' and id_modifier[k]=='N':
            var6=int(cab_count)*1
    if Specify_id=="No":
        if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='Without Fan, Max Ambient +40°C' and Power_Supply_type=='20A AC/DC ATDI Supply – Rack Mount' and power_supply_red=='REDUNDANT'and abu_dhabi=='No' and (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' or FTA=='Universal Marshalling, GI only (0-6)' or FTA == 'No Treatment'):
            var6=int(cab_count)*1
    return var6
#Trace.Write(getpart_51156387_302(Product))