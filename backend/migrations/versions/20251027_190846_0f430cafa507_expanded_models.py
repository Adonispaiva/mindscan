from alembic import op
import sqlalchemy as sa

# revisao e dependencias
revision = '20251027_190846_0f430cafa507'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('emotions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=True),
        sa.Column('label', sa.String(), nullable=True),
        sa.Column('intensity', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('session_tags',
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.PrimaryKeyConstraint('session_id', 'tag_id')
    )

def downgrade():
    op.drop_table('session_tags')
    op.drop_table('emotions')
    op.drop_table('tags')
    op.drop_table('sessions')
    op.drop_table('users')
