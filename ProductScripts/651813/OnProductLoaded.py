#Populate container attributes with applicable records on load of product
def getContainer(Name):
    return Product.GetContainerByName(Name)
Product.Attributes.GetByName('HCI_PHD_Prd_Family').SelectDisplayValue('Enterprise Data Management')

if Quote.GetCustomField('R2QFlag').Content != 'Yes':
    Product.Attributes.GetByName('HCI_PHD_GES_Location').SelectDisplayValue('GES India')
ges_loc = str(Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').GetValue()) if Product.Attributes.GetByName('AR_HCI_FO_ENG_Executioncountry').GetValue() else 'United States'
country_codes = {'GES China':'CN','GES India':'IN','GES Uzbekistan':'UZ'}
cuntry_code = country_codes.get(str(Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue()))
Product.Attributes.GetByName('AR_HCI_No_FO_ENG').SelectDisplayValue('1')
noOfSys=1
cont=Product.GetContainerByName('HCI_PHD_Fo_Eng')
cont.Clear()
for i in range(0,noOfSys):
    row=cont.AddNewRow(False)
    row['Engineer']='FO Eng '+str(i+1)
    row.GetColumnByName('Activity Type').ReferencingAttribute.SelectDisplayValue('PHD Sr Eng')
    row.GetColumnByName('Execution Country').ReferencingAttribute.SelectDisplayValue('United States')
    row['Number of trips per engineer']='1'
    row.ApplyProductChanges()
    row.Calculate()
Product.AllowAttr('HCI_PHD_AddSelected')
Product.AllowAttrValues('HCI_Product_Choices', 'PHD_Labor', 'Uniformance_Insight_Labor', 'AFM_Labor')
prods =["PHD_Labor"]
attrs = ["HCI_Labor_Prod_Cont","HCI_Labor_common_prj_input1","HCI_Labor_common_prj_input2","HCI_Labor_prj_mng_lbr_input"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        if attr == "HCI_Labor_Prod_Cont":
            '''for prod in prods: 
                prd_lbr = container.AddNewRow(False)
                prd_lbr['Product'] = prod'''
        elif attr == "HCI_Labor_prj_mng_lbr_input":
            roles = ["Project Management", "Project Management - GES", "Project Administration", "Project Controls","Lead Engineering"]
            rolesDefaultValue={}
            if Quote.GetCustomField('R2QFlag').Content != 'Yes':
                rolesDefaultValue['Project Management']={'Per':'10','Activity':'Project Manager','country':'United States'}
                rolesDefaultValue['Project Management - GES']={'Per':'10','Activity':'ADV GES PM-IN','country':'United States'}
                rolesDefaultValue['Project Administration']={'Per':'7','Activity':'Project Admin','country':'United States'}
                rolesDefaultValue['Project Controls']={'Per':'3','Activity':'SYS PCA-Specialist','country':'United States'}
                rolesDefaultValue['Lead Engineering']={'Per':'10','Activity':'PHD Prin Eng','country':'United States'}
            else:
                rolesDefaultValue['Project Management']={'Per':'10','Activity':'Sr Project Manager','country':ges_loc}
                rolesDefaultValue['Project Management - GES']={'Per':'10','Activity':'ADV GES PM-'+str(cuntry_code)+'','country':ges_loc}
                rolesDefaultValue['Project Administration']={'Per':'0','Activity':'Project Admin','country':ges_loc}
                rolesDefaultValue['Project Controls']={'Per':'3','Activity':'SYS PCA-Specialist','country':ges_loc}
                rolesDefaultValue['Lead Engineering']={'Per':'10','Activity':'PHD Prin Eng','country':ges_loc}
            for role in roles:
                prj_manage_lbr = container.AddNewRow(False)
                prj_manage_lbr.GetColumnByName('Role').ReferencingAttribute.SelectDisplayValue(role)
                prj_manage_lbr['Percentage']=rolesDefaultValue[role]['Per']
                prj_manage_lbr.GetColumnByName('Activity_Type').ReferencingAttribute.SelectDisplayValue(rolesDefaultValue[role]['Activity'])
                prj_manage_lbr.GetColumnByName('Execution Country').ReferencingAttribute.SelectDisplayValue(rolesDefaultValue[role]['country'])
                prj_manage_lbr.ApplyProductChanges()
                prj_manage_lbr.Calculate()
        elif attr == "HCI_Labor_common_prj_input1" or attr == "HCI_Labor_common_prj_input2":
            container.AddNewRow(False)
            if Quote.GetCustomField('R2QFlag').Content == 'Yes':
                if attr == "HCI_Labor_common_prj_input1":
                    input1Cont = Product.GetContainerByName('HCI_Labor_common_prj_input1').Rows[0]
                    input1Cont.GetColumnByName('User Requirements').SetAttributeValue('Yes')
                    input1Cont.GetColumnByName('Project Set Up').SetAttributeValue('Yes')
                    input1Cont.GetColumnByName('KOM type').SetAttributeValue('Face 2 Face')
                elif attr == "HCI_Labor_common_prj_input2":
                    input2Cont = Product.GetContainerByName('HCI_Labor_common_prj_input2').Rows[0]
                    input2Cont.GetColumnByName('Site specific documentation').SetAttributeValue(str(input2Cont['Site Acceptance Testing (SAT)']))
'''cred = SqlHelper.GetList("select * from CT_Labor_Engineers where Product='PHD'")
cont=Product.GetContainerByName('HCI_PHD_Fo_Eng')
for eng in cred:
    row=cont.AddNewRow(False)
    row['Engineer']=eng.Engineers
cont=Product.GetContainerByName('HCI_PHD_GES_Eng')
row=cont.AddNewRow(False)
row['Engineer']='GES Eng 1'
row=cont.AddNewRow(False)
row['Engineer']='GES Eng 2'
'''