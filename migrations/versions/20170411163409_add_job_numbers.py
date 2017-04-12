# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '89177f936b9b'
down_revision = '384743329d34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('jobs', sa.Column('number', sa.Integer(), nullable=True))
    op.add_column('sources', sa.Column('job_number', sa.Integer(),
                  nullable=True))

    statement1 = '''
        UPDATE jobs SET number = tmp_jobs.rn
        FROM (
            SELECT ROW_NUMBER() OVER (PARTITION BY jobs.source_id
                                      ORDER BY finished) rn, id
            FROM jobs) AS tmp_jobs
        WHERE jobs.id = tmp_jobs.id
    '''
    op.execute(statement1)

    statement2 = '''
    UPDATE sources AS s SET job_number = 1
    '''
    op.execute(statement2)

    statement3 = '''
    UPDATE sources AS s SET job_number = (
        SELECT MAX(j.number) + 1 FROM jobs AS j WHERE s.id = j.source_id)
    WHERE s.active = 't'
    '''
    op.execute(statement3)

    statement4 = '''
    CREATE OR REPLACE FUNCTION add_job_number()
        RETURNS trigger LANGUAGE plpgsql AS
    $BODY$
    DECLARE
        next_value integer;
    BEGIN

        SELECT job_number FROM sources WHERE id = NEW.source_id INTO next_value;

        UPDATE sources SET job_number = job_number + 1 WHERE id = NEW.source_id;

        NEW.number = next_value;

        RETURN NEW;

    END;
    $BODY$
    '''
    op.execute(statement4)

    statement5 = '''
    CREATE TRIGGER job_number
        BEFORE INSERT
        ON jobs
        FOR EACH ROW
        EXECUTE PROCEDURE add_job_number();
    '''
    op.execute(statement5)


def downgrade():
    op.execute('DROP TRIGGER IF EXISTS job_number ON jobs')
    op.execute('DROP FUNCTION IF EXISTS add_job_number()')
    op.drop_column('jobs', 'number')
    op.drop_column('sources', 'job_number')
