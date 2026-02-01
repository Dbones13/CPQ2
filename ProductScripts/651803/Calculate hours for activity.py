from GS_Populate_Labour_WTW import populateWTW
from GS_CyberProductModule import CyberProduct
import System
import math
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
activity_container = Product.GetContainerByName('Activities')
MSS_hour_activities = SqlHelper.GetList("SELECT * FROM CT_PRODUCT_VARIABLES WHERE Product = 'MSS'").ToList()
patch_antivirus = Product.Attr('Patching and Anti-Virus Required').GetValue()
secure_conn = Product.Attr('Secure Remote Access').GetValue()
pcn_monitoring = Product.Attr('PCN Monitoring Required').GetValue()
microsoft_update = Product.Attr('Microsoft Updates Install').GetValue()
ip_security = Product.Attr('IP Security Tunnel Required').GetValue()
repo_server = Product.Attr('Repository Server Required').GetValue()
fat_veri = Product.Attr('FAT Document Verification and Execution').GetValue()
sat_veri = Product.Attr('SAT Document Verification and Execution').GetValue()
fds_dds = Product.Attr('FDS & DDS Documentation Required').GetValue()
redundancy = Product.Attr('Secure Remote Access Redundancy Required').GetValue()
a1_hours = 0
a2_hours = 0
a3_hours = 0
a4_hours = 0
a5_hours = 0
a6_hours = 0
a7_hours = 0
a8_hours = 0
a9_hours = 0
a10_hours = 0
a11_hours = 0
a16_index = -1
row_index = -1

num_win = float(Product.Attr('Number of Windows Assets').GetValue()) if Product.Attr('Number of Windows Assets').GetValue() != '' else 0.00
num_net = float(Product.Attr('Number of Network Assets').GetValue()) if Product.Attr('Number of Network Assets').GetValue() != '' else 0.00

if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
	if activity_container.Rows.Count>0:
		for row in activity_container.Rows:
			row_index = row_index + 1
			if row['Identifier'] == 'A1':
				if redundancy =="Yes":
					val = 2
				else:
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Servers_Config_Installation_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a1_hours = float(row['Hours'])
			if row['Identifier'] == 'A2':
				val = 0
				if patch_antivirus == 'Yes':
					val = num_win
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_AV_Client_Installation_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a2_hours = float(row['Hours'])
			if row['Identifier'] == 'A3':
				val = 0
				if patch_antivirus == 'Yes':
					val = num_win
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Config_of_WSUS_Registry_End Nodes_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a3_hours = float(row['Hours'])
			if row['Identifier'] == 'A4':
				val = 0
				if patch_antivirus == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Config_of_EPO_WSUS_Rules_Factor').Select(lambda y: y.Value).First()) * val)))
				a4_hours = float(row['Hours'])
			if row['Identifier'] == 'A5':
				val = 0
				if patch_antivirus =="Yes" and microsoft_update =="Yes":
					val = num_win
				elif patch_antivirus =="Yes" and microsoft_update =="":
					val = 0
				else:
					val = 0
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Install_Latest_Microsoft_updates_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a5_hours = float(row['Hours'])
			if row['Identifier'] == 'A6':
				val = 0
				if pcn_monitoring == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Asset_Discovery_Importing_PLs_for_Monitoring_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a6_hours = float(row['Hours'])
			if row['Identifier'] == 'A7':
				val = 0
				if pcn_monitoring == 'Yes':
					val = num_win + num_net
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Config_of_PLs_for_Performance Monitoring_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a7_hours = float(row['Hours'])
			if row['Identifier'] == 'A8':
				val = 0
				if pcn_monitoring == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Monitoring_Data_Validation_Report_Generation_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a8_hours = float(row['Hours'])
			if row['Identifier'] == 'A9':
				val = 0
				if patch_antivirus =="Yes":
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Network_Support_for_MSS_Firewall_Rules_for_AV_WSUS_Monitoring_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a9_hours = float(row['Hours'])
			if row['Identifier'] == 'A10':
				val = 0
				if ip_security == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_IP_Security_Tunnel_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a10_hours = float(row['Hours'])
			if row['Identifier'] == 'A11':
				val = 0
				if repo_server == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Repository_Server_Onsite_Factor').Select(lambda y: y.Value).First()) * val)))
				a11_hours = float(row['Hours'])
			if row['Identifier'] == 'A12':
				val = 0
				if fds_dds == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_FDS_DDS_Documentation_Factor').Select(lambda y: y.Value).First()) * val)))
			if row['Identifier'] == 'A13':
				val = 0
				if fat_veri == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_FAT_Document_Verification_Execution_Factor').Select(lambda y: y.Value).First()) * val)))
			if row['Identifier'] == 'A14':
				val = 0
				if sat_veri == 'Yes':
					val = 1
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_SAT_Document_Verification_Execution_Factor').Select(lambda y: y.Value).First()) * val)))
			if row['Identifier'] == 'A15':
				row['Hours'] = str(int(math.ceil(float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Travel_Time_Factor').Select(lambda y: y.Value).First()) * float(MSS_hour_activities.Where(lambda x: x.Variable == 'Var_Travel_Time_Prod_Input_Factor').Select(lambda y: y.Value).First()))))
			if row['Identifier'] == 'A16':
				a16_index = row_index
			if Product.Attr('calculate_value_set').GetValue() == "True" or row['Edit Hours'] == '':
				row['Edit Hours'] = row['Hours']
		total_hours = a1_hours + a2_hours + a3_hours + a4_hours + a5_hours + a9_hours + a11_hours
		cybert_coord_per =  math.ceil(total_hours*0.10)

		if cybert_coord_per <= 8:
			cyber_coord_hrs = 8
		elif cybert_coord_per >= 40:
			cyber_coord_hrs = 40
		else:
			cyber_coord_hrs = cybert_coord_per
		activity_container.Rows[a16_index]['Hours'] = str(int(math.ceil(cyber_coord_hrs)))
		if Product.Attr('calculate_value_set').GetValue() == "True" or activity_container.Rows[a16_index]['Edit Hours'] =='':
			activity_container.Rows[a16_index]['Edit Hours'] = activity_container.Rows[a16_index]['Hours']
		cyber = CyberProduct(Quote, Product, TagParserQuote)
		cyber.populateActivityListPricing('Activities')
		populateWTW(['Activities'], Product, Quote)