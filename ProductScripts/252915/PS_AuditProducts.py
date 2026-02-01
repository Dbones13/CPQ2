def getfloat(val):
    if val:
        try:
            return float(val)
        except:
            return 0
    return 0

selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
'''for li in selectedProducts:
    Trace.Write(li)'''
needToAdd_IOhidden = False
needToAdd_FSChidden = False
'''for row in cont.Rows:
    if row['Selected_Products'] == 'FSC to SM IO Migration':
        needToAdd_IOhidden = True
    if row['Selected_Products'] == 'FSC to SM':
        needToAdd_FSChidden = True'''

if 'FSC to SM IO Migration' in selectedProducts:
    needToAdd_IOhidden = True
if 'FSC to SM' in selectedProducts:
    needToAdd_FSChidden = True

producthiddenContainer = Product.GetContainerByName('MSID_Product_Container_FSC_IO_hidden')
hiddenContainer = Product.GetContainerByName('MSID_Product_Container_FSC_hidden')
IOLaborCont = Product.GetContainerByName('MSID_Labor_FSC_to_SM_IO_Audit_Con')
auditCon = Product.GetContainerByName('MSID_Labor_FSC_to_SM_audit_Con')
IOHrs= 0
auditHrs = 0

for row in IOLaborCont.Rows:
    IOHrs +=  getfloat(row['Final_Hrs'])
for row in auditCon.Rows:
    auditHrs += getfloat(row['Final_Hrs'])
Trace.Write("Audit Hrs ----> {}".format(auditHrs))
if needToAdd_IOhidden and producthiddenContainer.Rows.Count == 0 and IOHrs > 0:
    newRowfsc = producthiddenContainer.AddNewRow('FSC_to_SM_IO_Audit_cpq')
    newRowfsc['Product Name'] = "FSC to SM IO Audit"
if needToAdd_FSChidden and hiddenContainer.Rows.Count == 0 and auditHrs > 0:
    newRowfsc = hiddenContainer.AddNewRow('FSC_to_SM_Audit_cpq')
    newRowfsc['Product Name'] = "FSC to SM Audit"

if (needToAdd_IOhidden == False and producthiddenContainer.Rows.Count) or IOHrs == 0 :
    Product.GetContainerByName('MSID_Product_Container_FSC_IO_hidden').Rows.Clear()
if (needToAdd_FSChidden == False and hiddenContainer.Rows.Count) or auditHrs == 0:
    #Trace.Write("*******************************************************")
    Product.GetContainerByName('MSID_Product_Container_FSC_hidden').Rows.Clear()