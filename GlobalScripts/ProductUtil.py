def addMessage(product , msg):
    if product.Name in ["Safety Manager HIPPS", "Safety Manager FGS", "Safety Manager ESD", "Safety Manager BMS", "SM Control Group", "SM Remote Group", "C300 System", "Series-C Control Group", "Series-C Remote Group","R2Q Safety Manager FGS", "R2Q Safety Manager ESD", "R2Q SM Control Group", "R2Q SM Remote Group"]:
        return
    if product.Messages.Contains(msg):
        return
    product.Messages.Add(msg)

def addMessages(product , msgs):
    for msg in msgs:
        addMessage(product , msg)

def getContainer(product, containerName):
    return product.GetContainerByName(containerName)

def getContainerBySystemId(product, containerSystemId):
    return product.GetContainerBySystemId(containerSystemId)