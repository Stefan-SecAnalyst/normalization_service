



def normalizer (record, rules):
    normalized = {}  # Start an empty dict for output
    for field, value in record.items():
        if field in rules:
            rule = rules[field]

            if rule.get("type") == "datetime":
                normalized = datetime_normalizer(value, rule)


            normalized_value = value
            normalized[field] = normalized_value
        else:
            normalized[field] = value
    return normalized



def datetime_normalizer(value, rule):
    # Implement datetime normalization logic here
    
    from datetime import datetime
    input_fmt = rule.get("input_format")
    output_fmt = rule.get("output_format", input_fmt)
    
    try:
        dt = datetime.strptime(value, input_fmt)
        normalized_value = dt.strftime(output_fmt)
    except Exception:
        normalized_value = value

    return normalized_value
