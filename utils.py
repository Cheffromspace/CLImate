import json


def output_json(data):
    json_output = json.dumps(data, indent=2)
    print(json_output)


def extract_response_text(response, expected_output_tag, include_output_tag=False):
    start_tag = f"<{expected_output_tag}>"
    end_tag = f"</{expected_output_tag}>"
    start_index = response.find(start_tag)
    end_index = response.find(end_tag)
    if start_index != -1 and end_index != -1:
        if include_output_tag:
            end_index += len(end_tag)
        else:
            start_index += len(start_tag)
        extracted_text = response[start_index:end_index].strip()
        return extracted_text
    else:
        raise ValueError(
            f"Expected tag <{expected_output_tag}> not found in the API response."
        )
