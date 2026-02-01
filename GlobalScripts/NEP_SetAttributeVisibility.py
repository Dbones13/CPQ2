def SetAttrVisibility(quote,product,name):
		if product.Name == 'New / Expansion Project':
				showList,HideList=[],[]
				h_add_attr,s_add_attr=[],[]
				if name=="Header_01_open":
						showList=["Project_Productivity","Project_Execution_Year","Project_Execution_Country","Project_management_Labor_Container"]
						HideList=["Labor_Productivity","Labor_Execution_Year","Labor_Execution_Country","Labor_Container","PLE_Productivity","PLE_Execution_Year","PLE_Execution_Country","PLE_Labor_Container","Project_Additional_Year","Project_Additional_Execution_Country","PM_Additional_Custom_Deliverables_Labor_Container"]
						if Product.Attr('MSID_GES_Location').GetValue() != 'None':
								h_add_attr = ["Labor_GES_%","PLE_GES_%","Project_Additinoal_GES_%"]
								HideList.extend(h_add_attr)
								s_add_attr = ["Project_GES_%"]
								showList.extend(s_add_attr)
				if name=="Header_19_open":
						showList=["Labor_Productivity","Labor_Execution_Year","Labor_Execution_Country","Labor_Container"]
						HideList=["Project_Productivity","Project_Execution_Year","Project_Execution_Country","Project_management_Labor_Container","PLE_Productivity","PLE_Execution_Year","PLE_Execution_Country","PLE_Labor_Container","Project_Additional_Year","Project_Additional_Execution_Country","PM_Additional_Custom_Deliverables_Labor_Container"]
						if Product.Attr('MSID_GES_Location').GetValue() != 'None':
								h_add_attr = ["PLE_GES_%","Project_Additinoal_GES_%","Project_GES_%"]
								HideList.extend(h_add_attr)
								s_add_attr = ["Labor_GES_%"]
								showList.extend(s_add_attr)
				if name=="Header_20_open":
						showList=["PLE_Productivity","PLE_Execution_Year","PLE_Execution_Country","PLE_Labor_Container"]
						HideList=["Project_Productivity","Project_Execution_Year","Project_Execution_Country","Project_management_Labor_Container","Labor_Productivity","Labor_Execution_Year","Labor_Execution_Country","Labor_Container","Project_Additional_Year","Project_Additional_Execution_Country","PM_Additional_Custom_Deliverables_Labor_Container"]
						if Product.Attr('MSID_GES_Location').GetValue() != 'None':
								h_add_attr = ["Labor_GES_%","Project_Additinoal_GES_%","Project_GES_%"]
								HideList.extend(h_add_attr)
								s_add_attr = ["PLE_GES_%"]
								showList.extend(s_add_attr)
				if name=="Header_07_open":
						showList=["Project_Additional_Year","Project_Additional_Execution_Country","PM_Additional_Custom_Deliverables_Labor_Container"]
						HideList=["Project_Productivity","Project_Execution_Year","Project_Execution_Country","Project_management_Labor_Container","Labor_Productivity","Labor_Execution_Year","Labor_Execution_Country","Labor_Container","PLE_Productivity","PLE_Execution_Year","PLE_Execution_Country","PLE_Labor_Container"]
						if Product.Attr('MSID_GES_Location').GetValue() != 'None':
								h_add_attr = ["Labor_GES_%","PLE_GES_%","Project_GES_%"]
								HideList.extend(h_add_attr)
								s_add_attr = ["Project_Additinoal_GES_%"]
								showList.extend(s_add_attr)
				for show in showList:
						product.Attr(show).Access = AttributeAccess.Editable
				for hide in HideList:
						product.Attr(hide).Access = AttributeAccess.Hidden
				return True
		else:
				return False

def SetMAttrVisibility(quote,product,name):
		if product.Name == 'MSID_New':
				Trace.Write(name)
				#if name != "#noName" and product.Attr('ATTR_ LBORHIDSHW').GetValue():
						#name+=","+product.Attr('ATTR_ LBORHIDSHW').GetValue()
				product.Attr('ATTR_ LBORHIDSHW').AssignValue(name)
				return {"name":product.Attr('ATTR_ LBORHIDSHW').GetValue()}
		else:
				return False

def SetEEGAttrVisibility(quote,product,name):
	if product.Name == 'Experion Enterprise Group' or Product.Name == 'New / Expansion Project':
		#if name != "#noName" and product.Attr('ATTR_ LBORHIDSHW').GetValue():
			#name+=","+product.Attr('ATTR_ LBORHIDSHW').GetValue()
			#Trace.Write(name)
		if "#all" in product.Attr('ATTR_ LBORHIDSHW').GetValue():
			product.Attr('ATTR_ LBORHIDSHW').AssignValue(None)
		else:
			product.Attr('ATTR_ LBORHIDSHW').AssignValue(name)
		return {"name":product.Attr('ATTR_ LBORHIDSHW').GetValue()}
	else:
		return False

if Product.Name == 'New / Expansion Project':
		ApiResponse = ApiResponseFactory.JsonResponse(SetEEGAttrVisibility(Quote,Product,Param.name))
elif Product.Name == 'MSID_New':
		ApiResponse = ApiResponseFactory.JsonResponse(SetMAttrVisibility(Quote,Product,Param.name))
elif Product.Name == 'Experion Enterprise Group':
		ApiResponse = ApiResponseFactory.JsonResponse(SetEEGAttrVisibility(Quote,Product,Param.name))
else:
		ApiResponse = ApiResponseFactory.JsonResponse(False)