def getContainer(Name):
	return Product.GetContainerByName(Name)

GraphicsMigrationDisplyShape = getContainer('Graphics_Migration_Displays_Shapes_Faceplates')
colValuesDict = {"Experion_shapes_multiplier": "1.0"}
for row in GraphicsMigrationDisplyShape.Rows:
	for col in row.Columns:
		defaultVal = colValuesDict.get(col.Name)
		if defaultVal:
			row[col.Name] = defaultVal
GraphicsMigrationDisplyShape.Calculate()

'''if Product.Attr('Scope').GetValue() != 'HW/SW':
	attr1 = Product.Attr("Migration_Configuration_Is_Standard_Builds_used").SelectValue('No')
	attr2 = Product.Attr("Migration_Graphics_Using_device_control_digital").SelectValue('No')
	attr3 = Product.Attr("Migration_Graphics_Have_multiple_DI_or_DO").SelectValue('No')
	attr4 = Product.Attr("Graphics_Migration_Is_the_system_connected_to").SelectValue('No')
	attr5 = Product.Attr("Graphics_Migration_Require_multi_tag_shapes").SelectValue('Yes')
	attr6 = Product.Attr("Graphics_Migration_Have_process_module_point").SelectValue('No')
	attr7 = Product.Attr("Graphics_Migration_Require_an_HMI_interface_for_AM").SelectValue('No')
	attr8 = Product.Attr("Migration_Graphics_Have_array_point_that_requires").SelectValue('No')
	attr9 = Product.Attr("Migration_Graphics_Willing_to_accept_alternative").SelectValue('No')
	attr10 = Product.Attr("Graphics_Migration_Have_specific_native_or_GUS").SelectValue('No')
	attr11 = Product.Attr("Graphics_Migration_Have_specific_native_or_GUS").SelectValue('No')
	attr12 = Product.Attr("Graphics_Migration_Alarm_groups_configured?").SelectValue('No')
	attr13 = Product.Attr("ATT_GMNUMSL").AssignValue('0')'''