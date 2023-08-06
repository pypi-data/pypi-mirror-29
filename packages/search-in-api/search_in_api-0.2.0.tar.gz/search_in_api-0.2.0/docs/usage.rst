=====
Usage
=====

To run **Search in API** with graphical user interface::

    $ python -m "search_in_api.search_in_api"

To run **Search in API** in a command line with dialog inputs::

    $ python -m "search_in_api.search_in_api" --command-line

To run **Search in API** in a bash script::

    python -m "search_in_api.search_in_api" --url="<url of the first page of api endpoint>" \
    --tag="<tag to search for>" --value="<value to search for>"

To use **Search in API** in a Python project::

    from search_in_api.search_in_api import search_for_string
    api_page_urls = search_for_string(
        url="<url of the first page of api endpoint>",
        tag="<tag to search for>",
        value="<value to search for>",
    )


