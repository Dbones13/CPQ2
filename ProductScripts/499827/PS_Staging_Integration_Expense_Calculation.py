#System cabinets and Marshalling Cabinets Calc:
def getInt(Var):
    if Var:
        return int(Var)
    else: return 0

if Product.GetContainerByName('CE_SystemGroup_Cont'):
    Sys_Cont = Product.GetContainerByName('CE_SystemGroup_Cont').Rows
else:
    Sys_Cont = []
Products = ['ControlEdge UOC System','C300 System','Safety Manager ESD','Safety Manager FGS','Safety Manager BMS','Safety Manager HIPPS','ControlEdge PLC System','ControlEdge RTU System']
C300_Part = UOC_Part = RTU_Part = PLC_Part = SM_ESD_Part = SM_FSG_Part = SM_BMS_Part = SM_HIPPS_Part = int(0)
#UOC_Part = int(0)
for sys in Sys_Cont:
    A = sys.Product.GetContainerByName('CE_System_Cont')
    for SG_Child in A.Rows:
        if SG_Child['Product Name'] in Products :
            if SG_Child['Product Name'] == 'C300 System':
                SG = SG_Child.Product.GetContainerByName('Series_C_Control_Groups_Cont')
                for SG_C300 in SG.Rows:
                    C300_Part += (getInt(SG_C300['C300_Sys_Cabinets'])+getInt(SG_C300['C300_Sys_Cabinets_RG']))
            elif SG_Child['Product Name'] == 'ControlEdge UOC System':
                SG = SG_Child.Product.GetContainerByName('UOC_ControlGroup_Cont')
                for SG_UOC in SG.Rows:
                    UOC_Part += (getInt(SG_UOC['staging_UOC_Num_of_Sys_Cabinets'])+getInt(SG_UOC['Staging_UOC_Num_of_Sys_Cabinets_RG']))
            elif SG_Child['Product Name'] == 'Safety Manager ESD':
                SG = SG_Child.Product.GetContainerByName('SM_ControlGroup_Cont')
                for SG_SM_ESD in SG.Rows:
                    SM_ESD_Part += (getInt(SG_SM_ESD['staging_SM_Sys_Cabinets']) + getInt(SG_SM_ESD['staging_SM_Sys_Cabinets_RG']))
            elif SG_Child['Product Name'] == 'Safety Manager FGS':
                SG = SG_Child.Product.GetContainerByName('SM_ControlGroup_Cont')
                for SG_SM_FGS in SG.Rows:
                    SM_FSG_Part += (getInt(SG_SM_FGS['staging_SM_Sys_Cabinets']) + getInt(SG_SM_FGS['staging_SM_Sys_Cabinets_RG']))
            elif SG_Child['Product Name'] == 'Safety Manager BMS':
                SG = SG_Child.Product.GetContainerByName('SM_ControlGroup_Cont')
                for SG_SM_BMS in SG.Rows:
                    SM_BMS_Part += (getInt(SG_SM_BMS['staging_SM_Sys_Cabinets']) + getInt(SG_SM_BMS['staging_SM_Sys_Cabinets_RG']))
                
            elif SG_Child['Product Name'] == 'Safety Manager HIPPS':
                SG = SG_Child.Product.GetContainerByName('SM_ControlGroup_Cont')
                for SG_SM_HIPPS in SG.Rows:
                    SM_HIPPS_Part += (getInt(SG_SM_HIPPS['staging_SM_Sys_Cabinets']) + getInt(SG_SM_HIPPS['staging_SM_Sys_Cabinets_RG']))
                
            elif SG_Child['Product Name'] == 'ControlEdge PLC System':
                SG = SG_Child.Product.GetContainerByName('PLC_ControlGroup_Cont')
                for SG_PLC in SG.Rows:
                    PLC_Part += (getInt(SG_PLC['staging_PLC_Num_of_Sys_Cabinets'])+getInt(SG_PLC['staging_PLC_Num_of_Sys_Cabinets_RG']))
            elif SG_Child['Product Name'] == 'ControlEdge RTU System':
                SG = SG_Child.Product.GetContainerByName('RTU_ControlGroup_Cont')
                for SG_RTU in SG.Rows:
                    RTU_Part += getInt(SG_RTU['staging_RTU_Num_of_Sys_Cabinets'])

