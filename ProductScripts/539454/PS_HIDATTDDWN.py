def getContainer(Name):
    return Product.GetContainerByName(Name)

def getattvalue(attName):
    return Product.Attr(attName)

opmBasicInfoCon = getContainer('OPM_Basic_Information')
futureExp = Product.Attr('MSID_Future_Experion_Release').GetValue()
expHwSelect = getattvalue('OPM_Experion_Server_Hardware_Selection')
accTestReq = getattvalue('OPM_Acceptance_Test_Required')
attr1 = getattvalue('OPM_Select_RESS_platform_configuration')
attr2 = getattvalue('OPM_Other_Servers_Hardware_Selection')

for Row in opmBasicInfoCon.Rows:
    if Row["OPM_Is_the_Experion_System_LCN_Connected"] == "Yes":
        if Product.Attr('OPM_Experion_Server_Hardware_Selection').Allowed:
            for value in expHwSelect.Values:
                if value.Display in ('DELL T160','DELL R260','DELL R450 STD TPM','DELL R450 STD','DELL R450 STD No TPM','DELL R360'):
                    value.Allowed = False
                if value.Display in ('DELL T360','Dell R740XL','HP DL360 G10'):
                    value.Allowed = True
    elif Row["OPM_Is_the_Experion_System_LCN_Connected"] == "No":
        if futureExp in ('R501','R511','R510'):
            if Product.Attr('OPM_Experion_Server_Hardware_Selection').Allowed:
                for value in expHwSelect.Values:
                    if value.Display in ('DELL T160','DELL R260','DELL R360'):
                        value.Allowed = False
                    if value.Display in ('Dell R740XL','HP DL360 G10','DELL T360','DELL R450 STD TPM','DELL R450 STD No TPM') :
                        value.Allowed = True
        elif futureExp == 'R520':
            if Product.Attr('OPM_Experion_Server_Hardware_Selection').Allowed:
                for value in expHwSelect.Values:
                    if value.Display in ('Dell R740XL','HP DL360 G10','DELL T360','DELL T160','DELL R260','DELL R450 STD TPM','DELL R450 STD No TPM','DELL R360') :
                        value.Allowed = True
        elif futureExp == 'R530':
            if Product.Attr('OPM_Experion_Server_Hardware_Selection').Allowed:
                for value in expHwSelect.Values:
                    if value.Display in ('DELL T360','DELL T160','DELL R260','DELL R450 STD TPM','DELL R360') :
                        value.Allowed = True
    if Row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] == "Yes":
        for value in accTestReq.Values:
            if value.Display in ('HAT','FAT','FAT & SAT','No'):
                value.Allowed = False
            if value.Display in ('HAT & SAT','SAT'):
                value.Allowed = True
    elif Row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] == "No":
        for value in accTestReq.Values:
            if value.Display in ('HAT','FAT','FAT & SAT','No','HAT','HAT & SAT','SAT'):
                value.Allowed = True
    break

if futureExp in ('R501','R511','R510'):
    if Product.Attr('OPM_Select_RESS_platform_configuration').Allowed:
        for value in attr1.Values:
            if value.Display in ('DELL T160','DELL R260'):
                value.Allowed = False
            if value.Display in ('Dell R740XL','HP DL360 G10','DELL T360','DELL R450 STD TPM','DELL R450 STD No TPM') :
                value.Allowed = True
    if Product.Attr('OPM_Other_Servers_Hardware_Selection').Allowed:
        for value in attr2.Values:
            if value.Display in ('DELL T160','DELL R260','DELL R360'):
                value.Allowed = False
            if value.Display in ('HP DL360 G10','DELL T360','DELL R450 STD TPM','DELL R450 STD No TPM'):
                value.Allowed = True

elif futureExp == 'R520':
    if Product.Attr('OPM_Select_RESS_platform_configuration').Allowed:
        for value in attr1.Values:
            if value.Display in ('DELL T160','DELL R260','HP DL360 G10','Dell R740XL','DELL T360','DELL R450 STD TPM','DELL R450 STD No TPM') :
                value.Allowed = True
    if Product.Attr('OPM_Other_Servers_Hardware_Selection').Allowed:
        for value in attr2.Values:
            if value.Display in ('DELL T160','DELL R260','HP DL360 G10','DELL T360','DELL R450 STD TPM','DELL R450 STD No TPM','DELL R360') :
                value.Allowed = True

