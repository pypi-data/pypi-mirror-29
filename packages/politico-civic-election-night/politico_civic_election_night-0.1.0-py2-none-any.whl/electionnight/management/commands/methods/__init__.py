from .bootstrap.executive_office import ExecutiveOffice
from .bootstrap.legislative_office import LegislativeOffice
from .bootstrap.special_election import SpecialElection


class BootstrapContentMethods(
    ExecutiveOffice,
    LegislativeOffice,
    SpecialElection
):
    pass
