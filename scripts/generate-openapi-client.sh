#!/usr/bin/env bash

# This script uses the 'openapi-python-client' tool to generate a Python HTTP client from OpenAPI specification.

# remove previous output if any
/bin/rm -rf things-api-client
/bin/rm -rf local/IndustrialAPI/client

# generate new client
openapi-python-client generate --path local/IndustrialAPI/spec.yml

# move generate Python package as a subpackage of ours
mv things-api-client/things_api_client local/IndustrialAPI/client

# remove temporary output
/bin/rm -rf things-api-client