# =========================================================================================================
#   Component: GS_PCN_Populate_Write_Ins
#      Author: Prashant Yadav
#   Copyright: Honeywell Inc
#     Purpose: This script is used inside PCN Hardening Product to populate Write-Ins Product
# ========================================================================================================
def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def activities_unit_list(product):
	if product.PartNumber == 'CYBER_APP_CNTRL':
		cyber_activities_cont_show_hide(product)
	unit_cost = 0.00
	list_price = 0.00
	activities = product.GetContainerByName('Activities')
	for row in activities.Rows:
		if row['Identifier'] not in ['Total','On-Site','Off-Site']:
			edit_hrs = float(row['Edit Hours']) if row['Edit Hours'] != '' else 0.00
			cost = float(row['Pricing']) if row['Pricing'] !='' else 0.00
			price = float(row['List_Price']) if row['List_Price'] !='' else 0.00
			unit_cost += cost * edit_hrs
			list_price += price * edit_hrs
	return unit_cost,list_price

def activities_cont_show_hide(product):
	D1 = D2 = D3 = 0
	for rows in product.GetContainerByName('Domain').Rows:
		if rows.RowIndex != 0:
			D1 += int(rows['Domain_1']) if rows['Domain_1'] !='' else 0
			D2 += int(rows['Domain_2']) if rows['Domain_2'] !='' else 0
			D3 += int(rows['Domain_3']) if rows['Domain_3'] !='' else 0
	domain_row = D1+D2+D3
	if domain_row > 0:
		product.AllowAttr('Activities')
	else:
		product.DisallowAttr('Activities')

def cyber_activities_cont_show_hide(product):
	cyber_app_servers = 0
	validated_stations = 0
	non_validated_stations = 0
	validated_servers = 0
	non_validated_servers = 0
	migrations = 0
	Total = 0
	for row in product.GetContainerByName('Network Level Container').Rows:
		cyber_app_servers += int(row['Number of Cyber App Control Servers']) if row['Number of Cyber App Control Servers'] != '' else 0
		validated_stations += int(row['Validated Stations']) if row['Validated Stations'] != '' else 0
		non_validated_stations += int(row['Non‐Validated Stations']) if row['Non‐Validated Stations'] != '' else 0
		validated_servers += int(row['Validated Servers']) if row['Validated Servers'] != '' else 0
		non_validated_servers += int(row['Non‐Validated Servers']) if row['Non‐Validated Servers'] != '' else 0
		migrations += int(row['MIGRATIONS ONLY - Existing Server & Station Clients']) if row['MIGRATIONS ONLY - Existing Server & Station Clients'] != '' else 0
	Total = cyber_app_servers + validated_stations + non_validated_stations + non_validated_stations + validated_servers + non_validated_servers + migrations
	if Total > 0:
		product.AllowAttr('Activities')
	else:
		activity = product.GetContainerByName('Activities')
		deletelist = [row.RowIndex for row in activity.Rows]
		if len(deletelist) > 0:
			for row_index in sorted(deletelist, reverse=True):
				activity.DeleteRow(row_index)
		product.DisallowAttr('Activities')

def remove_rows_by_system_id(container, system_id):
	rows_to_delete = [row.RowIndex for row in container.Rows if row.Product.SystemId == system_id]
	for row in rows_to_delete:
		container.DeleteRow(row)

def write_in(product):
	if product.PartNumber == 'PCN':
		cyber_care_sys_id = 'Write-In_Entitlement-Hardening_Cyber_Care_cpq'
		hardening_sys_id = 'Write-In_Entitlement-Hardening_Services_cpq'
		factor = 0.30
		writeInPartNumber_hardening = 'Write-In Entitlement-Hardening Services'
		writeInPartNumber_care = 'Write-In Entitlement-Hardening Cyber Care'
	elif product.PartNumber == 'CYBER_APP_CNTRL':
		cyber_care_sys_id = 'Write-In Entitlement-Cyber App Control Care_cpq'
		hardening_sys_id = 'Write-In Entitlement-Cyber App Control_cpq'
		factor = 0.35
		writeInPartNumber_hardening = 'Write-In Entitlement-Cyber App Control'
		writeInPartNumber_care = 'Write-In Entitlement-Cyber App Control Care'
	return cyber_care_sys_id,hardening_sys_id,factor,writeInPartNumber_hardening,writeInPartNumber_care

