Service = Product.Attr('SC_Service_Product').GetValue()
if Service == 'System Evolution Program':
    Product.Attr('SC_Training_Match_Contract_Value').Allowed = False
    Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = False
    Product.Attr('SC_Training_Match_Contract_Value_SS').Allowed = False

#Product.Attr('SC Other Cost Details').Allowed = False

Ent = Product.GetContainerByName('SC_Entitlements')
Ent.Clear()
#OTU
Product.Attr('Contract_OTU_SESP').AssignValue(Service)

#Other Cost Details: To show only for "SESP Value Remote Plus" and "SESP Value Plus" product
#if Service == "SESP Value Remote Plus" or Service == "SESP Value Plus":
Product.Attr("SC Other Cost Details").Allowed = True

a = SqlHelper.GetList("select distinct Top 1000 Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = '{}' and IsMandatory = 'False' and Status='Active'".format(Service))
for row in a:
    if row.IsMandatory == 'FALSE':
        i = Ent.AddNewRow()
        i['Entitlement'] = row.Entitlement
Ent.Calculate()
###############3
Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue(str(Product.Attr('EnabledService_Entitlement').GetValue()))
if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
    Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.ReadOnly
else:
    Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.Editable
############ SO that it refreshes the asssets container
if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
    pr_servers = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
    pr_workstations = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Workstations'")[0].Price
    pr_windows = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Windows'")[0].Price
    pr_tpn = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-TPN NODES'")[0].Price
    pr_controllers = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-CONTROLLERS'")[0].Price
    pr_switches = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Switches'")[0].Price
    pr_scada = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
    pr_safety = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
    for i in Product.GetContainerByName('Asset_details_ServiceProd').Rows:
        rowListPrice = (int(i['Servers']) * int(pr_servers)) + ( int(i['Workstations']) if i['Workstations'] != '' else 0 ) * int(pr_workstations) + (int( i['Windows - Other']) if i['Windows - Other'] != '' else 0) * int(pr_windows) + (int(i['TPN Nodes']) if i['TPN Nodes'] != '' else 0 * int(pr_tpn)) + (int(i['Controllers']) if i['Controllers'] != '' else 0 * int(pr_controllers)) + (int(i['Switches']) if i['Switches'] != '' else 0 * int(pr_switches)) + (int(i['SCADA Servers']) if i['SCADA Servers'] != ''  else 0 * int(pr_scada)) + (int(i['Safety Manager']) if i['Safety Manager'] != '' else 0 * int(pr_safety))
        i['List Price'] = str(round(float(rowListPrice)))
    else:
        Product.GetContainerByName('Asset_details_ServiceProd').Calculate()
else:
    per_device = SqlHelper.GetFirst("select * from SC_HARDCODE_VALUES where Name = N'{0}'".format('Essentials % of Enhanced')).Value
    pr_servers = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
    pr_workstations = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Workstations'")[0].Price
    pr_windows = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Windows'")[0].Price
    pr_tpn = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-TPN NODES'")[0].Price
    pr_controllers = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-CONTROLLERS'")[0].Price
    pr_switches = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Switches'")[0].Price
    pr_scada = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
    pr_safety = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
    for i in Product.GetContainerByName('Asset_details_ServiceProd').Rows:
        rowListPrice = (float(float(i['Servers']) * float(pr_servers) if i['Servers'] != '' and i['Servers'].isdigit() else 0) * float(per_device)) + (float(float(i['Workstations']) * float(pr_workstations) if i['Workstations'] != '' and i['Workstations'].isdigit() else 0 ) * float(per_device)) + (float(float(i['Windows - Other']) * float(pr_windows)if i['Windows - Other'] != '' and i['Windows - Other'].isdigit() else 0) * float(per_device)) + (float(float(i['TPN Nodes']) * float(pr_tpn) if i['TPN Nodes'] != '' and i['TPN Nodes'].isdigit() else 0) * float(per_device)) + (float(float(i['Controllers']) * float(pr_controllers) if i['Controllers'] != '' and i['Controllers'].isdigit() else 0) * float(per_device)) + (float(float(i['Switches']) * float(pr_switches) if i['Switches'] != '' and i['Switches'].isdigit() else 0) * float(per_device)) + (float(float(i['SCADA Servers']) * float(pr_scada) if i['SCADA Servers'] != '' and i['SCADA Servers'].isdigit() else 0) * float(per_device)) + (float(float(i['Safety Manager']) * float(pr_safety) if i['Safety Manager'] != '' and i['Safety Manager'].isdigit() else 0) * float(per_device))
        i['List Price'] = str(round(float(rowListPrice),2))
    else:
        Product.GetContainerByName('Asset_details_ServiceProd').Calculate()
        
        
