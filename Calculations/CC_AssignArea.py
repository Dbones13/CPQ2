def AssignArea(mainitem, area):
	for item in mainitem.Children:
		item['QI_Area'].Value = area
		for childitem in item.Children:
			childitem['QI_Area'].Value = area
			for _childitem in childitem.Children:
				_childitem['QI_Area'].Value = area

if Session["prevent_execution"] != "true":
	msidParentRolledUpItemId = {}
	for item in Quote.MainItems:
		if item.ProductName == 'Migration_New':
			for msidlevel in item.Children:
				if msidlevel.ProductName == 'MSID_New':
					msid = msidlevel.PartNumber
					Trace.Write(msidlevel.PartNumber)
					for productlevel in msidlevel.Children:
						if productlevel.ProductName in ['ControlEdge PLC System Migration', 'ControlEdge UOC System Migration', 'CE PLC Control Group','CE PLC Remote Group', 'UOC Control Group', 'CE PLC Remote Group']:
							AssignArea(productlevel, msid)