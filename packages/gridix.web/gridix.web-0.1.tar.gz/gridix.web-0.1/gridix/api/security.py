from webargs.pyramidparser import use_args
from pyramid.security import Allow, Everyone, Authenticated



class ACLResource(object):
    __acl__ = [
        (Allow, 'api:admin', 'api'),
    ]

    def __init__(self, request):
        self.request = request


def api_role_finder(userid, request):
    roles = request.jwt_claims.get('roles', [])
    return roles


def use_args_with(schema_cls, schema_kwargs=None, **kwargs):
    schema_kwargs = schema_kwargs or {}
    def factory(request):
        only = request.matchdict.get('fields', None)
        partial = request.method == 'PATCH'
        return schema_cls(
            only=only, partial=partial, strict=True,
            context={'request': request}, **schema_kwargs
        )
    return use_args(factory, **kwargs)
