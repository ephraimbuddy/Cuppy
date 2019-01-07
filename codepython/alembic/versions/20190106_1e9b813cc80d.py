"""init

Revision ID: 1e9b813cc80d
Revises: 
Create Date: 2019-01-06 04:19:27.291763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e9b813cc80d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=80), nullable=False),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_auth_groups')),
    sa.UniqueConstraint('name', name=op.f('uq_auth_groups_name'))
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories'))
    )
    op.create_table('navs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=True),
    sa.Column('path', sa.Unicode(length=255), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('before', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['navs.id'], name=op.f('fk_navs_parent_id_navs')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_navs'))
    )
    op.create_table('root',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_root'))
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tags'))
    )
    op.create_table('user_factory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_factory'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Unicode(length=50), nullable=False),
    sa.Column('email', sa.Unicode(length=50), nullable=False),
    sa.Column('password_hash', sa.UnicodeText(), nullable=True),
    sa.Column('first_name', sa.Unicode(length=50), nullable=True),
    sa.Column('last_name', sa.Unicode(length=50), nullable=True),
    sa.Column('about', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('auth_user_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('ip_addr', sa.Unicode(length=39), nullable=False),
    sa.Column('event', sa.Enum('L', 'R', 'P', 'F', name='event'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_auth_user_log_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_auth_user_log'))
    )
    op.create_index(op.f('ix_auth_user_log_user_id'), 'auth_user_log', ['user_id'], unique=False)
    op.create_table('contents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('published', sa.Boolean(name='published'), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('modification_date', sa.DateTime(), nullable=True),
    sa.Column('in_navigation', sa.Boolean(name='in_navigation'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['navs.id'], name=op.f('fk_contents_id_navs')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_contents_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_contents'))
    )
    op.create_table('section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['navs.id'], name=op.f('fk_section_id_navs')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_section'))
    )
    op.create_table('user_activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Unicode(length=100), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_activity_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_activity'))
    )
    op.create_index(op.f('ix_user_activity_user_id'), 'user_activity', ['user_id'], unique=False)
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['auth_groups.id'], name=op.f('fk_user_group_group_id_auth_groups'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_group_user_id_users'), onupdate='CASCADE', ondelete='CASCADE')
    )
    op.create_index('user_group_index', 'user_group', ['user_id', 'group_id'], unique=False)
    op.create_table('content_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['contents.id'], name=op.f('fk_content_tags_content_id_contents')),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name=op.f('fk_content_tags_tag_id_tags')),
    sa.PrimaryKeyConstraint('tag_id', 'content_id', name=op.f('pk_content_tags'))
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['contents.id'], name=op.f('fk_documents_id_contents')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_documents'))
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.Unicode(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], name=op.f('fk_files_document_id_documents')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_files_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_files'))
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_posts_category_id_categories')),
    sa.ForeignKeyConstraint(['id'], ['documents.id'], name=op.f('fk_posts_id_documents')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts'))
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('files')
    op.drop_table('documents')
    op.drop_table('content_tags')
    op.drop_index('user_group_index', table_name='user_group')
    op.drop_table('user_group')
    op.drop_index(op.f('ix_user_activity_user_id'), table_name='user_activity')
    op.drop_table('user_activity')
    op.drop_table('section')
    op.drop_table('contents')
    op.drop_index(op.f('ix_auth_user_log_user_id'), table_name='auth_user_log')
    op.drop_table('auth_user_log')
    op.drop_table('users')
    op.drop_table('user_factory')
    op.drop_table('tags')
    op.drop_table('root')
    op.drop_table('navs')
    op.drop_table('categories')
    op.drop_table('auth_groups')
    # ### end Alembic commands ###