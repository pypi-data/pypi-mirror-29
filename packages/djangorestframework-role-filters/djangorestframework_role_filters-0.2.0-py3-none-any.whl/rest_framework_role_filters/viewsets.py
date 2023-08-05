from rest_framework.viewsets import ModelViewSet


class RoleFilterModelViewSet(ModelViewSet):
    role_filter_group = None

    def get_role_id(self, request):
        pass

    def initial(self, request, *args, **kwargs):
        super(RoleFilterModelViewSet, self).initial(request, *args, **kwargs)
        self.role_id = self.get_role_id(request)
        allowed_actions = self.role_filter_group.get_allowed_actions(self.role_id, request, self)
        if self.action not in allowed_actions:
            self.permission_denied(
                request,
                message='action={} not allowed for role={}'.format(self.action, self.role_id)
            )

    def get_queryset(self):
        queryset = super(RoleFilterModelViewSet, self).get_queryset()
        return self.role_filter_group.get_queryset(self.role_id, self.request, self, queryset) or queryset

    def get_serializer_class(self):
        serializer_class = super(RoleFilterModelViewSet, self).get_serializer_class()
        return self.role_filter_group.get_serializer_class(self.role_id, self.request, self) or serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return self.role_filter_group.get_serializer(self.role_id, self.request, self, serializer_class, *args, **kwargs) or serializer_class(*args, **kwargs)
