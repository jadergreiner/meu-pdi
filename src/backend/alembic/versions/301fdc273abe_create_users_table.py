"""create_users_table

Revision ID: 301fdc273abe
Revises:
Create Date: 2025-11-03 13:56:08.959762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '301fdc273abe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nome_completo', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('email_validado', sa.Boolean(), nullable=False, default=False),
        sa.Column('token_validacao', sa.String(length=255), nullable=True),
        sa.Column('token_expiracao', sa.DateTime(timezone=True), nullable=True),
        sa.Column('foto_perfil', sa.String(length=500), nullable=True),
        sa.Column('cargo_atual', sa.String(length=100), nullable=True),
        sa.Column('empresa_atual', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('linkedin_url', sa.String(length=500), nullable=True),
        sa.Column('github_url', sa.String(length=500), nullable=True),
        sa.Column('pdi_status', sa.String(length=50), nullable=False, default='iniciando'),
        sa.Column('pdi_objetivos', sa.Text(), nullable=True),
        sa.Column('pdi_progresso', sa.Integer(), nullable=False, default=0),
        sa.Column('pdi_ultima_atualizacao', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('data_cadastro', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('data_atualizacao', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()'), onupdate=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    # Create index on email for faster lookups
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    # Drop users table
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
