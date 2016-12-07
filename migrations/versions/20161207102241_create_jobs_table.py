# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from alembic import op


# revision identifiers, used by Alembic.
revision = '75a21383f7ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('jobs',
        sa.Column('job_id', sa.Unicode),
        sa.Column('created', sa.DateTime(timezone=True)),
        sa.Column('finished', sa.DateTime(timezone=True)),
        sa.Column('status', sa.Unicode),
        sa.Column('report', JSONB),
        sa.Column('error', JSONB),
        sa.Column('plugin_name', sa.Unicode),
        sa.Column('plugin_conf', JSONB),
    )


def downgrade():
    op.drop_table('jobs')
