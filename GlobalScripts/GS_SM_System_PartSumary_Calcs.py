from math import ceil
def get_int(val):
    if val:
        return int(val)
    return 0

def get_System_parts(Product,parts_dict):
    #CXCPQ-33231 AND CXCPQ-33219 added by Lahu.
    SM_Controller_Simulation_License= Product.GetContainerByName('SM_Common_Questions').Rows[0].GetColumnByName('SM_Controller_Simulation_License').Value
    SM_Historian_Server_Upgrade= Product.GetContainerByName('SM_Common_Questions').Rows[0].GetColumnByName('SM_Historian_Server_Upgrade').Value
    SM_Physical_Media_Kit= Product.GetContainerByName('SM_Common_Questions').Rows[0].GetColumnByName('SM_Physical_Media_Kit').Value
    SM_Builder_Concurrent_User_License= Product.GetContainerByName('SM_Common_Questions').Rows[0].GetColumnByName('SM_Builder_Concurrent_User_License').Value
    if int(SM_Controller_Simulation_License) > 0:
        qty = SM_Controller_Simulation_License
        parts_dict["FS-SCSIML01"] = {'Quantity' : qty, 'Description': 'SC S300 CONTROLLER SIMULATION LICENSE'}
    if int(SM_Historian_Server_Upgrade) > 0:
        qty = SM_Historian_Server_Upgrade
        parts_dict["FS-SOEUP-4011"] = {'Quantity' : qty, 'Description': 'UPGRADE SOE to FS-SOESERV-4001'}
    #CXCPQ-33221 AND CXCPQ-33232 added by Lahu.
    if int(SM_Physical_Media_Kit) > 0:
        qty = SM_Physical_Media_Kit
        parts_dict["FS-SCSBP212"] = {'Quantity' : qty, 'Description': 'SC SB R212 PHYSICAL MEDIAKIT'}
    if int(SM_Builder_Concurrent_User_License) > 0:
        qty = SM_Builder_Concurrent_User_License
        parts_dict["FS-SCSBL212"] = {'Quantity' : qty, 'Description': 'SC SB R212 CONCURENT USER LICENSE'}
        qty= 1
        parts_dict["FS-SCSBE212"] = {'Quantity' : qty, 'Description': 'SC SB R212 EL.SOFTW.DISTR. MEDIAKIT'}
    
    SM_Historian_Basic_Server_1Client = Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("SM_Historian_Basic_Server_1Client").DisplayValue
    if SM_Historian_Basic_Server_1Client == '100':
        parts_dict["FS-SH2021-0011"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC+SERVER(+1CLIENT) 100 T'}
    elif SM_Historian_Basic_Server_1Client == '500':
        parts_dict["FS-SH2021-0012"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC+SERVER(+1CLIENT) 500 T'}
    elif SM_Historian_Basic_Server_1Client == '2500':
        parts_dict["FS-SH2021-0013"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC+SERVER(+1CLIENT) 2500 T'}
    elif SM_Historian_Basic_Server_1Client == '10000':
        parts_dict["FS-SH2021-0014"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC+SERVER(+1CLIENT) 10000 T'}
    elif SM_Historian_Basic_Server_1Client == '50000':
        parts_dict["FS-SH2021-0015"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC+SERVER(+1CLIENT) 50000 T'}
    
    SM_Historian_Basic_Database_Ext = Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("SM_Historian_Basic_Database_Ext").DisplayValue
    if SM_Historian_Basic_Database_Ext=='500':
        parts_dict["FS-SH2021-1002"] = {'Quantity' : 1, 'Description': 'SH R202.1 DB EXTENS. 100 TO 500 TAGS'}
    elif SM_Historian_Basic_Database_Ext == '2500':
        parts_dict["FS-SH2021-1003"] = {'Quantity' : 1, 'Description': 'SH R202.1 DB EXTENS. 100 TO 2500 TAGS'}
    elif SM_Historian_Basic_Database_Ext == '10000':
        parts_dict["FS-SH2021-1004"] = {'Quantity' : 1, 'Description': 'SH R202.1 DB EXTENS. 100 TO 10000 TAGS'}
    elif SM_Historian_Basic_Database_Ext == '50000':
        parts_dict["FS-SH2021-1005"] = {'Quantity' : 1, 'Description': 'SH R202.1 DB EXTENS. 100 TO 50000 TAGS'}
    
    #CXCPQ-33214
    SM_Historian_Basic_SW = Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("SM_Historian_Basic_SW").DisplayValue
    if SM_Historian_Basic_SW == '100':
        parts_dict["FS-SH2021-0001"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC 100 TAGS'}
    elif SM_Historian_Basic_SW == '500':
        parts_dict["FS-SH2021-0002"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC 500 TAGS'}
    elif SM_Historian_Basic_SW == '2500':
        parts_dict["FS-SH2021-0003"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC 2500 TAGS'}
    elif SM_Historian_Basic_SW == '10000':
        parts_dict["FS-SH2021-0004"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC 10000 TAGS'}
    elif SM_Historian_Basic_SW == '50000':
        parts_dict["FS-SH2021-0005"] = {'Quantity' : 1, 'Description': 'SH R202.1 BASIC 50000 TAGS'}
    
   
    return parts_dict