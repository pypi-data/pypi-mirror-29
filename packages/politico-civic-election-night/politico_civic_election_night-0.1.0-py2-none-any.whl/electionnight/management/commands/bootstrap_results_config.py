import json
import os

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.conf import settings as project_settings

from election.models import Election, ElectionCycle
from electionnight.conf import settings as app_settings
from geography.models import DivisionLevel


class Command(BaseCommand):
    help = (
        'Creates config files used by our bash process to bake out '
        'election results from Elex and the AP.'
    )

    def serialize_cycle(self, cycle):
        """
        /election-results/cycle/
        """
        elections = Election.objects.filter(
            race__cycle__name=cycle,
            race__special=False,
        )

        if elections.count() == 0:
            return

        levels = ['national', 'state']
        config_key = cycle
        output_key = '{0}'.format(cycle)

        self._write_to_json(elections, config_key, levels, output_key)

        if elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                elections, config_key, levels, output_key
            )

    def serialize_federal_body(self, body, elections, cycle):
        """
        /election-results/cycle/senate/
        /election-results/cycle/house/
        """
        body_elections = elections.filter(
            race__office__body__slug=body,
            race__special=False,
        )

        if body_elections.count() == 0:
            return

        levels = ['state']
        config_key = body
        output_key = '{0}/{1}'.format(cycle, body)

        self._write_to_json(body_elections, config_key, levels, output_key)

        if body_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                body_elections, config_key, levels, output_key
            )

    def serialize_federal_exec(self, office, elections, cycle):
        """
        /election-results/cycle/president/
        """
        office_elections = elections.filter(
            race__office__slug=office,
            race__special=False,
        )

        if office_elections.count() == 0:
            return

        levels = ['national', 'state']
        config_key = office
        output_key = '{0}/{1}'.format(cycle, office)

        self._write_to_json(office_elections, config_key, levels, output_key)

        if office_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                office_elections, config_key, levels, output_key
            )

    def serialize_state(self, state, elections, cycle):
        """
        /election-results/cycle/state/
        """
        state_elections = elections.filter(
            Q(division__slug=state) | Q(division__parent__slug=state),
            race__special=False,
        )

        if state_elections.count() == 0:
            return

        levels = ['state', 'county']
        config_key = state
        output_key = '{0}/{1}'.format(cycle, state)

        self._write_to_json(state_elections, config_key, levels, output_key)

        if state_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                state_elections, config_key, levels, output_key
            )

    def serialize_special(self, state, elections, cycle):
        """
        /election-results/cycle/state/special-election/MMM-DD
        """
        state_elections = elections.filter(
            Q(division__slug=state) | Q(division__parent__slug=state),
            race__special=True,
        )

        if state_elections.count() == 0:
            return

        levels = ['state', 'county']
        config_key = state
        output_key = '{0}/{1}/special-election/{2}'.format(
            cycle,
            state,
            state_elections.first().election_day.special_election_datestring()
        )

        self._write_to_json(state_elections, config_key, levels, output_key)

        if state_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                state_elections, config_key, levels, output_key
            )

    def serialize_state_federal_body(self, state, body, elections, cycle):
        """
        /election-results/cycle/senate/state/
        /election-results/cycle/house/state/
        """
        state_federal_body_elections = elections.filter(
            Q(division__slug=state) | Q(division__parent__slug=state),
            race__office__body__slug=body,
            race__special=False,
        )

        if state_federal_body_elections.count() == 0:
            return

        levels = ['state', 'county']
        config_key = '{0}-{1}'.format(body, state)
        output_key = '{0}/{1}/{2}'.format(
            cycle,
            body,
            state
        )

        self._write_to_json(
            state_federal_body_elections, config_key, levels, output_key
        )

        if state_federal_body_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                state_federal_body_elections, config_key, levels, output_key
            )

    def serialize_state_body(self, state, body, elections, cycle):
        """
        /election-results/cycle/state/senate/
        /election-resutls/cycle/state/house/
        """
        state_body_elections = elections.filter(
            division__slug=state,
            race__office__body__slug=body,
            race__special=False,
        )

        if state_body_elections.count() == 0:
            return

        levels = ['state', 'county']
        config_key = '{0}-state-{1}'.format(state, body)
        output_key = '{0}/{1}/{2}'.format(
            cycle,
            state,
            body
        )

        self._write_to_json(
            state_body_elections, config_key, levels, output_key
        )

        if state_body_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                state_body_elections, config_key, levels, output_key
            )

    def serialize_state_federal_exec(self, state, office, elections, cycle):
        """
        /election-results/cycle/president/state/
        """
        state_office_elections = elections.filter(
            division__slug=state,
            race__office__slug=office,
            race__special=False,
        )

        if state_office_elections.count() == 0:
            return

        levels = ['state', 'county']
        config_key = '{0}-{1}'.format(office, state)
        output_key = '{0}/{1}/{2}'.format(
            cycle,
            office,
            state
        )

        self._write_to_json(
            state_office_elections, config_key, levels, output_key
        )

        if state_office_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                state_office_elections, config_key, levels, output_key
            )

    def serialize_state_exec(self, state, office, elections, cycle):
        """
        /election-results/cycle/state/governor/
        """
        state_exec_elections = elections.filter(
            division__slug=state,
            race__office__slug=office,
            race__special=False,
        )

        if state_exec_elections.count() == 0:
            return

        levels = ['state', 'county']
        config_key = '{0}-{1}'.format(state, office)
        output_key = '{0}/{1}/{2}'.format(
            cycle,
            state,
            office
        )

        self._write_to_json(
            state_exec_elections, config_key, levels, output_key
        )

        if state_exec_elections[0].election_type.is_primary():
            config_key = '{0}-{1}'.format(config_key, 'primary')
            output_key = os.path.join(output_key, 'primary')

            self._write_to_json(
                state_exec_elections, config_key, levels, output_key
            )

    def _write_to_json(self, elections, config_key, levels, output_key):
        full_output_path = os.path.join(
            project_settings.BASE_DIR,
            app_settings.RESULTS_STATIC_DIR,
            'election-results',
            output_key
        )

        ids = []
        for election in elections:
            try:
                ids.append(election.meta.ap_election_id)
            except Election.meta.RelatedObjectDoesNotExist:
                continue

        output = {
            'elections': ids,
            'levels': levels,
            'output_path': full_output_path
        }

        with open('{0}/{1}.json'.format(self.folder, config_key), 'w') as f:
            json.dump(output, f)

    def add_arguments(self, parser):
        parser.add_argument('election_date', type=str)

    def handle(self, *args, **options):
        self.folder = os.path.join(
            project_settings.BASE_DIR,
            app_settings.RESULTS_STATIC_DIR,
            'election-config'
        )

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        for f in os.listdir(self.folder):
            f_path = os.path.join(self.folder, f)

            try:
                if os.path.isfile(f_path):
                    os.unlink(f_path)
            except Exception as e:
                print(e)

        cycle_year = options['election_date'].split('-')[0]

        latest_cycle = ElectionCycle.objects.get(name=cycle_year).name
        # self.serialize_cycle(latest_cycle)

        elections = Election.objects.filter(
            election_day__date=options['election_date'],
        )

        federal_bodies = set(elections.filter(
            race__office__body__label__isnull=False,
            race__office__jurisdiction__name='U.S. Federal Government'
        ).values_list('race__office__body__slug', flat=True))

        state_bodies = set(elections.filter(
            race__office__body__label__isnull=False,
        ).exclude(
            race__office__jurisdiction__name='U.S. Federal Government'
        ).values_list('race__office__body__slug', flat=True))

        states = elections.filter(
            race__office__division__level__name=DivisionLevel.STATE,
        ).values_list('division__slug', flat=True)

        district_parents = elections.filter(
            race__office__division__level__name=DivisionLevel.DISTRICT,
        ).values_list('division__parent__slug', flat=True)

        states = set(list(states) + list(district_parents))

        federal_exec_offices = set(elections.filter(
            race__office__body__isnull=True,
            race__office__jurisdiction__name='U.S. Federal Government'
        ).values_list('race__office__slug', flat=True))

        state_exec_offices = set(elections.filter(
            race__office__body__isnull=True,
        ).exclude(
            race__office__jurisdiction__name='U.S. Federal Government'
        ).values_list('race__office__slug', flat=True))

        for body in federal_bodies:
            self.serialize_federal_body(body, elections, latest_cycle)

            for state in states:
                self.serialize_state_federal_body(
                    state, body, elections, latest_cycle
                )

        for state in states:
            self.serialize_state(state, elections, latest_cycle)
            self.serialize_special(state, elections, latest_cycle)

            for body in state_bodies:
                self.serialize_state_body(state, body, elections, latest_cycle)

            for office in state_exec_offices:
                self.serialize_state_exec(
                    state, office, elections, latest_cycle
                )

        for office in federal_exec_offices:
            self.serialize_federal_exec(office, elections, latest_cycle)

            for state in states:
                self.serialize_state_exec(
                    state, office, elections, latest_cycle
                )