fut_rel = Product.Attr('MSID_Future_Experion_Release').GetValue()
con2 = Product.GetContainerByName('OPM_Basic_Information')
if con2.Rows.Count > 0:
    for row in con2.Rows:
        Trace.Write("sssssss")
        lcn = row["OPM_Is_the_Experion_System_LCN_Connected"]
        sshw = row["OPM_Servers_and_Stations_HW_replace_needed"]
        ress = row["OPM_RESS_Migration_in_scope"]
        Trace.Write("Print1111-"+str(lcn)+"   "+str(sshw)+"  "+str(ress))
        break
    if lcn == 'Yes' or sshw == 'Yes' or ress == 'Yes' :
        attr1 = Product.Attr('OPM_ACET_EAPP_Server_Hardware_Selection')
        attr2 = Product.Attr('OPM_Other_Servers_Hardware_Selection')
        attr3 = Product.Attr('OPM_Experion_Server_Hardware_Selection')
        attr4 = Product.Attr('OPM_Select_RESS_platform_configuration')
        if fut_rel in ('R520','R530','R511','R510'):
            if Product.Attr('OPM_ACET_EAPP_Server_Hardware_Selection').Allowed:
                for value in attr1.Values:
                    if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                        value.Allowed=False
            if Product.Attr('OPM_Other_Servers_Hardware_Selection').Allowed:
                for value in attr2.Values:
                    if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                        value.Allowed=False
            if Product.Attr('OPM_Experion_Server_Hardware_Selection').Allowed:
                for value in attr3.Values:
                    if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                        value.Allowed=False
            if Product.Attr('OPM_Select_RESS_platform_configuration').Allowed:
                for value in attr4.Values:
                    if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                        value.Allowed=False
        attr5 = Product.Attr('OPM_EST_Tower_Hardware_Selection')
        attr6 = Product.Attr('OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection')
        flag=True if lcn=="Yes" and sshw=="Yes" else False
        if fut_rel not in ('R520','R530'):
            if Product.Attr('OPM_EST_Tower_Hardware_Selection').Allowed:
                for value in attr5.Values:
                    if value.Display in ('HP Z4 G5','Dell T5860XL'):
                        value.Allowed = False
                    else:
                        if value.Display=="HP Z4 G4 MLK" and flag:
                            value.Allowed=False
                        else:
                            value.Allowed = True
            if Product.Attr('OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection').Allowed:
                for value in attr6.Values:
                    if value.Display in ('HP Z4 G5','Dell T5860XL'):
                        value.Allowed = False
                    else:
                        if value.Display=="HP Z4 G4 MLK" and flag:
                            value.Allowed=False
                        else:
                            value.Allowed = True
        elif fut_rel == 'R530':
            if Product.Attr('OPM_EST_Tower_Hardware_Selection').Allowed:
                for value in attr5.Values:
                    if value.Display in ('HP Z4 G5','Dell T5860XL'):
                        value.Allowed = True
                    else:
                        value.Allowed = False
            if Product.Attr('OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection').Allowed:
                for value in attr6.Values:
                    if value.Display in ('HP Z4 G5','Dell T5860XL'):
                        value.Allowed = True
                    else:
                        value.Allowed = False
        else:
            if Product.Attr('OPM_EST_Tower_Hardware_Selection').Allowed:
                for value in attr5.Values:
                    if value.Display in ('HP Z4 G4 MLK','Dell T5820XL'):
                        value.Allowed = True
                    else:
                        value.Allowed = False
            if Product.Attr('OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection').Allowed:
                for value in attr6.Values:
                    if value.Display in ('HP Z4 G4 MLK','Dell T5820XL'):
                        value.Allowed = True
                    else:
                        value.Allowed = False
        if fut_rel in ('R520','R530','R511','R510'):
            attr1 = Product.Attr('OPM_ACET_EAPP_Server_Hardware_Selection')
            attr3 = Product.Attr('OPM_Experion_Server_Hardware_Selection')
            if Product.Attr('OPM_ACET_EAPP_Server_Hardware_Selection').Allowed:
                for value in attr1.Values:
                    if value.Display in ('Dell R740XL'):
                        value.Allowed = False
            if Product.Attr('OPM_Experion_Server_Hardware_Selection').Allowed:
                for value in attr3.Values:
                    if value.Display in ('Dell R740XL'):
                        value.Allowed = False
    if ress == 'Yes' and fut_rel in ('R520','R530','R511','R510'):
        attr4 = Product.Attr('OPM_Select_RESS_platform_configuration')
        if Product.Attr('OPM_Select_RESS_platform_configuration').Allowed:
            for value in attr4.Values:
                if value.Display in ('Dell R740XL'):
                    value.Allowed = False