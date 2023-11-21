"""template fields changes

Revision ID: dac396b13921
Revises: 74e3f8a6b3c2
Create Date: 2023-11-17 12:59:24.873502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dac396b13921'
down_revision = '74e3f8a6b3c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE eventtemplatevisibilityenum AS ENUM('MANDATORY', 'OPTIONAL', 'HIDDEN')")
    op.execute("CREATE TYPE phasevisibilityenum AS ENUM('REGULAR', 'HIDDEN')")
    op.execute("TRUNCATE works RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE work_phases RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE event_templates RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE event_templates_history RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE event_configurations RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE event_configurations_history RESTART IDENTITY CASCADE")


    with op.batch_alter_table('event_configurations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('MANDATORY', 'OPTIONAL', 'HIDDEN', name='eventtemplatevisibilityenum'), nullable=False))
        batch_op.add_column(sa.Column('repeat_count', sa.Integer(), nullable=False))
        batch_op.drop_column('mandatory')

    with op.batch_alter_table('event_configurations_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('MANDATORY', 'OPTIONAL', 'HIDDEN', name='eventtemplatevisibilityenum'), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('repeat_count', sa.Integer(), autoincrement=False, nullable=False))
        batch_op.drop_column('mandatory')

    with op.batch_alter_table('event_templates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('MANDATORY', 'OPTIONAL', 'HIDDEN', name='eventtemplatevisibilityenum'), nullable=False, comment='Indicate whether the event generated with this template should be autogenerated  or available for optional events or added in the back end using actions'))
        batch_op.drop_column('mandatory')

    with op.batch_alter_table('event_templates_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('MANDATORY', 'OPTIONAL', 'HIDDEN', name='eventtemplatevisibilityenum'), autoincrement=False, nullable=False, comment='Indicate whether the event generated with this template should be autogenerated  or available for optional events or added in the back end using actions'))
        batch_op.drop_column('mandatory')

    with op.batch_alter_table('phase_codes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('REGULAR', 'HIDDEN', name='phasevisibilityenum'), nullable=True))

    with op.batch_alter_table('phase_codes_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visibility', sa.Enum('REGULAR', 'HIDDEN', name='phasevisibilityenum'), autoincrement=False, nullable=True))

    with op.batch_alter_table('work_phases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sort_order', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('visibility', sa.Enum('REGULAR', 'HIDDEN', name='phasevisibilityenum'), autoincrement=False, nullable=True))

    with op.batch_alter_table('work_phases_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sort_order', sa.Integer(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('visibility', sa.Enum('REGULAR', 'HIDDEN', name='phasevisibilityenum'), autoincrement=False, nullable=True))

    with op.batch_alter_table('works', schema=None) as batch_op:
        batch_op.add_column(sa.Column('work_decision_date', sa.DateTime(timezone=True), nullable=True))

    with op.batch_alter_table('works_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('work_decision_date', sa.DateTime(timezone=True), autoincrement=False, nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('works_history', schema=None) as batch_op:
        batch_op.drop_column('work_decision_date')

    with op.batch_alter_table('works', schema=None) as batch_op:
        batch_op.drop_column('work_decision_date')

    with op.batch_alter_table('work_phases_history', schema=None) as batch_op:
        batch_op.drop_column('visibility')
        batch_op.drop_column('sort_order')

    with op.batch_alter_table('work_phases', schema=None) as batch_op:
        batch_op.drop_column('visibility')
        batch_op.drop_column('sort_order')

    with op.batch_alter_table('phase_codes_history', schema=None) as batch_op:
        batch_op.drop_column('visibility')

    with op.batch_alter_table('phase_codes', schema=None) as batch_op:
        batch_op.drop_column('visibility')

    with op.batch_alter_table('event_templates_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mandatory', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('visibility')

    with op.batch_alter_table('event_templates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mandatory', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('visibility')

    with op.batch_alter_table('event_configurations_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mandatory', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('repeat_count')
        batch_op.drop_column('visibility')

    with op.batch_alter_table('event_configurations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mandatory', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('repeat_count')
        batch_op.drop_column('visibility')

    # ### end Alembic commands ###