##############
if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
    for i in Product.Attr('Customer_has_cyber_enabledServicesModel').Values:
        if i.IsSelected == False:
            for j in Product.Attr('enhanced_and_no_vse_enabledServicesModel').Values:
                j.IsSelected = True
        else:
            for j in Product.Attr('enhanced_and_no_vse_enabledServicesModel').Values:
                j.IsSelected = False
else:
    for i in Product.Attr('enhanced_and_no_vse_enabledServicesModel').Values:
        i.IsSelected = False
    for k in Product.Attr('data_broker_needed_enabledServicesModel').Values:
                k.IsSelected = False
#################
for i in Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Values:
    if i.IsSelected == True:
        for j in Product.Attr('Customer_has_cyber_enabledServicesModel').Values:
            if j.IsSelected == False:
                for k in Product.Attr('essentail_select_the_option_enabledServicesModel').Values:    
                    k.IsSelected = True
            else:
                for i in Product.Attr('essentail_select_the_option_enabledServicesModel').Values:
                    i.IsSelected = False
    else:
        for i in Product.Attr('essentail_select_the_option_enabledServicesModel').Values:
            i.IsSelected = False
        for k in Product.Attr('data_broker_needed_enabledServicesModel').Values:
                k.IsSelected = False
#############################
for i in Product.Attr('enhanced_and_no_vse_enabledServicesModel').Values:
    for j in Product.Attr('essentail_select_the_option_enabledServicesModel').Values:
        if i.IsSelected == True or j.IsSelected == True:
            for k in Product.Attr('data_broker_needed_enabledServicesModel').Values:
                k.IsSelected = True
        else:
            for k in Product.Attr('data_broker_needed_enabledServicesModel').Values:
                k.IsSelected = False

####################
#UDC calc START
servers = 0
workstations = 0
window = 0
for i in Product.GetContainerByName('Asset_details_ServiceProd').Rows:
    if i['Servers'] or i['Workstations'] or i['Windows - Other']:
        servers += int(i['Servers'])
        workstations += int(i['Workstations'])
        window += int(i['Windows - Other'])
