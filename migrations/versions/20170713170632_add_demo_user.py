# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c3a57c9f3bb7'
down_revision = 'a3b2c7e585b4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO users (id, name, display_name, created, admin)
        VALUES ('77af91ac-4ba2-4ecd-88eb-8ce650b62cce', 'demo', 'demo', now(), false)
    """)
    op.execute("""
        INSERT INTO api_tokens (id, user_id, token, description, created)
        VALUES (
            'c8e1878a-f6da-404a-ac0c-e86e5607d497',
            '77af91ac-4ba2-4ecd-88eb-8ce650b62cce',
            'D0123458B8E36326C60253FE4A7FF6662CAB0C48',
            'Demo Token',
            now()
        )
    """)
    op.execute("""
        INSERT INTO sources (id, name, active, updated, integration_name, conf)
        VALUES ('9b6b6391-5404-4e7f-bdb8-271c2cb42fbb', 'demo', true, now(), 'api', '{"private": false}')
    """)
    op.execute("""
        INSERT INTO source_users (source_id, user_id, role)
        VALUES (
            '9b6b6391-5404-4e7f-bdb8-271c2cb42fbb',
            '77af91ac-4ba2-4ecd-88eb-8ce650b62cce',
            'default'
        )
    """)


def downgrade():
    op.execute("DELETE FROM jobs WHERE source_id = '9b6b6391-5404-4e7f-bdb8-271c2cb42fbb'")
    op.execute("DELETE FROM sources WHERE id = '9b6b6391-5404-4e7f-bdb8-271c2cb42fbb'")
    op.execute("DELETE FROM users WHERE id = '77af91ac-4ba2-4ecd-88eb-8ce650b62cce'")
