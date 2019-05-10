# REST

Integrations to generate the base models used to guide the generation of the API models in the nem2 library.

## Dependencies

1. pyyaml
2. bravado-core
3. curl

## Validating Spec

To validate the OpenAPI specification, run the following code snippets.

```python
import yaml
from bravado_core.spec import Spec

with open('swagger.yaml') as f:
    raw_spec = yaml.load(f, Loader=yaml.Loader)
spec = Spec.from_dict(raw_spec, config={'use_models': False})
```

## Swagger Codegen

To auto-generate code for the data-transfer objects, run the following code snippet: this should auto-generate DTO models for the REST API.

```bash
curl -H "Content-type: application/json" \
    -X POST \
    -d '{"options": {"packageName": "nem2"},"swaggerUrl": "https://raw.githubusercontent.com/Alexhuszagh/nem2-sdk-python/master/rest/swagger.yaml"}' \
    https://generator.swagger.io/api/gen/clients/python
```
