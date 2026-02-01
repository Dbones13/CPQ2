def getContainer(Name):
    return Product.GetContainerByName(Name)

def getAttributeValueCode(Name):
    if Product.Attr(Name).SelectedValue:
        return Product.Attr(Name).SelectedValue.ValueCode
    return ''

def isHidden(container,Column):
    return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Hidden'

commonQuestionCon = getContainer("MSID_CommonQuestions")
scope = getAttributeValueCode('MIgration_Scope_Choices')
Product.Attr('MSID_ShowTab').AssignValue('')
showTab = True

for row in commonQuestionCon.Rows:
    for col in row.Columns:
        if not isHidden("MSID_CommonQuestions" , col.Name) and row.GetColumnByName(col.Name).Value in ('','None'):
            showTab = False
            break
    break
if showTab:
    Product.Attr('MSID_ShowTab').AssignValue('1')