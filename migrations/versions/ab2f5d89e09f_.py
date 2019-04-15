"""empty message

Revision ID: ab2f5d89e09f
Revises: 
Create Date: 2019-04-07 17:47:39.272032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab2f5d89e09f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=True),
    sa.Column('brand', sa.String(length=50), nullable=True),
    sa.Column('manufacturer', sa.String(length=50), nullable=True),
    sa.Column('product', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth2_credentials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token_uri', sa.String(length=100), nullable=False),
    sa.Column('client_id', sa.String(length=100), nullable=False),
    sa.Column('client_secret', sa.String(length=100), nullable=False),
    sa.Column('token', sa.String(length=250), nullable=False),
    sa.Column('refresh_token', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id')
    )
    op.create_table('oauth2_scopes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scope', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('scope')
    )
    op.create_table('usagelog',
    sa.Column('log_id', sa.Integer(), nullable=False),
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('user_idx', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('log_id')
    )
    op.create_table('scopes',
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.Column('credential_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['credential_id'], ['oauth2_credentials.id'], ),
    sa.ForeignKeyConstraint(['scope_id'], ['oauth2_scopes.id'], ),
    sa.PrimaryKeyConstraint('scope_id', 'credential_id')
    )
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    op.drop_table('scopes')
    op.drop_table('usagelog')
    op.drop_table('oauth2_scopes')
    op.drop_table('oauth2_credentials')
    op.drop_table('devices')
    # ### end Alembic commands ###