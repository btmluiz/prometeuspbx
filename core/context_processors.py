class PermLookupDict:
    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return str(self.user.get_all_permissions())

    def __getitem__(self, perm_name):
        return self.user.has_perm(perm_name)

    def __iter__(self):
        # To fix 'item in perms.someapp' and __getitem__ interaction we need to
        # define __iter__. See #18979 for details.
        raise TypeError("PermLookupDict is not iterable.")


class PermWrapper:
    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.user!r})"

    def __getitem__(self, perm):
        return PermLookupDict(self.user)[perm]

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("PermWrapper is not iterable.")

    def __contains__(self, perm_name):
        """
        Lookup by "someapp" or "someapp.someperm" in perms.
        """
        # if "." not in perm_name:
        #     # The name refers to module.
        #     return bool(self[perm_name])
        return PermLookupDict(self.user)[perm_name]

    def __str__(self):
        return str(PermLookupDict(self.user))


def auth(request):
    """
    Return context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, use AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, "user"):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser

        user = AnonymousUser()

    return {
        "user": user,
        "perms": PermWrapper(user),
    }
