import us
from django.core.management.base import BaseCommand
from geography.models import Division, DivisionLevel
from government.models import Jurisdiction
from tqdm import tqdm


class Command(BaseCommand):
    help = (
        'Loads federal and state jurisdictions. Must be run AFTER the'
        'bootstrap_geography command.'
    )

    def handle(self, *args, **options):
        print('Loading jurisdictions')
        USA = Division.objects.get(code='00', level__name='country')
        FED, created = Jurisdiction.objects.get_or_create(
            name="U.S. Federal Government",
            division=USA
        )
        state_level = DivisionLevel.objects.get(name='state')
        for state in tqdm(us.states.STATES):
            division = Division.objects.get(code=state.fips, level=state_level)
            name = '{} State Government'.format(state.name)
            if str(state.fips) == '11':
                name = 'Government of the District of Columbia'
            Jurisdiction.objects.get_or_create(
                name=name,
                division=division,
                parent=FED,
            )
        self.stdout.write(
            self.style.SUCCESS('Done.')
        )