def addWriteIn(product):
	writein_cont = product.GetContainerByName('Write-In Entitlements for Cyber')

	cyber_care_sys_id,hardening_sys_id,factor,writeInPartNumber_hardening,writeInPartNumber_care = write_in(product)

	unit_cost,list_price = activities_unit_list(product)

	cyberCare = product.Attr('Enhanced Support-Cyber CARE').GetValue()
	hardening = product.Attr('PCN Hardening Standard Technical Support').GetValue()

	cyber_flag = 0
	for row in writein_cont.Rows:
		if row.Product.SystemId == cyber_care_sys_id:
			cyber_flag = 1
			break
	if cyberCare != '' and cyber_flag == 0:
		writeInProduct = SqlHelper.GetFirst("SELECT Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts(nolock) where Product = '"+writeInPartNumber_care+"'")
		writein_cyber = writein_cont.AddNewRow(cyber_care_sys_id, False)
		writein_cyber.Product.Attr('CustomPrice_2').AssignValue(str(round(float(unit_cost) * float(factor),2))) #Cost
		writein_cyber.Product.Attr('CustomPrice').AssignValue(str(round(float(list_price) * float(factor),2))) #List Price
		writein_cyber.Product.Attr('CurrentCurrencyRate').AssignValue('0')
		if writeInProduct:
			writein_cyber.Product.Attr('Product Line').AssignValue(writeInProduct.ProductLine)
			writein_cyber.Product.Attr('Product Line Description').AssignValue(writeInProduct.ProductLineDescription)
			writein_cyber.Product.Attr('Product line sub group').AssignValue(writeInProduct.ProductLineSubGroup)
			writein_cyber.Product.Attr('PLSG description').AssignValue(writeInProduct.ProductLineSubGroupDescription)
		writein_cyber.Product.ApplyRules()
		writein_cyber.ApplyProductChanges()
		writein_cyber.Calculate()
		writein_cont.Calculate()
		#remove_rows_by_system_id(product.GetContainerByName('Write-In Entitlements for Cyber'), hardening_sys_id)

	'''elif cyberCare == '':
		remove_rows_by_system_id(product.GetContainerByName('Write-In Entitlements for Cyber'), cyber_care_sys_id)'''

	if writein_cont.Rows.Count == 0 and hardening != '' and cyberCare == '':
		writeInProduct = SqlHelper.GetFirst("SELECT Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts(nolock) where Product = '"+writeInPartNumber_hardening+"'")
		writein_hard = writein_cont.AddNewRow(hardening_sys_id, False)
		writein_hard.Product.Attr('CustomPrice_2').AssignValue(str(round(float(unit_cost) * 0.20,2)))
		writein_hard.Product.Attr('CustomPrice').AssignValue(str(round(float(list_price) * 0.20, 2)))
		writein_hard.Product.Attr('CurrentCurrencyRate').AssignValue('0')
		if writeInProduct:
			writein_hard.Product.Attr('Product Line').AssignValue(writeInProduct.ProductLine)
			writein_hard.Product.Attr('Product Line Description').AssignValue(writeInProduct.ProductLineDescription)
			writein_hard.Product.Attr('Product line sub group').AssignValue(writeInProduct.ProductLineSubGroup)
			writein_hard.Product.Attr('PLSG description').AssignValue(writeInProduct.ProductLineSubGroupDescription)
		writein_hard.Product.ApplyRules()
		writein_hard.ApplyProductChanges()
		writein_hard.Calculate()
		writein_cont.Calculate()
	if product.PartNumber == 'PCN':
		activities_cont_show_hide(product)

def updateWriteIn(product):
	write_cont = product.GetContainerByName('Write-In Entitlements for Cyber')
	cyberCare = product.Attr('Enhanced Support-Cyber CARE').GetValue()

	cyber_care_sys_id,hardening_sys_id,factor,writeInPartNumber_hardening,writeInPartNumber_care = write_in(product)

	unit_cost,list_price = activities_unit_list(product)
	if write_cont.Rows.Count > 0:
		for row in write_cont.Rows:
			if row.Product.SystemId == hardening_sys_id and cyberCare =='':
				row.Product.Attr('CustomPrice_2').AssignValue(str(round(float(unit_cost) * 0.20,2)))
				row.Product.Attr('CustomPrice').AssignValue(str(round(float(list_price) * 0.20, 2)))
				row.Product.Attr('CurrentCurrencyRate').AssignValue('0')    
				row.Product.ApplyRules()
				row.ApplyProductChanges()
				row.Calculate()
				write_cont.Calculate()             
			elif row.Product.SystemId == cyber_care_sys_id and cyberCare !='':
				row.Product.Attr('CustomPrice_2').AssignValue(str(round(float(unit_cost) * float(factor),2)))
				row.Product.Attr('CustomPrice').AssignValue(str(round(float(list_price) * float(factor),2)))
				row.Product.Attr('CurrentCurrencyRate').AssignValue('0')
				row.Product.ApplyRules()
				row.ApplyProductChanges()
				row.Calculate()
				write_cont.Calculate()   
			else:
				addWriteIn(product)
	else:
		addWriteIn(product)
	if product.PartNumber == 'PCN':
		activities_cont_show_hide(product)