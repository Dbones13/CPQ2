def quantity_display(parts_dict, attrs):
    quantity1 = attrs.fps_10a + attrs.fps_10a_2
    parts_dict['AL-FPCB01'] = quantity1
    quantity2 = attrs.fps_20a + attrs.fps_20a_2
    parts_dict['AL-FPCB02'] = quantity2
    return parts_dict