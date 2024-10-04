import json , os
import tldextract
from urllib.parse import urlparse



os.system('curl -s -k https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/hackerone_data.json -o input.json')
# Load input JSON from a file
with open('input.json', 'r') as file:
    input_json = json.load(file)

# Function to extract domain from asset identifier
def get_domain(asset_identifier):
    # Extract the domain components using tldextract
    extracted = tldextract.extract(asset_identifier)
    
    # Check if domain and suffix are valid
    if extracted.domain and extracted.suffix:
        # Reconstruct the cleaned domain
        if extracted.subdomain:
            cleaned_domain = f"{extracted.subdomain}.{extracted.domain}.{extracted.suffix}"
        else:
            cleaned_domain = f"{extracted.domain}.{extracted.suffix}"
    else:
        return None  # Return None if domain or suffix are missing

    # Parse URL if necessary
    if '://' in cleaned_domain:
        parsed_url = urlparse(cleaned_domain)
        domain = parsed_url.netloc
    else:
        domain = cleaned_domain

    # Handle wildcard patterns
    if domain.startswith('*'):
        # Remove the leading '*' to get the domain
        domain = domain.lstrip('*.')
    elif '-*' in domain:
        # If wildcard is in the middle, replace '-*' with an empty string
        domain = domain.replace('-*', '')
    elif '*-' in domain:
        # If wildcard is in the middle, replace '*-' with an empty string
        domain = domain.replace('*-', '')

    return domain

# Function to transform the program data to the desired output format
def transform_program_data(program):
    program_name = program["name"]

    # Get in-scope and out-of-scope assets based on criteria and asset_type "wildcard" or "url"
    scopes = [
        get_domain(scope["asset_identifier"]) for scope in program["targets"]["in_scope"]
        if scope["eligible_for_submission"] and (scope["asset_type"].lower() == "wildcard" or scope["asset_type"].lower() == "url")
    ]
    
    # Filter out None values
    scopes = [scope for scope in scopes if scope is not None]

    ooscopes = [
        get_domain(scope["asset_identifier"]) for scope in program["targets"]["out_of_scope"]
        if not scope["eligible_for_submission"] and (scope["asset_type"].lower() == "wildcard" or scope["asset_type"].lower() == "url")
    ]
    
    # Filter out None values
    ooscopes = [scope for scope in ooscopes if scope is not None]

    return {
        "programm_name": program_name,
        "config": {
            "key1": "value1",
            "key2": "value2"
        },
        "scopes": scopes,
        "ooscopes": ooscopes
    }

# Filter the program with name containing "cbre" and transform it
for program in input_json:
    if "kahootz" in program["name"].lower():
        transformed_data = transform_program_data(program)
# Write the output JSON to a file
        with open('../tmp/kahootz.json', 'w') as file:
            json.dump(transformed_data, file, indent=4)

    if "moov" in program["name"].lower():
        transformed_data = transform_program_data(program)
# Write the output JSON to a file
        with open('../tmp/moov.json', 'w') as file:
            json.dump(transformed_data, file, indent=4)

    if "productboard" in program["name"].lower():
        transformed_data = transform_program_data(program)
# Write the output JSON to a file
        with open('../tmp/productboard.json', 'w') as file:
            json.dump(transformed_data, file, indent=4)
print("Output written to 'output.json'")