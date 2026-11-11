"""List research questions and inspect plans; never pretend pending analysis ran."""
import argparse
import json
from dataclasses import asdict
from pathlib import Path
from gidh_delhi_air.investigations.registry import list_investigations, plan_investigation


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Delhi Air investigations')
    commands = parser.add_subparsers(dest='command', required=True)
    listing = commands.add_parser('list', help='List investigations and their current status')
    listing.add_argument('--json', action='store_true')
    planning = commands.add_parser('plan', help='Inspect a read-only plan; no analysis or publication')
    planning.add_argument('investigation_id')
    planning.add_argument('--config', type=Path, help='JSON object of investigation-specific parameters')
    planning.add_argument('--set', action='append', default=[], metavar='KEY=JSON',
                          help='Override one parameter, e.g. year=2024; can be repeated')
    planning.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if args.command == 'list':
        investigations = list_investigations()
        if args.json:
            print(json.dumps([asdict(item) for item in investigations], indent=2))
        else:
            for item in investigations:
                print(f'{item.id}: {item.title} [{item.status}]')
        return 0
    try:
        parameters = json.loads(args.config.read_text()) if args.config else {}
        if not isinstance(parameters, dict):
            raise ValueError('Configuration must be a JSON object')
        for setting in args.set:
            key, separator, value = setting.partition('=')
            if not separator or not key:
                raise ValueError('--set requires KEY=JSON')
            parameters[key] = json.loads(value)
        plan = plan_investigation(args.investigation_id, parameters)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False, allow_nan=False))
    else:
        print(f'{plan.investigation.title} — planning, no results generated')
        print('Parameters: ' + json.dumps(plan.parameters, ensure_ascii=False))
        print('Inputs:')
        for entry in plan.inputs:
            print('  ' + entry['path'])
        print('Pending decisions:')
        for decision in plan.pending_decisions:
            print('  - ' + decision)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
