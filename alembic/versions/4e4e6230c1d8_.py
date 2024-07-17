"""empty message

Revision ID: 4e4e6230c1d8
Revises: 717dc1a6e60c
Create Date: 2024-07-12 14:00:07.973102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e4e6230c1d8'
down_revision: Union[str, None] = '717dc1a6e60c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('groupname', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_id'), 'group', ['id'], unique=False)
    op.create_table('intake',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orientation', sa.Date(), nullable=False),
    sa.Column('startdate', sa.Date(), nullable=False),
    sa.Column('enddate', sa.Date(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.Column('groupid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['groupid'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_intake_id'), 'intake', ['id'], unique=False)
    op.create_table('semester',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('startdate', sa.Date(), nullable=True),
    sa.Column('enddate', sa.Date(), nullable=True),
    sa.Column('midsemstart', sa.Date(), nullable=True),
    sa.Column('midsemend', sa.Date(), nullable=True),
    sa.Column('midsemduration', sa.Integer(), nullable=True),
    sa.Column('bufferstart', sa.Date(), nullable=True),
    sa.Column('bufferend', sa.Date(), nullable=True),
    sa.Column('buffersemduration', sa.Integer(), nullable=True),
    sa.Column('examstart', sa.Date(), nullable=True),
    sa.Column('examend', sa.Date(), nullable=True),
    sa.Column('examduration', sa.Integer(), nullable=True),
    sa.Column('intakeid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intakeid'], ['intake.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_semester_id'), 'semester', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_semester_id'), table_name='semester')
    op.drop_table('semester')
    op.drop_index(op.f('ix_intake_id'), table_name='intake')
    op.drop_table('intake')
    op.drop_index(op.f('ix_group_id'), table_name='group')
    op.drop_table('group')
    # ### end Alembic commands ###
