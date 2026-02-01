from GS_CostAPI_Module import gen_Item_PayLoad, getCost, getAccessToken, getHost
from GS_LSG_Pricing import GetListPriceFromCPS
import re
def GetLongModelNumberCode():
    container=Product.GetContainerByName('Trace_Software_License_Configuration_transpose').Rows
    class_0_new=[]
    class_0_ex=[]
    class_1_new=[]
    class_1_ex=[]
    class_2_new=[]
    class_2_ex=[]
    class_3_new=[]
    class_3_ex=[]
    for i in container:
        if i.RowIndex==0:
            if i['Trace_Software_ESVT'] != '' : class_0_new.append(int(i['Trace_Software_ESVT']))
            if i['Trace_Software_Experion_PKS'] !='' : class_1_new.append(int(i['Trace_Software_Experion_PKS']))
            if i['Trace_Software_Honeywell_TPS'] !='' : class_1_new.append(int(i['Trace_Software_Honeywell_TPS']))
            if i['Trace_Software_Experion_LX_Plantcruise']!='' :
                class_1_new.append(int(i['Trace_Software_Experion_LX_Plantcruise']))
            if i['Trace_Software_Honeywell_Safety_Manager'] !='':
                class_2_new.append(int(i['Trace_Software_Honeywell_Safety_Manager']))
            if i['Trace_Software_Triconex'] != '' :
                class_2_new.append(int(i['Trace_Software_Triconex']))
            if i['Trace_Software_Experion_SCADA'] != '' :
                class_2_new.append(int(i['Trace_Software_Experion_SCADA']))
            if i['Trace_Software_APC_Aspen_DMC_or_ProfitSuite'] != '' :
                class_2_new.append(int(i['Trace_Software_APC_Aspen_DMC_or_ProfitSuite']))
            if i['Trace_Software_Honeywell_ControlEdge_PLC'] != '' :
                class_2_new.append(int(i['Trace_Software_Honeywell_ControlEdge_PLC']))
            if i['Trace_Software_FSC'] != '' :
                class_2_new.append(int(i['Trace_Software_FSC']))
            if i['Trace_Software_Uniformance_PHD'] != '' :
                class_3_new.append(int(i['Trace_Software_Uniformance_PHD']))
            if i['Trace_Software_OSI_PI'] != '' :
                class_3_new.append(int(i['Trace_Software_OSI_PI']))
            if i['Trace_Software_SPI_Tools'] != '' :
                class_3_new.append(int(i['Trace_Software_SPI_Tools']))
            if i['Trace_Software_RS_Logix'] != '' :
                class_3_new.append(int(i['Trace_Software_RS_Logix']))
            if i['Trace_Software_Custom_User_Defined_System'] != '' :
                class_3_new.append(int(i['Trace_Software_Custom_User_Defined_System']))
        if i.RowIndex==1:
            if i['Trace_Software_ESVT'] != '' : class_0_ex.append(int(i['Trace_Software_ESVT']))
            if i['Trace_Software_Experion_PKS'] !='' : class_1_ex.append(int(i['Trace_Software_Experion_PKS']))
            if i['Trace_Software_Honeywell_TPS'] !='' : class_1_ex.append(int(i['Trace_Software_Honeywell_TPS']))
            if i['Trace_Software_Experion_LX_Plantcruise']!='' :
                class_1_ex.append(int(i['Trace_Software_Experion_LX_Plantcruise']))
            if i['Trace_Software_Honeywell_Safety_Manager'] !='':
                class_2_ex.append(int(i['Trace_Software_Honeywell_Safety_Manager']))
            if i['Trace_Software_Triconex'] != '' :
                class_2_ex.append(int(i['Trace_Software_Triconex']))
            if i['Trace_Software_Experion_SCADA'] != '' :
                class_2_ex.append(int(i['Trace_Software_Experion_SCADA']))
            if i['Trace_Software_APC_Aspen_DMC_or_ProfitSuite'] != '' :
                class_2_ex.append(int(i['Trace_Software_APC_Aspen_DMC_or_ProfitSuite']))
            if i['Trace_Software_Honeywell_ControlEdge_PLC'] != '' :
                class_2_ex.append(int(i['Trace_Software_Honeywell_ControlEdge_PLC']))
            if i['Trace_Software_FSC'] != '' :
                class_2_ex.append(int(i['Trace_Software_FSC']))
            if i['Trace_Software_Uniformance_PHD'] != '' :
                class_3_ex.append(int(i['Trace_Software_Uniformance_PHD']))
            if i['Trace_Software_OSI_PI'] != '' :
                class_3_ex.append(int(i['Trace_Software_OSI_PI']))
            if i['Trace_Software_SPI_Tools'] != '' :
                class_3_ex.append(int(i['Trace_Software_SPI_Tools']))
            if i['Trace_Software_RS_Logix'] != '' :
                class_3_ex.append(int(i['Trace_Software_RS_Logix']))
            if i['Trace_Software_Custom_User_Defined_System'] != '' :
                class_3_ex.append(int(i['Trace_Software_Custom_User_Defined_System']))
    sum_class_0=sum(class_0_new)+sum(class_0_ex)
    sum_class_1=sum(class_1_new)+sum(class_1_ex)
    sum_class_2=sum(class_2_new)+sum(class_2_ex)
    sum_class_3=sum(class_3_new)+sum(class_3_ex)

    class_0_tier1_new=0
    class_0_tier2_new=0
    class_1_tier1_new=0
    class_1_tier2_new=0
    class_2_tier1_new=0
    class_2_tier2_new=0
    class_3_tier1_new=0
    class_3_tier2_new=0
    if sum_class_0 ==1:
        class_0_tier1_new=1
        class_0_tier2_new=0
    if sum_class_0 >1:
        class_0_tier1_new=1
        class_0_tier2_new=sum_class_0-1
    if sum_class_1 ==1:
        class_1_tier1_new=1
        class_1_tier2_new=0
    if sum_class_1 >1:
        class_1_tier1_new=1
        class_1_tier2_new=sum_class_1-1
    if sum_class_2 ==1:
        class_2_tier1_new=1
        class_2_tier2_new=0
    if sum_class_2 >1:
        class_2_tier1_new=1
        class_2_tier2_new=sum_class_2-1
    if sum_class_3 ==1:
        class_3_tier1_new=1
        class_3_tier2_new=0
    if sum_class_3 >1:
        class_3_tier1_new=1
        class_3_tier2_new=sum_class_3-1
    # ------------------ existing --------------
    class_0_tier1_ex=0
    class_0_tier2_ex=0
    class_1_tier1_ex=0
    class_1_tier2_ex=0
    class_2_tier1_ex=0
    class_2_tier2_ex=0
    class_3_tier1_ex=0
    class_3_tier2_ex=0
    if sum(class_0_ex)==0 and sum(class_0_new) > 0 :
        class_0_tier1_ex=1
    if sum(class_0_ex)>0:
        class_0_tier1_ex=0
    if sum(class_0_new) == 0:
        class_0_tier2_ex=0
    if sum(class_0_new) > 0:
        class_0_tier2_ex=sum(class_0_new)-class_0_tier1_ex

    if sum(class_1_ex)==0 and sum(class_1_new) > 0 :
        class_1_tier1_ex=1
    if sum(class_1_ex)>0:
        class_1_tier1_ex=0
    if sum(class_1_new) == 0:
        class_1_tier2_ex=0
    if sum(class_1_new) > 0:
        class_1_tier2_ex=sum(class_1_new)-class_1_tier1_ex

    if sum(class_2_ex)==0 and sum(class_2_new) > 0 :
        class_2_tier1_ex=1
    if sum(class_2_ex)>0:
        class_2_tier1_ex=0
    if sum(class_2_new) == 0:
        class_2_tier2_ex=0
    if sum(class_2_new) > 0:
        class_2_tier2_ex=sum(class_2_new)-class_2_tier1_ex

    if sum(class_3_ex)==0 and sum(class_3_new) > 0 :
        class_3_tier1_ex=1
    if sum(class_3_ex)>0:
        class_3_tier1_ex=0
    if sum(class_3_new) == 0:
        class_3_tier2_ex=0
    if sum(class_3_new) > 0:
        class_3_tier2_ex=sum(class_3_new)-class_3_tier1_ex

    scope=Product.Attr('Trace_Software_What_is_the_scope').SelectedValue.UserInput
    table8=table9=table10=table11=table12=table13=table14=table15=table16=0
    Trace.Write(scope)
    #Changes to Existing License (Expansions) New License
    if scope == 'New License' :
        table8=class_1_tier1_new+(class_0_tier1_new*2)
        table9=class_1_tier2_new+(class_0_tier2_new*2)
        table10=class_2_tier1_new
        table11=class_2_tier2_new
        table12=class_3_tier1_new
        table13=class_3_tier2_new
        table14=0
        table15=0
        table16=0
    if scope == 'Changes to Existing License (Expansions)' :
        table8=class_1_tier1_ex+(class_0_tier1_ex*2)
        table9=class_1_tier2_ex+(class_0_tier2_ex*2)
        table10=class_2_tier1_ex
        table11=class_2_tier2_ex
        table12=class_3_tier1_ex
        table13=class_3_tier2_ex
        table14=sum(class_1_ex)+(sum(class_0_ex)*2)
        table15=sum(class_2_ex)
        table16=sum(class_3_ex)
    if table8<10: table8='0'+str(table8)
    if table9<10: table9='0'+str(table9)
    if table10<10: table10='0'+str(table10)
    if table11<10: table11='0'+str(table11)
    if table12<10: table12='0'+str(table12)
    if table13<10: table13='0'+str(table13)
    if table14<10: table14='0'+str(table14)
    if table15<10: table15='0'+str(table15)
    if table16<10: table16='0'+str(table16)

    final_result=str(str(table8)+'-'+str(table9)+'-'+str(table10)+'-'+str(table11)+'-'+str(table12)+'-'+str(table13)+'-'+str(table14)+'-'+str(table15)+'-'+str(table16))
    return final_result
