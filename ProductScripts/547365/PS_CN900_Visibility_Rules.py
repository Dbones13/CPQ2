from GS_UpdateLaborPrices import getFloat
def getContainer(containerName):
    return Product.GetContainerByName(containerName)

def getAttributeValue(attribute_name):
    return Product.Attributes.GetByName(attribute_name)

def setHidden(cont,column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(cont, column))
def setEditable(cont,column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(cont, column))

def disallowattrs(attname):
    return Product.DisallowAttr(attname)
def allowattrs(attname):
    return Product.AllowAttr(attname)
if Product.Name == "ControlEdge CN900 System":

    '''#Total_UOC_DCS_Marshalling
    if getAttributeValue('staging_Marshalling_Cabinets_c300_rtu_uoc_SM_plc'):
        staging_c300_rtu_uoc_Sm_plc=getAttributeValue('staging_Marshalling_Cabinets_c300_rtu_uoc_SM_plc').GetValue()
    #staging_c300_rtu_uoc_Sm_plc = staging_c300_rtu_uoc_Sm_plc if staging_c300_rtu_uoc_Sm_plc else 0
    if getAttributeValue('Total_UOC_DCS_Marshalling'):
        getAttributeValue('Total_UOC_DCS_Marshalling').AssignValue(str(staging_c300_rtu_uoc_Sm_plc))'''

    #ADC_Ges_Location
    if getContainer('CN900_Labor_Details'):
        for i in getContainer('CN900_Labor_Details').Rows:
            cn900_ges_loc=i['CN900_Ges_Location_Labour']
            if cn900_ges_loc == "None":
                if getAttributeValue('CN900_CD_LD_GES Engineer %'):
                    disallowattrs('CN900_CD_LD_GES Engineer %')
                GES_Eng=setHidden('CE CN900 Additional Custom Deliverables','GES Eng')
                GES_Eng_Split=setHidden('CE CN900 Additional Custom Deliverables','GES Eng % Split')
                GES_Eng_unit_reg_cost=setHidden('CE CN900 Additional Custom Deliverables','GES_Unit_Regional_Cost')
                GES_Eng_regional_cost=setHidden('CE CN900 Additional Custom Deliverables','GES_Regional_Cost')
                GES_Eng_ListPrice=setHidden('CE CN900 Additional Custom Deliverables','GES_ListPrice')
                GES_Eng_WTW_cost=setHidden('CE CN900 Additional Custom Deliverables','GES_WTW_Cost')
                #GES_Eng_MPA_Price=setHidden('CE CN900 Additional Custom Deliverables','GES_MPA_Price')
            else:
                if getAttributeValue('CN900_CD_LD_GES Engineer %'):
                    allowattrs('CN900_CD_LD_GES Engineer %')
                GES_Eng=setEditable('CE CN900 Additional Custom Deliverables','GES Eng')
                GES_Eng_Split=setEditable('CE CN900 Additional Custom Deliverables','GES Eng % Split')
                GES_Eng_unit_reg_cost=setEditable('CE CN900 Additional Custom Deliverables','GES_Unit_Regional_Cost')
                GES_Eng_regional_cost=setEditable('CE CN900 Additional Custom Deliverables','GES_Regional_Cost')
                GES_Eng_ListPrice=setEditable('CE CN900 Additional Custom Deliverables','GES_ListPrice')
                GES_Eng_WTW_cost=setEditable('CE CN900 Additional Custom Deliverables','GES_WTW_Cost')
                #GES_Eng_MPA_Price=setEditable('CE CN900 Additional Custom Deliverables','GES_MPA_Price')

    #Final Hrs 
    Ce_uoc_eng,Ce_uoc_Additional =0.0,0.0
    if getContainer('CE CN900 Engineering Labor Container'):
        for i in getContainer('CE CN900 Engineering Labor Container').Rows:
            if i['Final Hrs']:
                Ce_uoc_eng+=getFloat(i['Final Hrs'])
    if getContainer('CE CN900 Additional Custom Deliverables'):
        for i in getContainer('CE CN900 Additional Custom Deliverables').Rows:
            if i['Final Hrs']:
                Ce_uoc_Additional+=getFloat(i['Final Hrs'])
                Trace.Write(Ce_uoc_eng)
    Ce_uoc_eng= Ce_uoc_eng if Ce_uoc_eng else 0
    Ce_uoc_Additional= Ce_uoc_Additional if Ce_uoc_Additional else 0
    Total = getFloat(Ce_uoc_eng)+getFloat(Ce_uoc_Additional)
    if getAttributeValue('Final_Hrs'):
        getAttributeValue('Final_Hrs').AssignValue(str(Total))

	'''------GES Location ------'''
    if getContainer('CN900_Labor_Details'):
        for i in getContainer('CN900_Labor_Details').Rows:
            CN900_Ges_Location_labour =i['CN900_Ges_Location_Labour']
            if CN900_Ges_Location_labour == "None":
                disallowattrs('CE CN900 GES Engineer %')
                GES_ENG =setHidden('CE CN900 Engineering Labor Container','GES Eng')
                GES_Eng_Split=setHidden('CE CN900 Engineering Labor Container','GES Eng % Split')
                GES_Eng_unit_reg_cost=setHidden('CE CN900 Engineering Labor Container','GES_Unit_Regional_Cost')
                GES_Eng_regional_cost=setHidden('CE CN900 Engineering Labor Container','GES_Regional_Cost')
                GES_Eng_ListPrice=setHidden('CE CN900 Engineering Labor Container','GES_ListPrice')
                GES_Eng_WTW_cost=setHidden('CE CN900 Engineering Labor Container','GES_WTW_Cost')
                #GES_Eng_MPA_Price=setHidden('CE CN900 Engineering Labor Container','GES_MPA_Price')
            else:
                allowattrs('CE CN900 GES Engineer %')
                GES_Eng=setEditable('CE CN900 Engineering Labor Container','GES Eng')
                GES_Eng_Split=setEditable('CE CN900 Engineering Labor Container','GES Eng % Split')
                GES_Eng_unit_reg_cost=setEditable('CE CN900 Engineering Labor Container','GES_Unit_Regional_Cost')
                GES_Eng_regional_cost=setEditable('CE CN900 Engineering Labor Container','GES_Regional_Cost')
                GES_Eng_ListPrice=setEditable('CE CN900 Engineering Labor Container','GES_ListPrice')
                GES_Eng_WTW_cost=setEditable('CE CN900 Engineering Labor Container','GES_WTW_Cost')
                #GES_Eng_MPA_Price=setEditable('CE CN900 Engineering Labor Container','GES_MPA_Price')

    #LabourContainerHideCN900
    if getAttributeValue('CE_Scope_Choices'):
        if getAttributeValue('CE_Scope_Choices').GetValue() =="HW/SW":
            if getAttributeValue ('CN900_Labor_Details'):
                disallowattrs('CN900_Labor_Details')
        else:
            if getAttributeValue ('CN900_Labor_Details'):
                allowattrs('CN900_Labor_Details')