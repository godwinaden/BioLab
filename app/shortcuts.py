from app import config

from cassandra.cqlengine.query import DoesNotExist, MultipleObjectsReturned

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from starlette.exceptions import HTTPException as StarletteHTTPException

settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def is_json(request: Request):
    return request.headers.get("content") == "true"


def get_object_or_404(KlassName, **kwargs):
    obj = None
    try:
        obj = KlassName.objects.get(**kwargs)
    except DoesNotExist as exc:
        raise StarletteHTTPException(status_code=404, detail=repr(exc))
    except MultipleObjectsReturned as exc:
        raise StarletteHTTPException(status_code=400, detail=repr(exc))
    except Exception as exc:
        raise StarletteHTTPException(status_code=500, detail=repr(exc))
    return obj


def redirect(path, cookies: dict = {}, remove_session=False):
    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key=k, value=v, httponly=True)
    if remove_session:
        response.set_cookie(key="session_ended", value=1, httponly=True)
        response.delete_cookie("session_id")
    return response


def render(
    request, template_name, context={}, status_code: int = 200, cookies: dict = {}
):
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    response.set_cookie(key="darkmode", value=1)
    if len(cookies.keys()) > 0:
        # set httponly cookies
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    # delete coookies
    # for key in request.cookies.keys():
    #     response.delete_cookie(key)
    return response
