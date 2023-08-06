import os
import requests
import us

from django.core.management.base import BaseCommand
from geography.models import Division, DivisionLevel
from government.models import Body, Jurisdiction, Office
from tqdm import tqdm

BASE_URL = 'https://api.propublica.org/congress/v1/'


class Command(BaseCommand):
    help = (
        'Scrapes the ProPublica Congress API for federal Congress offices'
    )

    fed = Jurisdiction.objects.get(name="U.S. Federal Government")

    def build_congressional_offices(self, chamber):
        r = requests.get(
            '{0}{1}/{2}/members.json'.format(BASE_URL, '115', chamber),
            headers={
                'X-API-Key': os.environ.get('PROPUBLICA_CONGRESS_API_KEY')
            }
        )

        members = r.json()

        print('Loading U.S. {0} offices'.format(chamber.title()))
        for member in tqdm(members['results'][0]['members']):
            full_state = us.states.lookup(member['state'])
            if int(full_state.fips) > 56 or int(full_state.fips) == 11:
                continue

            if chamber == 'senate':
                for class_tup in Office.SENATE_CLASSES:
                    if class_tup[0] == member['senate_class']:
                        senate_class = class_tup[0]

                name = 'U.S. Senate, {0}, Class {1}'.format(
                    full_state.name,
                    senate_class
                )
                division_level = DivisionLevel.objects.get(
                    name='state'
                )
                division = Division.objects.get(
                    level=division_level,
                    code_components__postal=member['state']
                )

            elif chamber == 'house':
                senate_class = None

                name = 'U.S. House, {0}, District {1}'.format(
                    full_state.name,
                    member['district']
                )
                division_level = DivisionLevel.objects.get(
                    name='district'
                )

                code = ('00'
                        if member['at_large']
                        else member['district'].zfill(2)
                        )

                division = Division.objects.get(
                    level=division_level,
                    parent__code_components__postal=member['state'],
                    code=code
                )

            body = Body.objects.get(
                slug=chamber,
                jurisdiction=self.fed
            )

            Office.objects.get_or_create(
                name=name,
                label=name,
                jurisdiction=self.fed,
                division=division,
                body=body,
                senate_class=senate_class
            )

    def build_governorships(self):
        state_level = DivisionLevel.objects.get(name='state')

        state_jurisdictions = Jurisdiction.objects.filter(
            division__level=state_level
        )

        print('Loading governorships')
        for jurisdiction in tqdm(state_jurisdictions):
            name = '{0} Governor'.format(jurisdiction.division.name)

            Office.objects.get_or_create(
                name=name,
                label=name,
                jurisdiction=jurisdiction,
                division=jurisdiction.division,
            )

    def build_presidency(self):
        USA = Division.objects.get(
            code='00',
            level__name='country'
        )

        print('Loading presidency')

        Office.objects.get_or_create(
            slug="president",
            name="President of the United States",
            label="U.S. President",
            short_label="President",
            jurisdiction=self.fed,
            division=USA,
        )

    def handle(self, *args, **options):
        print('Loading offices')

        for chamber in ['senate', 'house']:
            self.build_congressional_offices(chamber)

        self.build_governorships()
        self.build_presidency()