System_cabinet = C300_Part + UOC_Part + RTU_Part + PLC_Part + SM_ESD_Part + SM_FSG_Part + SM_BMS_Part + SM_HIPPS_Part
#To Calculate Expense Type:
def final_quantity(r,oldValue):
    if oldValue != r['Calculated_Values']:
        r['Final_Values'] = r['Calculated_Values']
Cables = float(0)
TD = int(0)
PFAT = int(0)
FAT = int(0)
Area_ft = int(0)
Area_m = int(0)
F = int(0)
D = int(0)
Hrs = int(0)
H = int(0)

if Product.GetContainerByName('Staging_and_Integration_Expense_Cont'):
    Expense_Cont=Product.GetContainerByName('Staging_and_Integration_Expense_Cont').Rows
else:
    Expense_Cont = []
if Product.GetContainerByName('ExpProject_Que_Right'):
    PM_Cont = Product.GetContainerByName('ExpProject_Que_Right').Rows
else:
    PM_Cont = []
for PM in PM_Cont:
    FAT = int(PM['FAT Duration in weeks'])
if Product.GetContainerByName('Staging_and_Integration_Cont'):
    Cont=Product.GetContainerByName('Staging_and_Integration_Cont').Rows
else:
    Cont = []

for r in Cont:
    oldValue = r['Calculated_Values']
    if r['Questions'] == 'Number of System Cabinets':
        r['Calculated_Values'] = str(System_cabinet)
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Network Cabinets':
        #r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(Staging_Network_and_Server_Cabinet_Count) )*>')
        r['Calculated_Values'] = str(0)
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Auxiliary Cabinets':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_Auxiliary_Cabinet_Count) )*>')
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Operator Console Sections':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_Number_of_Operator_Console_Sections) )*>')
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Console Sections with Hardwired IO':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_Number_of_Console_Sections_with_Hardwired) )*>')
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Stations Console (Desk/Orion) <span class="sap-icon" style="color:#0a6ed1" data-toggle="tooltip" title="Enter the count of Stations in Orion Console and Desk console"></span>':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_Number_of_Stations_Console_system_group_ne) )*>')
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Server Cabinets':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Math.Sum(<*CTX( Container(CE_SystemGroup_Cont).Sum(Staging_Network_and_Server_Cabinet_Count) )*>,<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_experion_enterprise_partsummary_calc_sysGr) )*>) )*>')
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Marshalling Cabinets':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_Marshalling_Cabinets_c300_rtu_uoc_SM_sysgr) )*>')
        final_quantity(r,oldValue)
    elif r['Questions'] == 'Number of Experion Servers Console':
        r['Calculated_Values'] = TagParserProduct.ParseString('<*CTX( Container(CE_SystemGroup_Cont).Sum(staging_Number_of_Experion_Servers_Sys_grp) )*>')
        final_quantity(r,oldValue)
if Cont:
    Product.GetContainerByName('Staging_and_Integration_Cont').Calculate()

if Product.GetContainerByName('Staging_and_Integration_Cont'):
    Cont=Product.GetContainerByName('Staging_and_Integration_Cont').Rows
else:
    Cont = []

for r in Cont:
    if r['Final_Values'] == '':
        r['Final_Values'] = str(0)
    if r['Questions'] == 'Interconnecting IO Cables':
        Cables = int(r['Final_Values'])
    elif r['Questions'] not in ['Pre-FAT Duration (in weeks)','FAT Duration','Interconnecting IO Cables']:
        TD = TD + float(r['Final_Values'])
    elif r['Questions'] == 'Pre-FAT Duration (in weeks)':
        PFAT = int(r['Final_Values'])
#sq feet        
if Product.Attributes.GetByName('Staging_and_Integration_Floor_Area_Unit') and Product.Attributes.GetByName('Staging_and_Integration_Floor_Area_Unit').GetValue() == 'Square Feet':       
        
    if TD < 30:
        F = int(1)
    elif TD < 60 :
        F = int(2)
    else:
        F = int(3)
    D =  PFAT+FAT+(3*F)
    if D > 0 and TD > 0:
        Area_ft = round((TD * D * 3.2 * 10.76),0)
    else:
        Area_ft = int(0)
#Sq meter    
if Product.Attributes.GetByName('Staging_and_Integration_Floor_Area_Unit') and Product.Attributes.GetByName('Staging_and_Integration_Floor_Area_Unit').GetValue() == 'Square Meter':
    if TD < 30:
        F = int(1)
    elif TD < 60 :
        F = int(2)
    else:
        F = int(3)
    D =  PFAT+FAT+(3*F) 
    if D > 0 and TD > 0:
        Area_m = round(TD * D * 3.2 ,1)
    else:
        Area_m = int(0)
