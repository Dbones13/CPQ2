opc_server_redundancy = Product.Attr('OPC_server_redundancy_required').GetValue()
domain_controller_required = Product.Attr('Domain_Controller_Required').GetValue()
opc_server_required = Product.Attr('Opc_server_required').GetValue()
qty = 0

if opc_server_required == "Yes":
    if opc_server_redundancy == "Redundant":
        qty += 2
    else:
        qty += 1

if domain_controller_required == "Yes":
    qty += 1

Product.Attr('Additional Servers').AssignValue(str(qty))