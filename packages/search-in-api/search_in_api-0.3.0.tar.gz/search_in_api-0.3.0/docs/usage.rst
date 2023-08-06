=====
Usage
=====

To run **Search in API** with graphical user interface::

    $ search_in_api

To run **Search in API** in a command line with dialog inputs::

    $ search_in_api --command-line
    Enter API URL for the first page: https://example.com/api/songs.xml
    Enter tag to search for: title
    Enter value to search for: Journey
    Searching...
    API pages with the search result:
    https://example.com/api/songs.xml?page=7
    https://example.com/api/songs.xml?page=12
    Finished.

To run **Search in API** in a bash script::

    $ search_in_api --url="https://example.com/api/songs.xml" \
    --tag="title" --value="Journey"
    https://example.com/api/songs.xml?page=7
    https://example.com/api/songs.xml?page=12

To use **Search in API** in a Python project::

    from search_in_api.search_in_api import search_for_string
    api_page_urls = search_for_string(
        url="https://example.com/api/songs.xml",
        tag="title",
        value="Journey",
    )
    assert api_page_urls == ["https://example.com/api/songs.xml?page=7", "https://example.com/api/songs.xml?page=12"]
