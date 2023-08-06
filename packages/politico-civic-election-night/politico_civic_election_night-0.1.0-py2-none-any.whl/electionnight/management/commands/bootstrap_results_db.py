import json
import os
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.core.management import call_command
from time import sleep, time
from tqdm import tqdm

from election.models import Candidate, CandidateElection
from electionnight.conf import settings as app_settings
from electionnight.models import APElectionMeta
from geography.models import Division, DivisionLevel
from vote.models import Votes


class Command(BaseCommand):
    help = (
        'Ingests master results JSON file from Elex and updates the results '
        'models in Django.'
    )

    def download_results(self, options):
        writefile = open('master.json', 'w')
        elex_args = [
            'elex',
            'results',
            options['election_date'],
            '--national-only',
            '-o',
            'json',
        ]

        if options['test']:
            elex_args.append('-t')

        subprocess.run(elex_args, stdout=writefile)

    def process_result(self, result, tabulated):
        if result['is_ballot_measure']:
            return

        if result['level'] != 'state':
            return

        ap_meta = APElectionMeta.objects.get(
            ap_election_id=result['raceid'],
        )

        id_components = result['id'].split('-')
        candidate_id = '{0}-{1}'.format(
            id_components[1],
            id_components[2]
        )
        candidate = Candidate.objects.get(
            ap_candidate_id=candidate_id
        )

        candidate_election = CandidateElection.objects.get(
            election=ap_meta.election,
            candidate=candidate
        )

        if result['level'] in ['county', 'township']:
            division = Division.objects.get(code=result['fipscode'])
        else:
            division = Division.objects.get(
                level__name=DivisionLevel.STATE,
                code_components__postal=result['statepostal']
            )

        filter_kwargs = {
            'candidate_election': candidate_election,
            'division': division
        }

        kwargs = {}

        if not ap_meta.override_ap_votes:
            kwargs['count'] = result['votecount']
            kwargs['pct'] = result['votepct']

        if not ap_meta.override_ap_call:
            kwargs['winning'] = result['winner']
            kwargs['runoff'] = result['runoff']

        if ap_meta.precincts_reporting != result['precinctsreporting']:
            ap_meta.precincts_reporting = result['precinctsreporting']
            ap_meta.precincts_total = result['precinctstotal']
            ap_meta.precincts_reporting_pct = result['precinctsreportingpct']

        if (result['precinctsreportingpct'] == 1 or result['uncontested']
                or tabulated):
            ap_meta.tabulated = True

        ap_meta.save()

        Votes.objects.filter(**filter_kwargs).update(**kwargs)

    def main(self, options):
        start = 0

        while True:
            now = time()
            if (now - start) > app_settings.DATABASE_UPLOAD_DAEMON_INTERVAL:
                start = now

                if options['download']:
                    self.download_results(options)

                try:
                    data = json.load(open('reup.json'))
                except json.decoder.JSONDecodeError:
                    print('waiting for file to be available')
                    sleep(5)
                    data = json.load(open('reup.json'))

                for result in tqdm(data):
                    self.process_result(result, options['tabulated'])

                call_command(
                    'bake_elections',
                    options['election_date'],
                )

            if options['run_once']:
                print('run once specified, exiting')
                sys.exit(0)

            sleep(1)

    def add_arguments(self, parser):
        parser.add_argument('election_date', type=str)
        parser.add_argument(
            '--test',
            dest='test',
            action='store_true',
        )
        parser.add_argument(
            '--download',
            dest='download',
            action='store_true'
        )
        parser.add_argument(
            '--run_once',
            dest='run_once',
            action='store_true'
        )
        parser.add_argument(
            '--tabulated',
            dest='tabulated',
            action='store_true'
        )

    def handle(self, *args, **options):
        self.main(options)
