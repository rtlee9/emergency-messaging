from django.core.management.base import BaseCommand
import json
import pandas as pd
import numpy as np
import glob
import logging

from enrollment.students import models

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, **options):
        # read data
        raw_data_filenames = glob.glob('data/* Parent Contacts.xlsx')
        df_campuses = []
        for rdf in raw_data_filenames:
            df = pd.read_excel(rdf, skiprows=3, index_col=0)
            df.columns = [df.columns[i - 1] if i > 0 else 'id' for i, col in enumerate(df.columns)]
            df.set_index('id', inplace=True)
            df['filename'] = rdf
            df['campus'] = rdf.split('/')[1].split(' ')[0]
            df_campuses.append(df)
        df = pd.concat(df_campuses, sort=False).\
            rename(axis=1, mapper={'Unnamed: 10': 'meta'}).\
            rename(axis=1, mapper={col: col.lower().replace(' ', '_').replace('#', 'num') for col in df.columns})
        logger.info('Read {:,.0f} students from disk'.format(df.shape[0]))

        # process programs
        df.enrolled_programs = np.where(
            df.enrolled_programs.str.contains('(', regex=False),
            df.enrolled_programs.str.split('(').str[1].str.split(')').str[0],
            df.enrolled_programs.str.strip(),
        )

        # process parent names
        split = df.parent_1_name.str.split(', ')
        df['parent_1_last_name'] = split.str[0]
        df['parent_1_first_name'] = split.str[1]
        split = df.parent_2_name.str.split(', ')
        df['parent_2_last_name'] = split.str[0]
        df['parent_2_first_name'] = split.str[1]

        for idx, sr in df.iterrows():
            site, created = models.Site.objects.get_or_create(name=sr.campus)
            student, created = models.Student.objects.get_or_create(
                first_name=sr.first_name.strip(), last_name=sr.last_name.strip())

            student.classrooms.clear()
            classroom, created = models.Classroom.objects.get_or_create(
                name=sr.enrolled_programs, site=site)
            student.classrooms.add(classroom)

            p1, created = models.Parent.objects.get_or_create(
                first_name=sr.parent_1_first_name,
                last_name=sr.parent_1_last_name,
                email=sr.parent_1_email,
                phone_number=sr.parent_1_mobile_num,
            )
            p1.students.add(student)
            p2, created = models.Parent.objects.get_or_create(
                first_name=sr.parent_2_first_name,
                last_name=sr.parent_2_last_name,
                email=sr.parent_2_email,
                phone_number=sr.parent_2_mobile_num,
            )
            p2.students.add(student)
        logger.info('Success')
