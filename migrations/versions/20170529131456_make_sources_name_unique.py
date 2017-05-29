# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '29d6a95d9387'
down_revision = '89177f936b9b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        'sources_name_integration_name_key', 'sources', ['name', 'integration_name']);


def downgrade():
    op.drop_constraint('sources_name_integration_name_key', 'sources');
