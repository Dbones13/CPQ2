def getContainer(Name):
	return Product.GetContainerByName(Name)

attrs = ["CN900_Cabinet_Controller_Cont"]
for attr in attrs:
	container = getContainer(attr)
	if container.Rows.Count == 0:
		#setDefault = True
		container.AddNewRow('CN900_Control_Group_cpq',False)
		container.Calculate()