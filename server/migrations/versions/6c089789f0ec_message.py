"""message

Revision ID: 6c089789f0ec
Revises: debbe271c747
Create Date: 2024-03-17 13:31:40.437702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c089789f0ec'
down_revision = 'debbe271c747'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pizzas', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('ingredients',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.FLOAT(),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('restaurant_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('pizza_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.alter_column('pizza_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('restaurant_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.Integer(),
               type_=sa.FLOAT(),
               existing_nullable=False)

    with op.batch_alter_table('pizzas', schema=None) as batch_op:
        batch_op.alter_column('ingredients',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
