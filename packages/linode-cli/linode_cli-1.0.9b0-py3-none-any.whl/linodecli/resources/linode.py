import argparse
import getpass
import json
import sys
from datetime import datetime, timedelta
from time import sleep

import linode
from colorclass import Color
from terminaltables import SingleTable

from linodecli.config import update_namespace


def _colorize_status(status):
    if status in ('running'):
        return Color('{green}'+status+'{/green}')
    if status in ('booting','shutting_down','rebooting'):
        return Color('{yellow}'+status+'{/yellow}')
    return Color('{red}'+status+'{/red}')

def _colorize_yesno(yesno):
    if yesno == 'yes' or yesno == True:
        return Color('{green}yes{/green}')
    return Color('{red}no{/red}')

def _colorize_type(backup_type):
    if backup_type == 'auto':
        return Color('{yellow}auto{/yellow}')
    return Color('{green}'+backup_type+'{/green}')

def _make_linode_row(linode):
    return [
        linode.label,
        _colorize_status(linode.status),
        linode.region.id,
        _colorize_yesno(linode.backups.enabled),
        linode.specs.disk,
        linode.specs.memory,
    ]

def _make_raw_linode_row(group, linode):
    return  [
        group,
        linode.label,
        linode.status,
        linode.region.id,
        str(linode.backups.enabled),
        str(linode.specs.disk),
        str(linode.specs.memory)
    ]

def _get_linode_or_die(client, label):
        try:
            return client.linode.get_instances(linode.Linode.label == label).only()
        except:
            print("No linode found with label {}".format(label))
            sys.exit(1)

def _wait_for_state(minutes, linodes, expected_state):
    if not isinstance(linodes, list):
        linodes = [linodes]
    end_wait = datetime.now() + timedelta(minutes=minutes)
    sys.stdout.write('Waiting')
    linodes = linodes
    while datetime.now() < end_wait and any(linodes):
        linodes = [ l for l in linodes if not l.status == expected_state ]
        sys.stdout.write('.')
        sys.stdout.flush()
        sleep(2)
    print()