## Below logic is to populate the Write-in
#import clr
import System
#System.AddReference("System.Core")
#System.ImportExtensions(System.Linq)
from GS_AddWriteInProduct import getWriteInProductInfo, PopulateValidPartsCon

what_is_scope = Product.Attr('Trace_Software_What_is_the_scope').SelectedValue
order_type = Product.Attr('Trace_Software_Order_Type').SelectedValue
model_code = GetLongModelNumberCode()
part_generated_code = Product.Attr('Trace_software_code_hidden_calc').GetValue()
Trace.Write('========================================')
if '########' in part_generated_code:
    part_generated_code = part_generated_code.replace('########',model_code)
else:
    idx=[i.start() for i in re.finditer('-',part_generated_code)]
    a=idx[8]+1
    b=idx[17]
    x=part_generated_code[a:b]
    part_generated_code = part_generated_code.replace(x,model_code)
Trace.Write(part_generated_code)
part_generated_code = part_generated_code.replace('########',model_code)
Trace.Write(part_generated_code)
partNumberList =[]
_dict = { part_generated_code:"AS-UTRACS"}
partNumberList.append(_dict)
hostname = getHost()
########## PRICE ############
Trace.Write('Calling  CPS Price Service....')
Trace.Write('Host'+str(hostname))
Trace.Write('Partssss' + str(partNumberList))
_responsePrice = ''
Trace.Write('partsss '+str(partNumberList))
_responsePrice = GetListPriceFromCPS(Quote, partNumberList, ProductHelper, TagParserQuote,hostname)
responsePrice = ''
if _responsePrice != None or _reponsePrice != '':
    responsePrice = str(_responsePrice)
