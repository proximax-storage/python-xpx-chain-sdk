# SWAGGER

This folder should only be used by developers of the NEM2 SDK, and allows us to auto-generate the data-transfer object models and REST API methods using `swagger-codegen-cli`. Please note that Swagger is currently **not** in use by the NEM2-SDK, and is merely a potential feature if Swagger's automated codegen improves in quality (by using native async/await).

## Dependencies

1. Java
2. swagger-codegen-cli

## Installation

In order to use the following code, we will assume `swagger-codegen-cli-X.X.X.jar` is installed in the PATH (for example, `~/bin/`).

Next, create a symlink `swagger-codegen-cli.jar` pointing to `swagger-codegen-cli-X.X.X.jar` in the path (for example, run `ln -s ~/bin/swagger-codegen-cli-2.4.7.jar ~/bin/swagger-codegen-cli.jar` on Unix).

## Codegen

In order to generate the DTO code, run the following from the project directory:

```bash
# Generate code
java -jar ~/bin/swagger-codegen-cli.jar generate \
    --input-spec swagger/swagger.yaml \
    --lang python \
    --output swagger/codegen

# Remove existing xpx chain infrastructure folder.
rm -r xpxchain/infrastructure

# Move generate code to infrastructure.
mv swagger/codegen/swagger_client xpxchain/infrastructure

# Remove remaining code
rm -r swagger/codegen
```

This has all been automated, in a cross-platform manner, with `codegen.py`.
