import math
import ProductUtil

def checkInt(value):
    Trace.Write(value)
    if value == '':
        return True
    value = float(value)
    if value < 0:
        return False
    if math.ceil(value) != math.floor(value):
        return False
    return True

for attr in Product.Attributes:
    if "Number" in attr.GetLabel() and attr.Name != "Group Number":
        valid = checkInt(attr.GetValue())
        if valid:
            continue
        else:
            ProductUtil.addMessage(Product , "Please enter a positive integer value")
            attr.AssignValue('')