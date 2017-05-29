# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '30f96996b8ae'
down_revision = '29d6a95d9387'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE UNIQUE INDEX sources_github_id_key ON sources ((conf->'github_id'))")


def downgrade():
    op.drop_index('sources_github_id_key', 'sources');
