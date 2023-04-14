ADMIN_ORDERING = {
    "materials": [
        "Section",
        "SubSection",
        'Article'
    ],
}


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in app_dict.items():
        if app_name in ADMIN_ORDERING:
            app = app_dict[app_name]
            app["models"].sort(
                key=lambda x: ADMIN_ORDERING[app_name].index(x["object_name"])
            )
            app_dict[app_name]
            yield app
        else:
            yield app_dict[app_name]