else:
    if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
        pr_servers = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price
        pr_workstations = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Workstations'")[0].Price
        pr_windows = SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Windows'")[0].Price
        val = (int(servers) * int(pr_servers) ) + (int(pr_workstations) * int(workstations)) + (int(pr_windows) * int(window))
        udc = SqlHelper.GetFirst("select * from sc_hardcode_values where Name = 'Asset/Agent Limit/UDC'").Value
        if int(val) >  int(udc):
            Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').AssignValue('')
            Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').AssignValue(str(round(float(val),2))) #give the attr name in here please
        else:
                Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').AssignValue('0.00')
        independantArea = Product.Attr('#_of_independent_"areas"_enabledServicesModel').GetValue()
        UDEService = Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').GetValue()
        Trace.Write(UDEService)
        if independantArea != "" and independantArea is not None and not independantArea.isalpha():
            #Trace.Write('ppppp')
            if UDEService != '':
                #Trace.Write('ppppp')
                if float(independantArea) > float(UDEService):
                    #Trace.Write('ppppp')
                    Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(independantArea),2)))
                else:
                    Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(UDEService),2)))
            else:
                #Product.Messages.Add('Value for UDC is calculated incorrected please contact your admin')
                Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(independantArea),2)))
        else:
            #Product.Messages.Add('Please provide the valid number.')
            Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')
    elif Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Essential':
        per_device = float(SqlHelper.GetFirst("select * from SC_HARDCODE_VALUES where Name = N'{0}'".format('Essentials % of Enhanced')).Value)
        pr_servers = int(SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Servers'")[0].Price)
        pr_workstations = int(SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Workstations'")[0].Price)
        pr_windows = int(SqlHelper.GetList("select * from SC_Hardcode_Price where Name = 'Enhanced-Windows'")[0].Price)
        val = (float(servers * pr_servers)  + float(workstations * pr_workstations) + float(window * pr_windows)) * per_device
        udc = SqlHelper.GetFirst("select * from sc_hardcode_values where Name = 'Asset/Agent Limit/UDC'").Value
        if int(val) > int(udc):
            Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').AssignValue(str(round(float(val),2))) #give the attr name in here please
        else:
            Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').AssignValue('0.00')
        independantArea = Product.Attr('#_of_independent_"areas"_enabledServicesModel').GetValue()
        UDEService = Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').GetValue()
        Trace.Write(UDEService)
        if independantArea != "" and independantArea is not None and not independantArea.isalpha() :
            #Trace.Write('ppppp')
            if UDEService != '':
                #Trace.Write('ppppp')
                if float(independantArea) > float(UDEService):
                    #Trace.Write('ppppp')
                    Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(independantArea),2)))
                else:
                    Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(UDEService),2)))
            else:
                #Product.Messages.Add('Value for UDC is calculated incorrected please contact your admin')
                Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(independantArea),2)))
        else:
            #Product.Messages.Add('Please provide the valid number.')
            Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')
            
    else:
        #Product.Messages.Add('Please select a valid service product, Enhanced or Essential ')
        pass

        #UDC CALC END
######################### UPDating licenses after udc update ###############3
independantArea = Product.Attr('#_of_independent_"areas"_enabledServicesModel').GetValue()
UDEService = Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').GetValue()
Trace.Write(UDEService)
if independantArea != "" and independantArea is not None and not independantArea.isalpha() :
    #Trace.Write('ppppp')
    if UDEService != '':
        #Trace.Write('ppppp')
        if float(independantArea) > float(UDEService):
            #Trace.Write('ppppp')
            Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(independantArea),2)))
        else:
            Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(UDEService),2)))
    else:
        #Product.Messages.Add('Value for UDC is calculated incorrected please contact your admin')
        Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue(str(round(float(independantArea),2)))
else:
    #Product.Messages.Add('Please provide the valid number.')
    Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')

#Matrix License

qty = 0
for i in Product.Attr('data_broker_needed_enabledServicesModel').Values:
    if i.IsSelected == True:
        if Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').GetValue() != '':
            qty = float(Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').GetValue())
        per_device = int(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value) + int(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)
        list_price = qty * per_device
        Product.Attr('Matrix License').AssignValue(str(round(float(list_price))))
    else:
        Log.Info('-----------------THE LICENSE SHOULD BE ZERO')
        qty = 0
        #per_device = int(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value) + int(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)
        #list_price = qty * per_device
        Product.Attr('Matrix License').AssignValue('0.00')
    
    
############################### SO THAT HEADER LABELS WILL BE IN SYNC WITH QUOTE CURRENCY ################
if Quote:
    currency = Quote.SelectedMarket.CurrencyCode
else:
    currency = 'USD'
Product.GetContainerByName('Asset_details_ServiceProd').TotalRow.Columns['List Price'].HeaderLabel = 'List Price' + " (" + currency +")"
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")