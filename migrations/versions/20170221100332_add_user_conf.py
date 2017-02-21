# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '244d4ab5a66d'
down_revision = 'e3a19aabb983'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('conf', postgresql.JSONB(), nullable=True))


def downgrade():
    op.drop_column('users', 'conf')
