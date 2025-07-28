from fastapi import Request


class HTMXComponentSelector:
    """ An implementation of the fasthtmx component selector protocol that detects if the request came from htmx and returns a partial or full page.

    usage:
    @jinja.page("pages/add.html", "partials/add_form.html")
    def add_form():
    ...

    This renders either the partial or the whole page depending on whether the request came from browser or the htmx library.
    Use this to implement progressive enhancement based patterns.
    If your user goes to carpool_magic.com/carpools/182812918, the carpool app would render them a full page.
    If they go to carpools.com, click my carpools, and then click the carpools name, htmx can be configured to ask for
    carpool_magic.com/carpools/182812918,
    and it sends an hx-request header that tells the server the request only needs a partial. This class detects that and returns only the needed fragment of html.
    The responded fragment will render directly.
    """

    def __init__(self, page: str, partial: str):
        self.page = page
        self.partial = partial

    def get_component(self, request: Request, _error: Exception | None) -> str:
        """ Gets the component needed, based on if the hx-request header is present. """
        return self.partial if request.headers.get("hx-request") == "true" else self.page
