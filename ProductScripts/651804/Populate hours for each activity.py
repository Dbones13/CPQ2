import System
import math
from GS_Populate_Labour_WTW import populateWTW
from GS_CyberProductModule import CyberProduct
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
activity_container = Product.GetContainerByName('Activities')


D1 = D2 = D3 = 0
for rows in Product.GetContainerByName('Domain').Rows:
	if rows.RowIndex != 0:
		D1 += int(rows['Domain_1']) if rows['Domain_1'] !='' else 0
		D2 += int(rows['Domain_2']) if rows['Domain_2'] !='' else 0
		D3 += int(rows['Domain_3']) if rows['Domain_3'] !='' else 0
domain_row = D1+D2+D3
domain_count = len([value for value in (D1, D2, D3) if value > 0])

if domain_row == 0:
	activity_container.Rows.Clear()

if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
	if activity_container.Rows.Count > 0:
		pcn_activites = SqlHelper.GetList("Select PartNumber, Activity,Identifier,Hours FROM CT_ACTIVITIES where Product = 'PCN Hardening' and hours <> ''").ToList()
		fat_document_value = Product.Attr("FAT Document Verification and Execution").GetValue()
		a1_hours = 0
		a2_hours = 0
		a3_hours = 0
		a4_hours = 0
		a5_hours = 0
		a7_hours = 0
		a8_hours = 0
		a6_index = -1
		row_index = -1

		for row in activity_container.Rows:
			row_index = row_index + 1

			if row['Identifier'] == 'A2' and domain_count > 0: #Customer Assessment/Evaluation Phase
				row['Hours'] = str(24)
				a2_hours = int(row['Hours'])
			elif row['Identifier'] ==  'A4': #Final Phase Documentation Preparation
				row['Hours'] = str(16)
				a4_hours = int(row['Hours'])
			elif row['Identifier'] == 'A1' and domain_count > 0: #Project KickOff Meeting
				row['Hours'] = str(8 + (domain_count - 1) * 2)
				a1_hours = int(row['Hours'])
			elif row['Identifier'] == 'A7':  #Factory Acceptance Testing
				if fat_document_value != '':
					row['Hours'] = '40'
				else:
					row['Hours'] = '0'
				a7_hours = int(row['Hours'])
			elif row['Identifier'] == 'A8' and domain_count > 0: #Include Functional Design Specification (FDS) Documentation &Include Detail Design Specification (DDS) Documentation
				if Product.Attr("FDS & DDS Documentation Required").GetValue() != '':
					if domain_count > 0:
						row['Hours'] = str(48) if domain_count < 2 else str(48 + 16 *(domain_count-1))
					else:
						row['Hours'] = '0'
				else:
					row['Hours'] = '0'
				a8_hours = int(row['Hours'])

			elif row['Identifier'] == 'A3':  #Policy Enforcement Deployment (include Systems, Network and Firewalls)
				domain_container = Product.GetContainerByName('Domain')
				attr_value = Product.Attr('Number of Domains').GetValue()
				d1_windows,d1_network,d1_firewalls,domain_1 = 0,0,0,0
				d2_windows,d2_network,d2_firewalls,domain_2 = 0,0,0,0
				d3_windows,d3_network,d3_firewalls,domain_3 = 0,0,0,0
				for dom_row in domain_container.Rows:
					col=dom_row.Columns
					if dom_row.RowIndex == 1:
						d1_windows +=int(col['Domain_1'].Value) * 1
						d2_windows +=int(col['Domain_2'].Value) * 1
						d3_windows +=int(col['Domain_3'].Value) * 1
					if dom_row.RowIndex == 2:
						d1_network +=int(col['Domain_1'].Value) * 1
						d2_network +=int(col['Domain_2'].Value) * 1
						d3_network +=int(col['Domain_3'].Value) * 1
					if dom_row.RowIndex == 3:
						d1_firewalls +=int(col['Domain_1'].Value) * 4
						d2_firewalls +=int(col['Domain_2'].Value) * 4
						d3_firewalls +=int(col['Domain_3'].Value) * 4
					if attr_value =='1':
						domain_1 = 40 if (d1_windows + d1_network + d1_firewalls) <=40 else (d1_windows + d1_network + d1_firewalls)
					elif attr_value =='2':
						domain_1 = 40 if (d1_windows + d1_network + d1_firewalls) <=40 else (d1_windows + d1_network + d1_firewalls)
						domain_2 = 40 if 0 < (d2_windows + d2_network + d2_firewalls) <=40 else (d2_windows + d2_network + d2_firewalls)
					else:
						domain_1 = 40 if (d1_windows + d1_network + d1_firewalls) <=40 else (d1_windows + d1_network + d1_firewalls)
						domain_2 = 40 if 0 < (d2_windows + d2_network + d2_firewalls) <=40 else (d2_windows + d2_network + d2_firewalls)
						domain_3 = 40 if 0 < (d3_windows + d3_network + d3_firewalls) <=40 else (d3_windows + d3_network + d3_firewalls)
				domain_hrs = domain_1 + domain_2 + domain_3
				row['Hours'] = str(domain_hrs)
				a3_hours = int(row['Hours'])

			elif row['Identifier'] == 'A5': #Travel (onsite to customer)
				if fat_document_value == 'Yes':
					row['Hours'] = '32'
				else:
					row['Hours'] = '16'
				a5_hours = int(row['Hours'])
			elif row['Identifier'] == 'A6': #Cyber Coordination - 10%
				a6_index = row_index
			if Product.Attr('calculate_value_set').GetValue() == "True" or row['Edit Hours'] == '':
				row['Edit Hours'] = row['Hours']
			row.Calculate()

		#Calculate A6 hours outside for loop
		total_hours = int(math.ceil((a1_hours + a3_hours  + a7_hours ) * 0.10))
		r = activity_container.Rows[a6_index]

		if total_hours <= 8:
			r['Hours'] = '8'
		elif total_hours >= 40:
			r['Hours'] = '40'
		else:
			r['Hours'] = str(total_hours)
		if Product.Attr('calculate_value_set').GetValue() == "True" or r['Edit Hours'] == '':
			r['Edit Hours'] = r['Hours']

		cyber = CyberProduct(Quote, Product, TagParserQuote)
		cyber.populateActivityListPricing('Activities')
	populateWTW(['Activities'], Product, Quote)