def getContainer(Name):
    return Product.GetContainerByName(Name)
def ReadOnly(attrname):
    Product.Attr(attrname).Access = AttributeAccess.ReadOnly
def Editable(attrname):
    Product.Attr(attrname).Access = AttributeAccess.Editable
#Read only access for attribute based on Condition Dhrumil Shah : CXCPQ-60156 :start
selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])
if "ELEPIU ControlEdge RTU Migration Engineering" in selectedProducts:
    ReadOnly('ELEPIU_Total_numberof_Scada_points_for_controllers')
    ReadOnly('ELEPIU_Total_number_of_Process_points_controllers')
    ReadOnly('ELEPIU_Total_number_of_graphics_affected_by_ELPIU')
    PropType=Quote.GetCustomField('EGAP_Proposal_Type').Content
    if PropType!="Budgetary":
        Editable('ELEPIU_Total_numberof_Scada_points_for_controllers')
        Editable('ELEPIU_Total_number_of_Process_points_controllers')
        Editable('ELEPIU_Total_number_of_graphics_affected_by_ELPIU')
#Dhrumil Shah : CXCPQ-60156 :end