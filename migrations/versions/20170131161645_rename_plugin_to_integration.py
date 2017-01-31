# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op


# revision identifiers, used by Alembic.
revision = '3acb947457ed'
down_revision = '8fa94f89941f'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column('jobs', 'plugin_conf', new_column_name='integration_conf')
    op.alter_column('jobs', 'plugin_name', new_column_name='integration_name')


def downgrade():
    op.alter_column('jobs', 'integration_conf', new_column_name='plugin_conf')
    op.alter_column('jobs', 'integration_name', new_column_name='plugin_name')
