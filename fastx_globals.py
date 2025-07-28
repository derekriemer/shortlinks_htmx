
import jinja2
from fasthx import Jinja
from fastapi.templating import Jinja2Templates
import jinja_partials


jinja = None


def get_or_init_fastx():
    """ Get the fastx object used to decorate jinja template routes.
    if not initialized yet, initialize jinja, jinja_partials, and fastx before returning it.
    This factory function song and dance is here to prevent double initialization of fastx, because I'm not sure if that's something that would cause problems, and having two different places where fastx is initialized makes things annoying.
    """
    # pylint:disable=W0603
    global jinja
    if not jinja:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates"),
            extensions=[
                "jinja2.ext.debug",
            ]
        )
        templates = Jinja2Templates(env=env)
        jinja_partials.register_starlette_extensions(templates)
        jinja = Jinja(templates)
    return jinja
