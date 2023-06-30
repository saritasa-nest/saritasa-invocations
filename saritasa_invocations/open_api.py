import invoke

from . import django, printing, system


@invoke.task
def validate_swagger(context: invoke.Context) -> None:
    """Check that generated open_api spec is valid.

    It creates spec file in ./tmp folder and then validates it.

    """
    printing.print_success("Validating OpenAPI spec")
    system.create_tmp_folder(context)
    django.manage(
        context,
        "spectacular --file .tmp/schema.yaml --validate --fail-on-warn",
    )
