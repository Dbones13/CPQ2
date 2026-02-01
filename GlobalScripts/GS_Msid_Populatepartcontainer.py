import math

def getFloat(var):
    if var:
        return float(var)
    return 0

def val(operand, attrDict, index):
    try:
        return getFloat(operand)
    except Exception:
        if attrDict.get(operand):
            if type(attrDict[operand]) == type(list()) and index is not None:
                return getFloat(attrDict[operand][index])
            elif type(attrDict[operand]) == type(list()) and index is None:
                return getFloat(attrDict[operand][0])
            return getFloat(attrDict[operand])
    return 0

def operate(operator, operand1, operand2, attrDict, index):
    operand1 = val(operand1, attrDict, index)
    operand2 = val(operand2, attrDict, index)
    res = 0
    if operator == '/':
        return round(operand1 / operand2)
    if operator == '%':
        return operand1 % operand2
    if operator == '//':
        return operand1 // operand2
    if operator == '+':
        return operand1 + operand2
    if operator == '-':
        return operand1 - operand2
    if operator == '*':
        return operand1 * operand2
    if operator == 'F':
        return math.floor(operand1/operand2)
    if operator == 'C':
        return math.ceil(operand1/operand2)
    return 0

def calculate(expression, attrDict, index = None):
    expression.reverse()
    oprandStack = []
    for char in expression:
        if char in ('/', '//', '%', '+', '-', '*', 'F', 'C'):
            operand1 = oprandStack.pop()
            operand2 = oprandStack.pop()
            res = operate(char, operand1, operand2, attrDict, index)
            oprandStack.append(res)
            continue
        oprandStack.append(char)
    return oprandStack[0]

def getListSum(ls):
    res = 0
    for item in filter(lambda x : x, ls):
        res += int(item)
    return res

def calcualteMultiPartQty(row, attrDict):
    n = 0
    qty = 0
    lsType = type(list())
    attr1 = attrDict.get(row.Attribute_Name,"")
    attr2 = attrDict.get(row.Dependency_Attribute_Name, "")
    attr3 = attrDict.get(row.Dependency_Attribute_Name_2, "")
    if type(attr1) == lsType:
        n = len(attr1)
    if type(attr2) == lsType:
        n = len(attr2)
    if type(attr3) == lsType:
        n = len(attr3)
    for i in range(n):
        check = attr1[i] if type(attr1) == lsType else attr1
        if row.Attribute_Name and check != row.Attribute_Value_Code:
            continue
        check = attr2[i] if type(attr2) == lsType else attr2
        if row.Dependency_Attribute_Name and check != row.Dependency_Attribute_Value_Code:
            continue
        check = attr3[i] if type(attr3) == lsType else attr3
        if row.Dependency_Attribute_Name_2 and check != row.Dependency_Attribute_Value_Code_2:
            continue
        if row.Quantity_Reference_Attribute_Name:
            if row.Quantity_Reference_Attribute_Name.startswith("CALC:"):
                expression = row.Quantity_Reference_Attribute_Name[6:-1]
                qty += calculate(expression.split(','), attrDict, i)
            else:
                for attr in row.Quantity_Reference_Attribute_Name.split(","):
                    if type(attrDict[attr]) == lsType:
                        qty += int(attrDict[attr][i]) if attrDict[attr][i] else 0
                    else:
                        qty += int(attrDict[attr]) if attrDict[attr] else 0
        else:
            qty += row.Quantity
    return qty

def checkPartQtyToBeAdded(row, attrDict):
    # try:
    #Log.Info("AttDic==>"+str(attrDict))
    listType = type(list())
    if  type(attrDict.get(row.Attribute_Name, "")) == listType or type(attrDict.get(row.Dependency_Attribute_Name, "")) == listType or type(attrDict.get(row.Dependency_Attribute_Name_2, "")) == listType or row.CalculateMultiRows:
        return calcualteMultiPartQty(row,attrDict)
    if row.Attribute_Name and attrDict.get(row.Attribute_Name, "") != row.Attribute_Value_Code:
        return 0
    if row.Dependency_Attribute_Name and attrDict.get(row.Dependency_Attribute_Name, "") != row.Dependency_Attribute_Value_Code:
        return 0
    if row.Dependency_Attribute_Name_2 and attrDict.get(row.Dependency_Attribute_Name_2, "") != row.Dependency_Attribute_Value_Code_2:
        return 0
    qty = 0
    if row.Quantity_Reference_Attribute_Name:
        if row.Quantity_Reference_Attribute_Name.startswith("CALC:"):
            expression = row.Quantity_Reference_Attribute_Name[6:-1]
            qty = calculate(expression.split(','), attrDict)
        else:
            for attr in row.Quantity_Reference_Attribute_Name.split(","):
                if type(attrDict.get(attr)) == listType:
                    qty += getListSum(attrDict[attr])
                else:
                    qty += int(attrDict[attr]) if attrDict.get(attr) else 0
        return qty
    return row.Quantity
    # except:
        # return 0