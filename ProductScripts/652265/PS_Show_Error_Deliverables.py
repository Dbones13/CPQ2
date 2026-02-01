def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00

Product.Attr('ErrorMessage').AssignValue('')
Error_Message = ""

deliverables = Product.GetContainerByName("Winest Labor Container").Rows
count = 0
Labor_Message = ""
for row in deliverables:
    deliverable = row['Deliverable']
    if getFloat(row['Regional_Cost']) == 0 and getFloat(row['Final Hrs']) != 0:
        count += 1
        Labor_Message = Labor_Message + " - " +str(deliverable) + "<br>"
if count > 0:
    Labor_Message = "<b>"+'Cost is not available for resource in Valid Parts. Please select different Execution Country. Deliverables to look into: <br>'+"</b>" + Labor_Message
    if Error_Message != "":
        Error_Message = Error_Message + "<br>" + Labor_Message
    else:
        Error_Message = Labor_Message

deliverables = Product.GetContainerByName("Winest Additional Labor Container").Rows
count = 0
Labor_Message = ""
for row in deliverables:
    deliverable = row['Deliverable']
    if getFloat(row['Regional_Cost']) == 0 and getFloat(row['Final Hrs']) != 0 and row['Service Material'] != 'None':
        count += 1
        Labor_Message = Labor_Message + " - " +str(deliverable) + "<br>"
if count > 0:
    Labor_Message = "<b>"+'Cost is not available for resource in Additional Custom Deliverables. Please select different resource or select different Execution Country. Deliverables to look into: <br>'+"</b>" + Labor_Message
    if Error_Message != "":
        Error_Message = Error_Message + "<br>" + Labor_Message
    else:
        Error_Message = Labor_Message

if Error_Message != '':
    Product.Attr('ErrorMessage').AssignValue(Error_Message)