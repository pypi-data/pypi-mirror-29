## Summary
mechanic is a "toolkit" for building an API in Python from an OpenAPI 3.0 specification file. It (at least partially) 
bridges the gap between the contract (the API spec) and the enforcement of that contract (the code). 

mechanic was created because swagger codegen did not sufficiently meet our code generation needs. Our biggest 2 
requirements were:
- Ability to generate server stubs without overriding existing code/business logic.
- Generate DB models and serialization/deserialization from the OpenAPI 3.0 spec.

#### What does it do?
- Generates SQLAlchemy Models and Marshmallow schemas.
- Generates API endpoint controllers associated with the models and schemas.
- Generates Flask-Restplus starter code that gets you from zero to API in seconds.
- Adds some useful extensions to the OpenAPI 3.0 spec.

## Quickstart
```bash
pip install mechanic-gen
mechanic scaffold <openapi_file> <output_dir>
cd <output_dir>
pip install -r requirements.txt
gunicorn wsgi:application -b 0.0.0.0:8080
```
- Go to http://localhost:8080/openapi for your OpenAPI 3.0 documentation
- Go to http://localhost:8080/swagger for your Swagger 2.0 documentation generate from Flask-Restplus

#### Generate individual files
```bash
# generate marshmallow schemas
mechanic generate --schemas <openapi_file> <output_file>
# generate sqlalchemy models
mechanic generate --models <openapi_file> <output_file>
# generate marshmallow schemas and sqlalchemy models in same file
mechanic generate --models --schemas <openapi_file> <output_file>
# generate flask-restplus namespace
mechanic generate --namespaces <openapi_file> <output_file>
```
## Help
See [mechanic extensions](docs/mechanic-extensions.md) for useful extensions to add to your OpenAPI 3.0 file.  
See [mechanic FAQ](docs/mechanic-faq.md).
