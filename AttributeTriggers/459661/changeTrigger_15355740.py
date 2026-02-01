def assignMIBval(contprod,contname,contProdname,mibval):
	congrpcont = contprod.GetContainerByName(contname)
	if congrpcont and congrpcont.Rows.Count > 0:
		for rowc in congrpcont.Rows:
			if rowc.Product.Name == contProdname:
				rowc.Product.Attr("MIB Configuration Required?").SelectValue( mibval)
				if rowc.Product.Name == "Experion Enterprise Group":
					if mibval == "No":
						rowc.Product.AllowAttr('QVCS Support')
						if rowc.Product.Attr('QVCS Support').GetValue() == '':
							rowc.Product.Attr('QVCS Support').SelectValue('No')
					else:
						rowc.Product.DisallowAttr('QVCS Support')
				else:
					if mibval == "No":
						rowc.Product.AllowAttrValues('SerC_CG_IO_Family_Type','Series C')
						if rowc.Product.Attr('SerC_CG_IO_Family_Type').GetValue() == '':
							rowc.Product.Attr("SerC_CG_IO_Family_Type").SelectValue('Series C')
							if rowc.Product.Attr('SerC_CG_Power_System_Type').GetValue() == '':
								rowc.Product.AllowAttrValues('SerC_CG_Power_System_Type','Minimum Required Redundant')
								rowc.Product.Attr('SerC_CG_Power_System_Type').SelectValue('Minimum Required Redundant')
					elif mibval == "Yes":
						rowc.Product.DisallowAttrValues('SerC_CG_IO_Family_Type','Series C')	
						if rowc.Product.Attr('SerC_CG_IO_Family_Type').GetValue() == 'Series-C Mark II':
							rowc.Product.Attr("SerC_CG_IO_Family_Type").SelectValue('Series-C Mark II')
							#rowc.Product.AllowAttr('SerC_GC_Profibus_Gateway_Interface')
							rowc.Product.AllowAttr('SerC_CG_MIB_Configuration_Required')  
			rowc.Calculate()

cont = Product.GetContainerByName('CE_System_Cont')
mibval = Product.Attr('MIB Configuration Required?').GetValue()
for row in cont.Rows:
	contprod = row.Product
	if contprod.Name in ['Experion Enterprise System','C300 System']:
		contprod.Attr("MIB Configuration Required?").SelectValue(mibval)
		if contprod.Name == 'Experion Enterprise System':
			assignMIBval(contprod,'Experion_Enterprise_Cont','Experion Enterprise Group',mibval)
		if contprod.Name == 'C300 System':
			assignMIBval(contprod,'Series_C_Control_Groups_Cont','Series-C Control Group',mibval)
		row.Calculate()
cont.Calculate()