# coding: utf-8


def format_table_data(img_data):
    result = {}
    key = img_data[0][1]
    value = img_data[0][2]
    pairs = zip(key, value)
    for k, v in pairs:
        k_text = k.get('text')
        v_text = v.get('text')
        k_data = k_text[0] if k_text else None
        v_data = v_text[0] if v_text else None
        result.update({k_data: v_data})
    return result
