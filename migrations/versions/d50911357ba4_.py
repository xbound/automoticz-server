"""empty message

Revision ID: d50911357ba4
Revises: e9317a9c0ab0
Create Date: 2019-02-25 19:50:36.736950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd50911357ba4'
down_revision = 'e9317a9c0ab0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('jw_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jti')
    )
    op.create_table('scopes',
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.Column('credential_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['credential_id'], ['oauth2_credentials.id'], ),
    sa.ForeignKeyConstraint(['scope_id'], ['oauth2_scopes.id'], ),
    sa.PrimaryKeyConstraint('scope_id', 'credential_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scopes')
    op.drop_table('jw_token')
    op.drop_table('user')
    op.drop_table('oauth2_scopes')
    op.drop_table('oauth2_credentials')
    # ### end Alembic commands ###