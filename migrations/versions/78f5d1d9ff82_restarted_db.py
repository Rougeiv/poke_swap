"""restarted db

Revision ID: 78f5d1d9ff82
Revises: 
Create Date: 2024-05-02 08:51:56.939491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78f5d1d9ff82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pokedex_num', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('shiny', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_pokemon_name'), ['name'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('trade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('pokemon1', sa.String(length=32), nullable=False),
    sa.Column('pokemon2', sa.String(length=32), nullable=False),
    sa.Column('user_id1', sa.Integer(), nullable=False),
    sa.Column('user_id2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id1'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id2'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('trade', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_trade_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_trade_user_id1'), ['user_id1'], unique=False)
        batch_op.create_index(batch_op.f('ix_trade_user_id2'), ['user_id2'], unique=False)

    op.create_table('user_pokemon',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pokemon_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'pokemon_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_pokemon')
    with op.batch_alter_table('trade', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_trade_user_id2'))
        batch_op.drop_index(batch_op.f('ix_trade_user_id1'))
        batch_op.drop_index(batch_op.f('ix_trade_timestamp'))

    op.drop_table('trade')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_pokemon_name'))

    op.drop_table('pokemon')
    # ### end Alembic commands ###
