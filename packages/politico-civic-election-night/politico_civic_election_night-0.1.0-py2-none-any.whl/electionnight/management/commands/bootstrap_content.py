from django.core.management.base import BaseCommand
from election.models import ElectionDay
from geography.models import DivisionLevel
from government.models import Jurisdiction
from tqdm import tqdm

from .methods import BootstrapContentMethods


class Command(BaseCommand, BootstrapContentMethods):
    help = (
        'Bootstraps page content items for pages for all elections on an '
        'election day. Must be run AFTER bootstrap_election command.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'elections',
            nargs='+',
            help="Election dates to create content for."
        )

    def route_election(self, election):
        """
        Legislative or executive office?
        """
        if election.race.special:
            self.bootstrap_special_election(election)
        elif election.race.office.is_executive:
            self.bootstrap_executive_office(election)
        else:
            self.bootstrap_legislative_office(election)

    def handle(self, *args, **options):
        self.NATIONAL_LEVEL = DivisionLevel.objects.get(
            name=DivisionLevel.COUNTRY)
        self.STATE_LEVEL = DivisionLevel.objects.get(
            name=DivisionLevel.STATE)
        self.FEDERAL_JURISDICTION = Jurisdiction.objects.get(
            division__level=self.NATIONAL_LEVEL)
        print('Bootstrapping page content')
        election_dates = options['elections']

        for election_date in election_dates:
            print('> {}'.format(election_date))
            election_day = ElectionDay.objects.get(date=election_date)
            for election in tqdm(election_day.elections.all()):
                self.route_election(election)
        print('Done.')
