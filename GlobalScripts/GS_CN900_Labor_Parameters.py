class AttrStorage:
    def __init__(self, Product):
        self.opcnodes = Product.GetContainerByName('CN900_Labor_Details').Rows[0].GetColumnByName('CN900_OPC_Nodes').Value
        self.points = Product.GetContainerByName('CN900_Labor_Details').Rows[0].GetColumnByName('CN900_Points').Value