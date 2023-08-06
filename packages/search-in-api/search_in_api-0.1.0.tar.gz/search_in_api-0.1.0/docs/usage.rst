=====
Usage
=====

To run **Search in API** with graphical user interface::

    $ python search_in_api.py

To run **Search in API** in a command line with dialog inputs::

    $ python search_in_api.py --command-line

To run **Search in API** in a bash script::

    python search_in_api.py --url="<url of the first page of api endpoint>" \
    --tag="<tag to search for>" --value="<value to search for>"

To use **Search in API** in a project::

    from search_in_api.search_in_api import search_for_string
    api_page_urls = search_for_string(
        url="<url of the first page of api endpoint>",
        tag="<tag to search for>",
        value="<value to search for>",
    )


