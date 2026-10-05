from alembic import op
import sqlalchemy as sa
revision='0001_initial'; down_revision=None; branch_labels=None; depends_on=None

def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer,primary_key=True), sa.Column('name',sa.String(120),nullable=False), sa.Column('email',sa.String(255),nullable=False,unique=True), sa.Column('password_hash',sa.String(255),nullable=False), sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))
    op.create_table('documents', sa.Column('id',sa.Integer,primary_key=True), sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False), sa.Column('filename',sa.String(255),nullable=False), sa.Column('file_type',sa.String(20),nullable=False), sa.Column('file_size',sa.BigInteger,nullable=False), sa.Column('extracted_text',sa.Text,nullable=False), sa.Column('content_hash',sa.String(64)), sa.Column('status',sa.String(20),nullable=False), sa.Column('created_at',sa.DateTime(timezone=True),nullable=False), sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False))
    op.create_table('document_chunks', sa.Column('id',sa.Integer,primary_key=True), sa.Column('document_id',sa.Integer,sa.ForeignKey('documents.id',ondelete='CASCADE'),nullable=False), sa.Column('chunk_index',sa.Integer,nullable=False), sa.Column('content',sa.Text,nullable=False))
    op.create_table('integrations', sa.Column('id',sa.Integer,primary_key=True), sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False), sa.Column('provider',sa.String(50),nullable=False), sa.Column('access_token',sa.Text), sa.Column('refresh_token',sa.Text), sa.Column('expires_at',sa.DateTime(timezone=True)), sa.Column('created_at',sa.DateTime(timezone=True),nullable=False), sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False), sa.UniqueConstraint('user_id','provider',name='uq_user_provider'))
    op.create_table('chat_history', sa.Column('id',sa.Integer,primary_key=True), sa.Column('document_id',sa.Integer,sa.ForeignKey('documents.id',ondelete='CASCADE'),nullable=False), sa.Column('question',sa.Text,nullable=False), sa.Column('answer',sa.Text,nullable=False), sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))

def downgrade():
    op.drop_table('chat_history'); op.drop_table('integrations'); op.drop_table('document_chunks'); op.drop_table('documents'); op.drop_table('users')
