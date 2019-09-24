from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import re
import os


class KeywordQueryEventListener(EventListener):
    def have_vboxapi_and_virtualbox(self):
        import pkgutil
        return pkgutil.find_loader('virtualbox') and pkgutil.find_loader('vboxapi')

    def get_machine_info_cli(self):
        # Will allow us to capture separately the vm name and id
        regex = '^\"(.*)\" {(.*)}$'

        # Get list of all boxen and running boxen
        vms_raw = os.popen('vboxmanage list vms').read()
        running_vms_raw = os.popen('vboxmanage list runningvms').read()

        vms = vms_raw.strip('\n').split('\n')

        items = []
        for vm in vms:
            match = re.match(regex, vm)

            vm_name = match.group(1)
            vm_id = match.group(2)

            items.append({
                'id': vm_id,
                'name': vm_name,
                'description': 'State: running' if vm_id in running_vms_raw else 'State: stopped'
            })

        return items

    def get_machine_info_vboxapi(self):
        import virtualbox

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

        machines = self.get_machine_info_vboxapi() \
            if self.have_vboxapi_and_virtualbox() \
            else self.get_machine_info_cli()

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

        return RenderResultListAction(items)
