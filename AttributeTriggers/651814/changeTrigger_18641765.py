add_media = Product.Attr('Trace_Software_Additional_Media_Kits').SelectedValue.Display
Product.Attr('Trace_Software_Additional_Media_Kits').SelectedValue.Display = str(round(float(add_media)))
if int(round(float(add_media))) < 0 or int(round(float(add_media))) > 5:
	Product.Attr('Trace_Software_Additional_Media_Kits').SelectedValue.Display = '0'