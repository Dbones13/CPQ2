from GS_ApplyTariff_Mod import update_write_in_tariff_items,add_write_in_tariff,has_valid_tariff_product,delete_write_in_tariff_product

lob = Quote.GetCustomField('Booking LOB').Content
quote_type = Quote.GetCustomField('Quote Type').Content

if lob in ["CCC", "LSS", "HCP", "PAS"] and quote_type in ['Projects']:
    booking_country = Quote.GetCustomField('Booking Country').Content
    
    tariff_valid,coo_map,markup_rates,tariff_details = has_valid_tariff_product(Quote, booking_country)

    if tariff_valid:
        add_write_in_tariff(Quote, ProductHelper)
        update_write_in_tariff_items(Quote,coo_map,markup_rates,tariff_details)
    else:
        delete_write_in_tariff_product(Quote)