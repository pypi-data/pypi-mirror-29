class ResolvedResource(object):
    def __init__(self, module, type, name, phase, properties, children, dependencies, source_file, source_line):
        self.module = module
        self.type = type
        self.name = name
        self.phase = phase
        self.properties = properties
        self.parent = None
        self.children = children
        self.dependencies = dependencies
        self.source_file = source_file
        self.source_line = source_line
        self.handler = None
        self.id = None
        self.ipv4 = None
        self.ipv6 = None
        self.state = 0

    def __repr__(self):
        return '{0}:{1}'.format(self.type, self.name)

    def get_ancestor(self, type_pattern):
        from re import compile as re_compile

        pattern = re_compile(type_pattern)
        parent = self

        while parent and not pattern.search(parent.type):
            parent = parent.parent

        return parent

    @property
    def state_text(self):
        return 'Valid' if self.state else 'Error'


class ProjectProcessor(object):
    def __init__(self, handlers, variables):
        self.__handlers = handlers
        self.__variables = variables
        self.resources = []

    def __flatten_resource(self, parsed_resource):
        from collections import OrderedDict
        from ..utility import error_print
        from ..utility import warning_print

        type = parsed_resource.type
        phase = parsed_resource.phase
        properties = OrderedDict()
        dependencies = set()
        children = []

        for base in parsed_resource.bases:
            base_template = self.__flatten_resource(base)

            if base_template.type is not None:
                if type is not None:
                    warning_print(
                        '{0}:{1}: "{2}"''s type is overriden.',
                        parsed_resource.source_file,
                        parsed_resource.source_line,
                        parsed_resource.name)
                type = base_template.type

                if phase is not None:
                    warning_print(
                        '{0}:{1}: "{2}"''s phase is overriden.',
                        parsed_resource.source_file,
                        parsed_resource.source_line,
                        parsed_resource.name)
                phase = base_template.phase

            properties.update(base_template.properties)
            dependencies.update(base_template.dependencies)

            for child in base_template.children:
                children.append(child)

        properties.update(parsed_resource.properties)
        dependencies.update(parsed_resource.dependencies)

        resolved_resource = ResolvedResource(
            parsed_resource.module,
            type,
            parsed_resource.name,
            phase,
            properties,
            children,
            dependencies,
            parsed_resource.source_file,
            parsed_resource.source_line)

        if parsed_resource.is_resource:
            parsed_resource.resolved_resource = resolved_resource

        for child in parsed_resource.children:
            children.append(self.__flatten_resource(child))

        return resolved_resource

    def __flatten_resources(self, parsed_resources):
        for name, parsed_resource in parsed_resources.items():
            resource = self.__flatten_resource(parsed_resource)

            self.resources.append(resource)

    def __resolve_resource(self, resolved_resource, resolved_parent):
        from collections import OrderedDict
        from jinja2 import FileSystemLoader
        from jinja2.sandbox import SandboxedEnvironment
        from os.path import dirname

        base_path = dirname(resolved_resource.source_file)
        loader = FileSystemLoader(base_path)
        environment = SandboxedEnvironment(
            trim_blocks=False,
            lstrip_blocks=False,
            keep_trailing_newline=True,
            autoescape=False,
            loader=loader)
        environment.globals.update(self.__variables)
        parent_properties = resolved_parent.properties if resolved_parent else {}
        this_properties = OrderedDict()

        for name, value in resolved_resource.properties.items():
            this_properties[name] = environment.from_string(value).render({
                'this': this_properties,
                'parent': parent_properties})

        resolved_resource.properties = this_properties
        resolved_resource.parent = resolved_parent

        if resolved_parent:
            resolved_resource.path = '{0}/{1}:{2}:{3}'.format(
                resolved_parent.path,
                resolved_resource.module,
                resolved_resource.type,
                resolved_resource.name)
            resolved_resource.slug = '{0}/{1}'.format(
                resolved_parent.slug,
                resolved_resource.name)
        else:
            resolved_resource.path = '{0}:{1}:{2}'.format(
                resolved_resource.module,
                resolved_resource.type,
                resolved_resource.name)
            resolved_resource.slug = resolved_resource.name

        for child in resolved_resource.children:
            self.__resolve_resource(child, resolved_resource)

    def __resolve_resources(self):
        for resource in self.resources:
            self.__resolve_resource(resource, None)

    def __resolve_dependency(self, resolved_resource):
        from collections import defaultdict
        from queue import Queue

        dependency_queue = Queue()
        dependency_map = defaultdict(set)

        for dependency in resolved_resource.dependencies:
            dependency_queue.put((dependency.name, dependency))

        while not dependency_queue.empty():
            name, dependency = dependency_queue.get_nowait()

            if dependency.resolved_resource:
                dependency_map[name].add(dependency.resolved_resource)
            else:
                for derivative in dependency.derivatives:
                    dependency_queue.put((name, derivative))

        resolved_resource.dependencies = dependency_map

        for child in resolved_resource.children:
            self.__resolve_dependency(child)

    def __resolve_dependencies(self):
        for resource in self.resources:
            self.__resolve_dependency(resource)

    def __validate_resource(self, resource):
        from ..utility import error_print

        if resource.type is None:
            error_print(
                '{0}:{1} "{2}" does not inherit any typed resource.',
                resource.source_file,
                resource.source_line,
                resource.name)
        else:
            resource.handler = self.__handlers[resource.type](resource)

        resource.handler.validate()

        for child in resource.children:
            self.__validate_resource(child)

    def __validate_resources(self):
        for resource in self.resources:
            self.__validate_resource(resource)

    def __sort_resource(self, resource):
        resource.children = sorted(resource.children, key=lambda child: child.phase.priority)

        for child in resource.children:
            self.__sort_resource(child)

    def __sort_resources(self):
        for resource in self.resources:
            self.__sort_resource(resource)

    def resolve_resources(self, parsed_resources):
        self.__flatten_resources(parsed_resources)
        self.__resolve_resources()
        self.__resolve_dependencies()
        self.__validate_resources()
        self.__sort_resources()

    def __select_state(self, state_database, resource):
        state = state_database.get(resource.path)

        resource.id = state.id
        resource.code = state.code
        resource.ipv4 = state.ipv4
        resource.ipv6 = state.ipv6
        resource.state = state.state

        for child in resource.children:
            self.__select_state(state_database, child)

    def select_state(self, state_database):
        for resource in self.resources:
            self.__select_state(state_database, resource)

    def __update_state(self, state_database, resource):
        state_database.set(
            resource.path,
            resource.type,
            resource.name,
            resource.id,
            resource.name,
            resource.ipv4,
            resource.ipv6,
            resource.state)

        for child in resource.children:
            self.__update_state(state_database, child)

    def update_state(self, state_database):
        for resource in self.resources:
            self.__update_state(state_database, resource)
