def parse_form_data_to_json(form_data: bytes, exclude: list = None) -> dict:
    exclude = list if exclude is None else exclude
    values = form_data.decode('utf-8').split("&")
    return {k: v for k, v in (v.split("=") for v in values) if k not in exclude}
