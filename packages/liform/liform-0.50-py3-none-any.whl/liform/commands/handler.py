class HandlerCommand(object):
    def __init__(self, resources, phases, settings, variables, handler_name, final_state):
        from collections import defaultdict
        from datetime import datetime

        self.__resources = resources
        self.__phases = phases
        self.__settings = settings
        self.__variables = variables
        self.__handler_name = handler_name
        self.__final_state = final_state
        self.__command_time_from = datetime.utcnow()
        self.__phase_stats = defaultdict(int)
        self.__type_stats = defaultdict(int)
        self.__step_stats = defaultdict(int)

    def __mark_dirty(self, resource):
        resource.is_dirty = (not resource.state) and (resource._opted_in)
        resource._time_from = self.__command_time_from

        for child in resource.children:
            self.__mark_dirty(child)

    def __fore_phase(self, resource, phase):
        handler = getattr(resource.handler, self.__handler_name)

        if handler:
            handler.fore_phase(phase, self.__settings, self.__variables)

        for child in resource.children:
            self.__fore_phase(child, phase)

    def __execute_fore(self, resource, phase):
        from datetime import datetime

        if resource.phase.path == phase.path:
            handler = getattr(resource.handler, self.__handler_name)

            if handler:
                if not handler.try_sync(phase, self.__settings, self.__variables) and not resource.is_dirty:
                    resource.is_dirty = True

                handler.fore_children(phase, self.__settings, self.__variables)

    def __execute_deep(self, resource, phase):
        for child in resource.children:
            self.__execute(child, phase)

    def __execute_past(self, resource, phase):
        from datetime import datetime

        if resource.phase.path == phase.path:
            handler = getattr(resource.handler, self.__handler_name)

            if handler:
                handler.post_children(phase, self.__settings, self.__variables)

                if resource.is_dirty:
                    resource.state = self.__final_state

    def __execute(self, resource, phase):
        from datetime import datetime

        if resource.phase.path == phase.path:
            handler = getattr(resource.handler, self.__handler_name)

            if handler:
                if not handler.try_sync(phase, self.__settings, self.__variables) and not resource.is_dirty:
                    resource.is_dirty = True

                handler.fore_children(phase, self.__settings, self.__variables)

        for child in resource.children:
            self.__execute(child, phase)

        if resource.phase.path == phase.path:
            handler = getattr(resource.handler, self.__handler_name)

            if handler:
                handler.post_children(phase, self.__settings, self.__variables)

                if resource.is_dirty:
                    resource.state = self.__final_state

    def __post_phase(self, resource, phase):
        for child in resource.children:
            self.__post_phase(child, phase)

        handler = getattr(resource.handler, self.__handler_name)

        if handler:
            handler.post_phase(phase, self.__settings, self.__variables)

    def __run(self, phase):
        from datetime import datetime
        from threading import Thread

        if phase.reference_count > 0:
            time_from = datetime.utcnow()

            print(
                '{0:%H:%M} \033[36;1m>\033[0m {1:>+4}: \033[36;1m{2}\033[0m {3}'.format(
                    time_from,
                    int((time_from - self.__command_time_from).total_seconds()),
                    '||' if phase.is_parallel else '==',
                    phase.path))

            for resource in self.__resources:
                self.__fore_phase(resource, phase)

            if phase.is_parallel:
                fore_threads = [
                    Thread(
                        target=self.__execute_fore,
                        args=(resource, phase,)) for resource in self.__resources]

                for thread in fore_threads:
                    thread.start()

                for thread in fore_threads:
                    thread.join()

                deep_threads = [
                    Thread(
                        target=self.__execute_deep,
                        args=(resource, phase,)) for resource in self.__resources]

                for thread in deep_threads:
                    thread.start()

                for thread in deep_threads:
                    thread.join()

                post_threads = [
                    Thread(
                        target=self.__execute_past,
                        args=(resource, phase,)) for resource in self.__resources]

                for thread in post_threads:
                    thread.start()

                for thread in post_threads:
                    thread.join()
            else:
                for resource in self.__resources:
                    self.__execute(resource, phase)

            for child_phase in phase.children:
                self.__run(child_phase)

            for resource in self.__resources:
                self.__post_phase(resource, phase)

            time_till = datetime.utcnow()
            self.__phase_stats[phase.path] += (time_till - time_from).total_seconds()
            print(
                '{0:%H:%M} \033[36;1m<\033[0m {1:>+4}: \033[36;1m{2}\033[0m {3} ({4})'.format(
                    time_till,
                    int((time_till - self.__command_time_from).total_seconds()),
                    '||' if phase.is_parallel else '==',
                    phase.path,
                    int((time_till - time_from).total_seconds())))

    def run(self):
        for resource in self.__resources:
            self.__mark_dirty(resource)

        for phase in self.__phases:
            self.__run(phase)


class RefreshCommand(HandlerCommand):
    def __init__(self, resources, phases, settings, variables):
        super().__init__(resources, phases, settings, variables, 'refresh', 1)


class DestroyCommand(HandlerCommand):
    def __init__(self, resources, phases, settings, variables):
        super().__init__(resources, phases, settings, variables, 'destroy', 0)
