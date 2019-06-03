"""empty message

Revision ID: 426b6640c135
Revises: 
Create Date: 2019-06-02 22:31:32.635028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '426b6640c135'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('identity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_idx', sa.Integer(), nullable=True),
    sa.Column('logged_in', sa.Boolean(), nullable=True),
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
    op.create_table('wsdevices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idx', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('machine', sa.String(length=100), nullable=True),
    sa.Column('sysname', sa.String(length=100), nullable=True),
    sa.Column('version', sa.String(length=100), nullable=True),
    sa.Column('device_type', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_uuid', sa.String(), nullable=False),
    sa.Column('client', sa.String(length=50), nullable=True),
    sa.Column('identity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['identity_id'], ['identity.id'], ),
    sa.PrimaryKeyConstraint('id')
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
    sa.Column('token_type', sa.String(length=10), nullable=True),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.client_uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    op.drop_table('scopes')
    op.drop_table('clients')
    op.drop_table('wsdevices')
    op.drop_table('oauth2_scopes')
    op.drop_table('oauth2_credentials')
    op.drop_table('identity')
    # ### end Alembic commands ###