class Linode:
    def list(args, client, unparsed=None):
        linodes = client.linode.get_instances()
        groups = {}
        for l in linodes:
            if not l.group in groups:
                groups[l.group] = []
            groups[l.group].append(l)

        header = [ "label", "status", "location", "backups", "disk", "memory" ]

        for k in sorted(groups.keys()):
            if args.raw:
                for l in groups[k]:
                    print(args.separator.join(_make_raw_linode_row(k,l)))
            else:
                print(k if k else 'Linode')
                data = [ _make_linode_row(l) for l in groups[k] ]
                data = [ header ] + data
                tab = SingleTable(data)
                print(tab.table)

    def create(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="CLI Linode Manipulation")
        parser.add_argument('-l', '--label', metavar='LABEL', type=str,
                help="the label for the Linode")
        parser.add_argument('-L', '--location', metavar='LOCATION', type=str,
                help="the location for deployment.")
        parser.add_argument('-i', '--image', metavar='IMAGE', type=str,
                help="the Image to deploy")
        parser.add_argument('-p', '--plan', metavar='PLAN', type=str,
                help="the plan to deploy.")
        parser.add_argument('-P', '--password', metavar='PASSWORD', type=str,
                help="the root password for the new deployment")
        parser.add_argument('-g', '--group', metavar='GROUP', type=str,
                help="the group to deploy the new Linode to")
        parser.add_argument('-K', '--pubkey-file', metavar='KEYFILE', type=str, default=argparse.SUPPRESS,
                help="the public key file to install at `/root/.ssh/authorized_keys` when creating this Linode")
        parser.add_argument('-S', '--stackscript', metavar='STACKSCRIPT_ID', type=int,
                help="the personal or public StackScript ID to use for deployment")
        parser.add_argument('-J', '--stackscriptjson', metavar='STACKSCRIPT_JSON', type=str, default=None,
                help="The JSON encoded name/value pairs, answering the StackScript's User Defined Fields (UDFs).")
        parser.add_argument('-b', '--with-backups', action='store_true',
                help="If true, enable backups on the new Linode")
        parser.add_argument('-B', '--restore-backup', metavar='BACKUP_ID', type=int,
                help="The Backup to restore to the new Linode.")
        parser.add_argument('-w', '--wait', metavar='TIME', type=int, nargs='?', const=5,
            help="The amount of minutes to wait for boot.  If given with no argument, defaults to 5")

        args = parser.parse_args(args=unparsed, namespace=args)

        stackscript_data=None
        if args.stackscriptjson:
            try:
                stackscript_data = json.loads(args.stackscriptjson)
            except:
                print("Invalid JSON for stackscript data!")
                sys.exit(2)

        password = args.password
        if not password:
            password = getpass.getpass("Root Password: ")

        params = {
            "image": args.image,
            "group": args.group,
            "stackscript": args.stackscript,
            "root_pass": password,
            "label": args.label,
            "stackscript": args.stackscript,
            "stackscript_data": stackscript_data,
            "backup": args.restore_backup,
            "with_backups": args.with_backups,
        }

        if args.pubkey_file:
            params['authorized_keys'] = args.pubkey_file

        l = client.linode.create_instance(args.plan, args.location, **params)

        if args.wait:
            _wait_for_state(args.wait, l, 'running')

    def start(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Boot a Linode")
        parser.add_argument('label', metavar='LABEL', type=str, nargs='+',
            help="The Linode to boot")
        parser.add_argument('-w', '--wait', metavar='TIME', type=int, nargs='?', const=5,
            help="The amount of minutes to wait for boot.  If given with no argument, defaults to 5")

        args = parser.parse_args(args=unparsed, namespace=args)

        linodes = []
        for label in args.label:
            linodes.append(_get_linode_or_die(client, label))

        for l in linodes:
            l.boot()

        if args.wait:
            _wait_for_state(args.wait, linodes, 'running')

    def stop(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Power down a Linode")
        parser.add_argument('label', metavar='LABEL', type=str, nargs='+',
            help="The Linode to power down.")
        parser.add_argument('-w', '--wait', metavar='TIME', type=int, nargs='?', const=5,
            help="The amount of minutes to wait for shutdown.  If given with no argument, defaults to 5")

        args = parser.parse_args(args=unparsed, namespace=args)

        linodes = []
        for label in args.label:
            linodes.append(_get_linode_or_die(client, label))

        for l in linodes:
            l.shutdown()

        if args.wait:
            _wait_for_state(args.wait, linodes, 'offline')

    def restart(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Restart a Linode")
        parser.add_argument('label', metavar='LABEL', type=str, nargs='+',
                help="The Linode to restart")
        parser.add_argument('-w', '--wait', metavar='TIME', type=int, nargs='?', const=5,
                help="The amount of minutes to wait for restart.  If given with no argument, defaults to 5")

        args = parser.parse_args(args=unparsed, namespace=args)

        linodes = []
        for label in args.label:
            linodes.append(_get_linode_or_die(client, label))

        for l in linodes:
            l.reboot()

        if args.wait:
            _wait_for_state(args.wait, linodes, 'running')

    def show(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Shows information about a Linode")
        parser.add_argument('label', metavar='LABEL', type=str, nargs='+',
                help="The Linode to show")

        args = parser.parse_args(args=unparsed, namespace=args)

        linodes = []
        for label in args.label:
            linodes.append(_get_linode_or_die(client, label))

        for l in linodes:
            if args.raw:
                form = args.separator.join([ '{}' for i in range(0,7) ])
            else:
                form = """   label: {}
  status: {}
location: {}
 backups: {}
    disk: {}
  memory: {}
     ips: {}"""


            print(form.format(l.label, l.status, l.region.id, 'yes' if l.backups.enabled else 'no',
                l.specs.disk, l.specs.memory, ', '.join(l.ipv4)))

            if not args.raw and len(linodes) > 1 and not l == linodes[-1]:
                print()

    def delete(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Delete a Linode")
        parser.add_argument('label', metavar='LABEL', type=str, nargs='+',
                help="The Linode to Delete")

        args = parser.parse_args(args=unparsed, namespace=args)

        linodes = []
        for label in args.label:
            linodes.append(_get_linode_or_die(client, label))

        for l in linodes:
            l.delete()

    def rename(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Change a Linode's label")
        parser.add_argument('label', metavar='LABEL', type=str,
                help="The Linode whose label is to be changed")
        parser.add_argument('new_label', metavar='NEW_LABEL', type=str,
                help="The new label for this Linode")

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)
        l.label = args.new_label
        l.save()

    def group(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Set a Linode's display group.")
        parser.add_argument('label', metavar='LABEL', type=str, nargs='+',
                help="The Linode whose group is to be changed")
        parser.add_argument('new_group', metavar='GROUP', type=str,
                help="The new group for the Linode")

        args = parser.parse_args(args=unparsed, namespace=args)

        linodes = []
        for label in args.label:
            linodes.append(_get_linode_or_die(client, label))

        for l in linodes:
            l.group = args.new_group
            l.save()

    def rebuild(args, client, unparsed=None):
        parser = argparse.ArgumentParser('Rebuild an existing Linode.')
        parser.add_argument('label', metavar='LABEL', type=str,
                help="the Linode to rebuild")
        parser.add_argument('-i', '--image', metavar='IMAGE', type=str,
                help="the Image to deploy")
        parser.add_argument('-P', '--password', metavar='PASSWORD', type=str,
                help="the root password for the new deployment")
        parser.add_argument('-K', '--pubkey-file', metavar='KEYFILE', type=str, default=argparse.SUPPRESS,
                help="the public key file to install at `/root/.ssh/authorized_keys` when creating this Linode")
        parser.add_argument('-S', '--stackscript', metavar='STACKSCRIPT_ID', type=int,
                help="the personal or public StackScript ID to use for deployment")
        parser.add_argument('-J', '--stackscriptjson', metavar='STACKSCRIPT_JSON', type=str, default=None,
                help="The JSON encoded name/value pairs, answering the StackScript's User Defined Fields (UDFs).")
        parser.add_argument('-w', '--wait', metavar='TIME', type=int, nargs='?', const=5,
            help="The amount of minutes to wait for boot.  If given with no argument, defaults to 5")

        args = parser.parse_args(args=unparsed, namespace=args)

        stackscript_data=None
        if args.stackscriptjson:
            try:
                stackscript_data = json.loads(args.stackscriptjson)
            except:
                print("Invalid JSON for stackscript data!")
                sys.exit(2)

        password = args.password
        if not password:
            password = getpass.getpass("Root Password: ")

        l = _get_linode_or_die(client, args.label)

        l.rebuild(args.image, root_pass=password, authorized_keys=args.pubkey_file,
                stackscript=args.stackscript, stackscript_data=stackscript_data)

        if args.wait:
            _wait_for_state(args.wait, l, 'running')

    def resize(args, client, unparsed=None):
        print("This feature is not yet available in the alpha api.  You can stay "
                "up to date with alpha updates at https://engineering.linode.com")
        sys.exit(0)

    def ip_add(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Add an IP address to a Linode.")
        parser.add_argument('label', metavar='LABEL', type=str,
                help='The Linode to add an IP to')
        parser.add_argument('--private', action='store_true',
                help='Add a private IP address instead of a public one')

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)
        ip = l.allocate_ip(public=not args.private)

        print("Added {}".format(ip['address']))

    def locations(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="List all available locations.")

        # make sure they didn't send up junk
        args = parser.parse_args(args=unparsed, namespace=args)

        regions = client.get_regions()

        if args.raw:
            print(args.separator.join([ r.id for r in regions ]))
        else:
            for r in regions:
                print("{} {}".format(r.id, Color('{green}(Default){/green}') if r.id == args.location else ''))

    def images(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="List all available Images.")

        # make sure they didn't send up junk
        args = parser.parse_args(args=unparsed, namespace=args)

        images = client.get_images(linode.Image.is_public==True)

        if args.raw:
            print(args.separator.join([ i.label for i in images ]))
        else:
            for i in images:
                print("{} {}".format(i.label,
                    Color('{green}(Default){/green}') if i.id == args.image else ''))

    def plans(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="List all available Linode types.")

        # make sure they didn't send up junk
        args = parser.parse_args(args=unparsed, namespace=args)

        types = client.linode.get_types()

        if args.raw:
            print(args.separator.join([ t.id for t in types ]))
        else:
            for t in types:
                print("{} {}".format(t.id, Color('{green}(Default){/green}') if t.id == args.plan else ''))


    def backups_show(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Show information about a Linode's backups.")
        parser.add_argument('label', metavar='LABEL', type=str,
                help="The Linode whose backups we are viewing.")

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)
        if not l.backups.enabled:
            print("Backups are not enabled for {}".format(l.label))
            sys.exit(0)

        data = [ [ "id", "status", "label", "date" ] ]

        b = l.available_backups

        if b.snapshot.in_progress:
            b.snapshot.in_progress._set('type', "in progress")

        for cur in b.automatic + [ b.snapshot.current ] + [ b.snapshot.in_progress ]:
            if not cur:
                continue # we might not have all of these
            data.append([ cur.id, _colorize_type(cur.type),
                "" if cur.type == 'auto' else cur.label , cur.create_dt if hasattr(cur, 'create_dt') else cur.created ])

        tab = SingleTable(data)
        print(tab.table)

    def snapshot(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Take a snapshot of a Linode.")
        parser.add_argument('label', metavar='LABEL', type=str,
                help="The Linode we are taking a snapshot of.")
        parser.add_argument('-l', '--snapshot-label', metavar='SNAPLABEL', type=str,
                help="The label for the Snapshot we're taking")

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)
        if not l.backups.enabled:
            print("Backups are not enabled for {}".format(l.label))
            sys.exit(0)

        s = l.snapshot(label=args.snapshot_label)

        print("Snapshot {} in progress for {}".format(s.id, l.label))

    def backups_restore(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Restores a Backup to a Linode.")
        parser.add_argument('label', metavar='LABEL', type=str,
                help="The Linode whose Backup we are restoring.")
        parser.add_argument('backup', metavar='BACKUPID', type=int,
                help="The Backup to restore.")
        parser.add_argument('-l', '--restore-to-linode', metavar='RESTORE_TO_LINODE', type=str,
                help="The Linode we are restoring the Backup to.  "
                        "If omitted, restores to the linode the Backup was taken of.")
        parser.add_argument('-f', '--force', action='store_true',
                help="Overwrites all existing disks and configs on the target Linode.")

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)
        if not l.backups.enabled:
            print("Backups are not enabled for {}".format(l.label))
            sys.exit(0)

        b = linode.Backup(client, args.backup, l.id)

        # ensure this backup exists
        try:
            b.label
        except linode.ApiError:
            print("Not backup {} found for linode {}".format(args.backup, l.label))
            sys.exit(0)

        target = l
        if args.restore_to_linode:
            target = _get_linode_or_die(client, args.restore_to_linode)

        b.restore_to(target, overwrite=args.force)

        print("Restore in progress.")

    def backups_enable(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Enable Backups on a Linode.")
        parser.add_argument('label', metavar='LABEL', type=str,
                help="The Linode we are enabling Backups on.")

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)

        if l.backups.enabled:
            print("Backups already enabled on {}".format(l.label))
            sys.exit(0)

        l.enable_backups()

    def backups_cancel(args, client, unparsed=None):
        parser = argparse.ArgumentParser(description="Cancel Backups on a Linode.")
        parser.add_argument('label', metavar='LABEL', type=str,
                help="The Linode we are cancelling Backups on.")

        args = parser.parse_args(args=unparsed, namespace=args)

        l = _get_linode_or_die(client, args.label)

        if not l.backups.enabled:
            print("Backups are not enabled on {}".format(l.label))
            sys.exit(0)

        l.cancel_backups()
