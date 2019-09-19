from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import virtualbox
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        vbox = virtualbox.VirtualBox()
        items = []

        for machine in vbox.machines:
            name = machine.name + '[' + str(machine.state) + ']'
            description = 'OS: ' + machine.os_type_id \
                          + '; CPUs: ' + str(machine.cpu_count) \
                          + '; RAM: ' + str(machine.memory_size) + 'MB'

            # There doesn't seem to be any way at the moment to run custom python code as an action
            # Also, virtualbox does not yet support wayland, so make sure it starts as X
            # Even more also, can't use f strings cause I can't assure py 3.6 is available
            command = 'QT_QPA_PLATFORM=xcb /usr/lib/virtualbox/VirtualBoxVM --startvm "' + machine.id_p + '"'

            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=name,
                description=description,
                on_enter=RunScriptAction(command)
            ))

        return RenderResultListAction(items)
