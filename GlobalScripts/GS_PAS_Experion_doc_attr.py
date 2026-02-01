import System.Decimal as D
def docattr(Product):
    server_exp=acevalue=acevalueT=appNode=PCserever=mobile=oper_stnQ=sum_server=server_exp_tps=server_exp1=additionalserver1=0
    additionalserver1 = int(Product.Attr('Additional Servers').GetValue())
    TPS_req=Product.Attr('Interface with TPS Required?').GetValue() if Product.Attr('Interface with TPS Required?').GetValue() !='' else 'No'
    Server_req=Product.Attr('Server Redundancy Requirement?').GetValue() if Product.Attr('Server Redundancy Requirement?').GetValue() !='' else 'No'
    if Server_req=="Redundant":
        server_exp=2 + additionalserver1
    elif Server_req=="Non Redundant":
        server_exp=1 + additionalserver1
    if TPS_req=="Yes":
        server_exp_tps=server_exp
    else:
        server_exp1=server_exp
    qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
    qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
    qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
    PCserever=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
    mobile=int(Product.Attr('Mobile Server Nodes (0-1)').GetValue()) if Product.Attr('Mobile Server Nodes (0-1)').GetValue()!='' else 0
    ace=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet']
    ace_T=['ACE_T_Node _Tower_Mount_Desk','ACE_T_Node _Rack_Mount_Cabinet']
    app_node=['Experion APP Node - Tower Mount','Experion APP Node - Rack Mount']
    for i,j,k in zip(ace,ace_T,app_node):
        acevalue += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue() !='' else 0
        acevalueT += int(Product.Attr(str(j)).GetValue()) if Product.Attr(str(j)).GetValue() !='' else 0
        appNode += int(Product.Attr(str(k)).GetValue()) if Product.Attr(str(k)).GetValue() !='' else 0
    sum_server=server_exp1+server_exp_tps+acevalue+acevalueT+appNode+PCserever+mobile
    return server_exp,server_exp_tps,acevalue,acevalueT,appNode,PCserever,mobile,sum_server,server_exp1

def workstation(Product):
    oper_stnQ=server_exp=position=server_exp1=flex_desk=dms_qnt=0
    displaysize=Product.Attr('Display_Size_FlexServer').GetValue() if Product.Attr('Display_Size_FlexServer').GetValue() !='' else 'No'
    Trace.Write("displaysize "+str(displaysize))
    displaysize2=Product.Attr('DMS Display size').GetValue() if Product.Attr('DMS Display size').GetValue() !='' else 'No'
    Trace.Write("displaysize2 "+str(displaysize2))
    displaysize1=Product.Attr('Orion Console Display Size').GetValue() if Product.Attr('Orion Console Display Size').GetValue() !='' else 'No'
    Trace.Write("displaysize1 "+str(displaysize1))
    oper_stn=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15','DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15','Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)','Additional Stations']
    flex=Product.Attr('Display_Size_FlexServer').GetValue()
    flex_list=["Displays_Flex Server in Desk0_2","Displays_Flex Server in Desk0_2_2"]
    for i in flex_list:
        flex_desk += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue() !='' else 0
    Server_req=Product.Attr('Server Redundancy Requirement?').GetValue() if Product.Attr('Server Redundancy Requirement?').GetValue() !='' else 'No'
    if Server_req=="Redundant":
        server_exp=2*int(flex_desk)
    elif Server_req=="Non Redundant":
        server_exp=flex_desk
    if displaysize=="55 inch NTS":
        server_exp1=server_exp
    dms=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
    dms_mult=int(Product.Attr('DMS No of Displays 0_4').GetValue()) if Product.Attr('DMS No of Displays 0_4').GetValue() !='' else 0
    Trace.Write("dms_mult "+str(dms_mult))
    for j in dms:
        dms_qnt += int(Product.Attr(str(j)).GetValue()) if Product.Attr(str(j)).GetValue() !='' else 0
    dms_qn=dms_qnt*dms_mult
    if displaysize2=="55 inch NTS":
        dms_qn=dms_qn
    else:
        dms_qn=0
    position2=int(Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue() !='' else 0
    position3=int(Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue() !='' else 0
    Network_Cabinet_Qty=int(Product.Attr('Network_Cabinet_Qty').GetValue()) if Product.Attr('Network_Cabinet_Qty').GetValue() !='' else 0
    printer_Qty=int(Product.Attr('LaserJet Printer - Monochrome (0-99)').GetValue()) if Product.Attr('LaserJet Printer - Monochrome (0-99)').GetValue() !='' else 0
    if displaysize1=="55 inch NTS":
        position=(2*position2)+(3*position3)
    else:
        position=0
    inch55_dis=position+dms_qn+server_exp1
    for l in oper_stn:
        oper_stnQ += int(Product.Attr(str(l)).GetValue()) if Product.Attr(str(l)).GetValue() !='' else 0
    sum_workstn=oper_stnQ+inch55_dis
    return oper_stnQ,inch55_dis,sum_workstn,position2,position3,Network_Cabinet_Qty,printer_Qty