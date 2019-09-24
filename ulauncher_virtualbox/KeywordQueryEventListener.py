from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import virtualbox
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


class KeywordQueryEventListener(EventListener):
    def get_machine_info_cli(self):
        pass

    def get_machine_info_vboxapi(self):
        vbox = virtualbox.VirtualBox()
        items = []

        for machine in vbox.machines:
            description = \
                'State: ' + str(machine.state) \
                + '; OS: ' + machine.os_type_id \
                + '; CPUs: ' + str(machine.cpu_count) \
                + '; RAM: ' + str(machine.memory_size) + 'MB'
            items.append({
                'id': machine.id_p,
                'name': machine.name,
                'description': description,
            })

        return items


    def on_event(self, event, extension):
        vbox_exec = extension.preferences.get('vbox_exec')

        machines = self.get_machine_info_vboxapi()
        items = []
        for machine in machines:
            # There doesn't seem to be any way at the moment to run custom python code as an action
            # Also, virtualbox does not yet support wayland, so make sure it starts as X
            # Even more also, can't use f strings cause I can't assure py 3.6 is available
            command = 'QT_QPA_PLATFORM=xcb ' + vbox_exec + ' --startvm "' + machine['id'] + '"'

            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=machine['name'],
                description=machine['description'],
                on_enter=RunScriptAction(command)
            ))

        #
        #
        # vbox = virtualbox.VirtualBox()
        # items = []
        #
        # vbox_exec = extension.preferences.get('vbox_exec')
        #
        # for machine in vbox.machines:
        #     description = \
        #         'State: ' + str(machine.state) \
        #         + '; OS: ' + machine.os_type_id \
        #         + '; CPUs: ' + str(machine.cpu_count) \
        #         + '; RAM: ' + str(machine.memory_size) + 'MB'
        #
        #     # There doesn't seem to be any way at the moment to run custom python code as an action
        #     # Also, virtualbox does not yet support wayland, so make sure it starts as X
        #     # Even more also, can't use f strings cause I can't assure py 3.6 is available
        #     command = 'QT_QPA_PLATFORM=xcb ' + vbox_exec + ' --startvm "' + machine.id_p + '"'
        #
        #     items.append(ExtensionResultItem(
        #         icon='images/icon.png',
        #         name=machine.name,
        #         description=description,
        #         on_enter=RunScriptAction(command)
        #     ))

        return RenderResultListAction(items)
