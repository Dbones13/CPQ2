import GS_PAS_Experion_doc_attr
server_exp,server_exp_tps,acevalue,acevalueT,appNode,PCserever,mobile,sum_server,server_exp1=GS_PAS_Experion_doc_attr.docattr(Product)
oper_stnQ,inch55_dis,sum_workstn,position2,position3,Network_Cabinet_Qty,printer_Qty=GS_PAS_Experion_doc_attr.workstation(Product)

Product.Attr('Experion_Server_qnt').AssignValue(str(server_exp1))
Product.Attr('Experion_Server_qnt_tps').AssignValue(str(server_exp_tps))
Product.Attr('ACE_node Total_qnt').AssignValue(str(acevalue))
Product.Attr('ACE_node Total_qnt_tps').AssignValue(str(acevalueT))
Product.Attr('APP Node total QNT').AssignValue(str(appNode))
Product.Attr('Mobile Server Nodes').AssignValue(str(mobile))
Product.Attr('Simulation server qnt').AssignValue(str(PCserever))
Product.Attr('Total server qnt').AssignValue(str(sum_server))
Product.Attr('Operator Station QNT').AssignValue(str(oper_stnQ))
Product.Attr('Number of 55').AssignValue(str(inch55_dis))
Product.Attr('Number of 55 display1').AssignValue(str(sum_workstn))
Product.Attr('Number of 55 display3').AssignValue(str(position3))
Product.Attr('Number of 55 display2').AssignValue(str(position2))
position=position3+position2
cab_qnt =Product.Attr('exp_ent_cab_qnt').GetValue() if Product.Attr('exp_ent_cab_qnt').GetValue() !='' else 0
Product.Attr('orion qnt 2and 3').AssignValue(str(position))
Product.Attr('Network_Cabinet_Qty1').AssignValue(str(Network_Cabinet_Qty))
network=Network_Cabinet_Qty+int(cab_qnt)
Product.Attr('network switch').AssignValue(str(network))
Product.Attr('Printer qnt').AssignValue(str(printer_Qty))