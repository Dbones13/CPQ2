Session['FAT_required'] = Product.Attr('Graphics_Migration_FAT_required?').GetValue()
Trace.Write("sessionfat"+str(Session['FAT_required']))