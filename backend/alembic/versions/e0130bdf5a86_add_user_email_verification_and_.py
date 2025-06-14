"""add_user_email_verification_and_password_reset_fields

Revision ID: e0130bdf5a86
Revises: 
Create Date: 2025-05-30 14:24:49.387869 # Retaining original create date

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0130bdf5a86'
down_revision: Union[str, None] = None # This is the first migration
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_verified_email', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('users', sa.Column('email_verification_token', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_email_verification_token'), 'users', ['email_verification_token'], unique=True)
    op.add_column('users', sa.Column('password_reset_token', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_password_reset_token'), 'users', ['password_reset_token'], unique=True)
    op.add_column('users', sa.Column('password_reset_token_expiry', sa.DateTime(), nullable=True))
    
    # Change User.is_active to nullable=False, assuming it was previously nullable=True
    # Defaulting to True if it's a new constraint on existing rows.
    op.alter_column('users', 'is_active', 
                    existing_type=sa.Boolean(), 
                    nullable=False, 
                    server_default=sa.true())
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_active', 
                    existing_type=sa.Boolean(), 
                    nullable=True, 
                    server_default=sa.true()) # Revert nullability, keeping server_default consistent if it was there
    
    op.drop_index(op.f('ix_users_password_reset_token'), table_name='users')
    op.drop_column('users', 'password_reset_token_expiry')
    op.drop_column('users', 'password_reset_token')
    
    op.drop_index(op.f('ix_users_email_verification_token'), table_name='users')
    op.drop_column('users', 'email_verification_token')
    op.drop_column('users', 'is_verified_email')
    # ### end Alembic commands ###
