"""create clinica tables
Revision ID: 0001_create_clinica_tables
Revises: 
Create Date: 2026-06-30
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_create_clinica_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Crear tabla razas
    op.create_table(
        'razas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_razas_nombre', 'razas', ['nombre'])

    # Crear tabla propietarios
    op.create_table(
        'propietarios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('apellido', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), unique=True),
        sa.Column('telefono', sa.String(length=20), nullable=True),
        sa.Column('direccion', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_propietarios_nombre', 'propietarios', ['nombre'])
    op.create_index('ix_propietarios_email', 'propietarios', ['email'])

    # Crear tabla mascotas
    op.create_table(
        'mascotas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('edad', sa.Integer(), nullable=True),
        sa.Column('peso', sa.Float(), nullable=True),
        sa.Column('propietario_id', sa.Integer(), sa.ForeignKey('propietarios.id')),
        sa.Column('raza_id', sa.Integer(), sa.ForeignKey('razas.id')),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_mascotas_nombre', 'mascotas', ['nombre'])


def downgrade() -> None:
    op.drop_table('mascotas')
    op.drop_table('propietarios')
    op.drop_table('razas')

