# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3b2c7e585b4'
down_revision = '30f96996b8ae'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('api_tokens',
        sa.Column('id', sa.Unicode, primary_key=True),
        sa.Column('user_id', sa.Unicode(), nullable=False),
        sa.Column('token', sa.Unicode(), unique=True, nullable=False),
        sa.Column('description', sa.Unicode(), nullable=True),
        sa.Column('created', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )


def downgrade():
    op.drop_table('api_tokens')
