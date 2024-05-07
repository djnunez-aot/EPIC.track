"""Add team co-lead to staff roles

Revision ID: c64aaa268112
Revises: a67589eb0b5f
Create Date: 2024-04-22 16:25:53.831382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c64aaa268112'
down_revision = 'a67589eb0b5f'
branch_labels = None
depends_on = None
team_co_lead = 'Team Co-Lead'

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    roles = sa.Table(
        'roles',
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('sort_order', sa.Integer, nullable=False),
    )

    op.bulk_insert(roles, [
                   {'name': team_co_lead, 'sort_order': 5},
    ])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f"DELETE FROM roles WHERE name = '{team_co_lead}'")
    # ### end Alembic commands ###