else:
    responsePrice = '1.00'

################################


########## CPS COST #####################
Trace.Write('Calling  CPS Cost Service....')

responseToken = getAccessToken(hostname)
responsePayload = gen_Item_PayLoad(Quote,"AS-UTRACS",part_generated_code)
try:
    _responseCost = getCost(Quote, responseToken, responsePayload)
except:
    _responseCost = None
responseCost = ''
if _responseCost is not None and _responseCost['vcMaterialCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'] is not None:
    responseCost = str(_responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'])
    Trace.Write('========================COST'+str(responseCost))
else:
    responseCost = '1.00'

def GetWarrantCostPrice(responsePrice):
    price = 0.00
    cost = 0.00
    for row in Product.GetContainerByName('Trace_Software_License_Configuration_transpose').Rows:
        year_of_support = row['Trace_Software_Years_of_Support']
        if int(year_of_support) == 1:
            price = 0.20*float(responsePrice)
            #cost = 0.40*price
            cost = 0.55*price
        elif int(year_of_support) == 2:
            #price = 0.18*float(responsePrice)
            #cost = 0.40*price
            price = (0.18+0.18)*float(responsePrice)
            cost = 0.55*price
        else:
            #price = 0.16*float(responsePrice)
            #cost = 0.40*price
            price = (0.16+0.16+0.16)*float(responsePrice)
            cost = 0.55*price
    return price, cost


WriteInProduct_container = Product.GetContainerByName("WriteInProduct")
write_in_type = ''
description = ''
WriteInProduct_container.Rows.Clear()

if (what_is_scope.Display == "New License" and order_type.Display in ["Standard New Commercial License", 'Competitive Replacement Pricing']) or what_is_scope.Display == "Changes to Existing License (Expansions)":
    write_in_type = 'Write-In Trace Software'
    #description = "Trace Software"
    writeInProductInfo = getWriteInProductInfo(write_in_type)
    populate = PopulateValidPartsCon(Product, "LSS", write_in_type, "1", str(part_generated_code), responsePrice,responseCost, writeInProductInfo)

elif what_is_scope.Display == "New License" and order_type.Display == "Competitive Upgrade":
    write_in_type = 'Write-In Trace Software Competitive'
    #description = "Trace Software nonDiscount Pricing"
    writeInProductInfo = getWriteInProductInfo(write_in_type)
    populate = PopulateValidPartsCon(Product, "LSS", write_in_type, "1", str(part_generated_code), responsePrice, responseCost, writeInProductInfo)

if what_is_scope.Display == "New License":
    if order_type.Display == "Competitive Upgrade" or order_type.Display =="Competitive Replacement Pricing":
        write_in_type = 'Write-In Trace Extended Warranty Support'
        writeInProductInfo = getWriteInProductInfo(write_in_type)
        standard_price = float(responsePrice)*2
        warranty_price = (0.18+0.18+0.18)*standard_price
        cost = 0.55*warranty_price
        populate = PopulateValidPartsCon(Product, "LSS", write_in_type, "1", "Trace Extended Warranty Support", str(warranty_price), str(cost), writeInProductInfo)
    else:
        write_in_type = 'Write-In Trace Extended Warranty Support'
        #description = "Write-In Trace Extended Warranty Support"
        writeInProductInfo = getWriteInProductInfo(write_in_type)
        price, cost = GetWarrantCostPrice(responsePrice)
        #copied last line from Dev for Incomplete issue
        populate = PopulateValidPartsCon(Product, "LSS", write_in_type, "1", "Trace Extended Warranty Support", str(price), str(cost), writeInProductInfo)