#--------------------------------------------------------------
#					Change History Log
#--------------------------------------------------------------
# Description: Script to populate CF_MigrationYes
#--------------------------------------------------------------
# Date 			Name					    Version   Comment
# 16-Aug-2023   Yashwanth Boya				Intial Creation

if Session["prevent_execution"] != "true":
	productList = [items.ProductName for items in Quote.MainItems]
	Quote.GetCustomField('CF_MigrationYes').Content = 'Both' if ("Migration" in productList or "Migration_New" in productList) and "New / Expansion Project" in productList else 'New / Expansion Project'