#Project Coordinator
if TD < 30:
    F = int(1)
elif TD < 60:
    F = int(2)
else:
    F = int(3)
D =  PFAT+FAT+(3*F)
H = TD*1 + D*8 + FAT*4
if D > 0 and TD > 0 and H<=40:
    Hrs = 40
elif D >=0 and TD >= 0 and H > 40:
    Hrs = H
else:
    Hrs = 0 
#To populate Expense Container
for Exp in Expense_Cont:
    oldValue1 = Exp['Calculated_Hrs_Area']
    if Exp['Expense_Type'] == 'Assembler/Wiremen Support':
        C = round(Cables*0.75,2) 
        if oldValue1 != str(C):
            Exp['Final_Hrs_Area'] =str(C)
            Exp['Calculated_Hrs_Area'] =  Exp['Final_Hrs_Area'] 
    elif Exp['Expense_Type'] == 'Technician Support':
        TS = round(TD*7,2) 
        if oldValue1 != str(TS):
            Exp['Final_Hrs_Area'] = str(TS)
            Exp['Calculated_Hrs_Area'] =  Exp['Final_Hrs_Area']
    elif  Exp['Expense_Type'] == 'Integration Floor Space-Sq Feet':
        if oldValue1 != str(Area_ft):
            Exp['Final_Hrs_Area'] = str(Area_ft)
            Exp['Calculated_Hrs_Area'] =  Exp['Final_Hrs_Area']
    elif   Exp['Expense_Type'] == 'Integration Floor Space-Sq Meter':
        if oldValue1 != str(Area_m):
            Exp['Final_Hrs_Area'] = str(Area_m)
            Exp['Calculated_Hrs_Area'] =  Exp['Final_Hrs_Area']
    elif  Exp['Expense_Type'] == 'Project Co-ordinator/Leader Support':
        if oldValue1 != str(round(Hrs,2)):
            Exp['Final_Hrs_Area'] = str(round(Hrs,2))
            Exp['Calculated_Hrs_Area'] =  Exp['Final_Hrs_Area']
#Expense_Cont.Calculate()
# to populate Unit price:

quoteCurrency = Quote.SelectedMarket.CurrencyCode if Quote else ''
# Expense_Cont=Product.GetContainerByName('Staging_and_Integration_Expense_Cont')
if Product.Attributes.GetByName('Staging_and_Integration_Center'):
    center = Product.Attr('Staging_and_Integration_Center').GetValue()
    center_table = SqlHelper.GetList("Select Integration_Center,Particular,Unit_Cost,Unit_List_Price,Currency from STAGING_INTEGRATION_DATA where Integration_Center='{}'".format(center))
else:
    center_table = []

exchange_rate = '0'
for y in center_table:
    query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(y.Currency,quoteCurrency))
    if y.Currency == quoteCurrency:
        exchange_rate = 1
    else:
        exchange_rate = query.Exchange_Rate
    break
for x in center_table:
        for Expense in Expense_Cont:
            if x.Particular in Expense['Expense_Type']:
                final_Unit_Cost = float(x.Unit_Cost)*float(exchange_rate)
                Expense['Unit_Cost'] = str(final_Unit_Cost)
                Expense['Final_Unit_Cost'] = str(final_Unit_Cost)
                final_Unit_List_Price = float(x.Unit_List_Price)*float(exchange_rate)
                Expense['Unit_List_Price'] = str(final_Unit_List_Price)
                Expense['Final_Unit_List_Price'] = str(final_Unit_List_Price)
                final = round(float(Expense['Final_Hrs_Area']))
                if Expense['Final_Unit_Cost'] != 0:
                    Expense['Total_Cost'] = str(float(Expense['Final_Unit_Cost'])*float(final))
                else:
                    Expense['Total_Cost'] = str(float(Expense['Unit_Cost'])*float(final))
                if Expense['Final_Unit_List_Price'] != 0:
                    Expense['Total_List_Price'] = str(float(Expense['Final_Unit_List_Price'])*float(final))
                else:
                    Expense['Total_List_Price'] = str(float(Expense['Unit_List_Price'])*float(final))
if Expense_Cont:
    Product.GetContainerByName('Staging_and_Integration_Expense_Cont').Calculate()