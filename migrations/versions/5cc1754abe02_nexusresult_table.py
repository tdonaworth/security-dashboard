"""NexusResult table

Revision ID: 5cc1754abe02
Revises: d9e4b5440050
Create Date: 2020-07-02 13:44:39.589568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5cc1754abe02"
down_revision = "d9e4b5440050"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "nexus_result",
        sa.Column("row_id", sa.Integer(), nullable=False),
        sa.Column("create_date", sa.DateTime(), nullable=True),
        sa.Column("docker_tag", sa.String(length=20), nullable=True),
        sa.Column("service_name", sa.String(length=30), nullable=True),
        sa.Column("jenkins_url", sa.String(length=200), nullable=True),
        sa.Column("nexusiq_url", sa.String(length=200), nullable=True),
        sa.Column("yarn_log", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("row_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("nexus_result")
    # ### end Alembic commands ###
