# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op


# revision identifiers, used by Alembic.
revision = '764d8a0341e3'
down_revision = '75a21383f7ed'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('jobs', 'job_id', new_column_name='id')


def downgrade():
    op.alter_column('jobs', 'id', new_column_name='job_id')
