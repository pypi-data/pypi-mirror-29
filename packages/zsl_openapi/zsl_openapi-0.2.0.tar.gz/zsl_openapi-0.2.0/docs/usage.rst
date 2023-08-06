=====
Usage
=====

In high level, it is enough to define container with the :class:`zsl_openapi.module.OpenAPIModule`.

::

    class StorageContainer(WebContainer):
        open_api = OpenAPIModule

Then you may use CLI `open_api` command with your application.

::

    python app.py \
        open_api generate \
        --package storage.models.persistent \
        --output api/openapi_spec_full.yml \
        --description api/openapi_spec.yml

The complete sample `app.py` may look like this. Change the container name from `StorageContainer` to whatever has
meaning for you.

::

    class StorageContainer(WebContainer):
        ... # The other modules.
        open_api = OpenAPIModule


    def main() -> None:
        initialize()
        run()


    def initialize() -> None:
        if os.environ.get('PROFILE'):
            set_profile(os.environ['PROFILE'])
        else:
            logging.getLogger().warning("Running without a setting profile. This is usually unwanted, set up the profile "
                                        "using PROFILE environment variable and corresponding file <PROFILE>.cfg in "
                                        "settings directory.")
        app = Zsl(app_name, version=__version__, modules=StorageContainer.modules())
        logging.getLogger(app_name).debug("ZSL app created {0}.".format(app))


    @inject(zsl_cli=ZslCli)
    def run(zsl_cli: ZslCli) -> None:
        zsl_cli.cli()


    if __name__ == "__main__":
        main()

And complete API description (`openapi_spec.yml`) may look like this:

::

    swagger: "2.0"
    info:
      description: "Music Storage API version 1 specification. The storage API provides a convenient way to browse the catalogues and perform maintenance tasks"
      version: "1"
      title: "MusicStorage API v1"
      termsOfService: "Feel free to use!"
      contact:
        email: "babka@atteq.com"
      license:
        name: "BSD"
        url: "https://opensource.org/licenses/BSD-3-Clause"


Then you can use the `python app.py open_api generate` CLI command to generate OpenAPI specification from your python
persistent models.

The possible options of the `generate` command:

--package <package_name>        the package/module where the persistent modules are sought. If there are more, you can use mode `--package` options.
--output <filename>             file in which the spec is generated.
--description <input_filename>  file from which the description of API is taken - name, license, etc.
