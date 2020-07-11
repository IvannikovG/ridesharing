"""empty message

Revision ID: 9af42215c3c8
Revises: 7cde205ff39b
Create Date: 2020-06-23 17:31:37.960260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af42215c3c8'
down_revision = '7cde205ff39b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ride', sa.Column('about_ride', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ride', 'about_ride')
    # ### end Alembic commands ###
