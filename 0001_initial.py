"""initial schema"""
from alembic import op
import sqlalchemy as sa
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('telegram_id',sa.BigInteger(),nullable=False), sa.Column('username',sa.String(255)), sa.Column('full_name',sa.String(255),nullable=False), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now()), sa.UniqueConstraint('telegram_id'))
    op.create_index('ix_users_telegram_id','users',['telegram_id'],unique=True)
    op.create_table('organizations', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('full_name',sa.String(500),nullable=False), sa.Column('short_name',sa.String(255)), sa.Column('address',sa.String(500)), sa.Column('phone',sa.String(100)), sa.Column('email',sa.String(255)), sa.Column('website',sa.String(255)), sa.Column('stir',sa.String(50)), sa.Column('bank_details',sa.Text()), sa.Column('leader_name',sa.String(255)), sa.Column('leader_position',sa.String(255)), sa.Column('logo_path',sa.String(500)), sa.Column('default_signer',sa.String(255)), sa.Column('number_prefix',sa.String(50),nullable=False), sa.Column('reset_yearly',sa.Boolean(),nullable=False))
    op.create_table('organization_members', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('organization_id',sa.Integer(),sa.ForeignKey('organizations.id',ondelete='CASCADE'),nullable=False), sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False), sa.Column('role',sa.String(30),nullable=False), sa.UniqueConstraint('organization_id','user_id'))
    op.create_table('letters', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id'),nullable=False), sa.Column('organization_id',sa.Integer(),sa.ForeignKey('organizations.id')), sa.Column('letter_number',sa.String(100)), sa.Column('letter_type',sa.String(100),nullable=False), sa.Column('recipient',sa.String(500),nullable=False), sa.Column('recipient_person',sa.String(255)), sa.Column('recipient_position',sa.String(255)), sa.Column('subject',sa.String(500),nullable=False), sa.Column('content',sa.Text(),nullable=False), sa.Column('signer_name',sa.String(255)), sa.Column('signer_position',sa.String(255)), sa.Column('attachments',sa.Text()), sa.Column('status',sa.String(30),nullable=False), sa.Column('prompt_tokens',sa.Integer()), sa.Column('completion_tokens',sa.Integer()), sa.Column('total_tokens',sa.Integer()), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now()), sa.Column('updated_at',sa.DateTime(timezone=True),server_default=sa.func.now()), sa.UniqueConstraint('organization_id','letter_number',name='uq_org_letter_number'))
    op.create_index('ix_letters_letter_number','letters',['letter_number'])
    op.create_table('letter_versions', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('letter_id',sa.Integer(),sa.ForeignKey('letters.id',ondelete='CASCADE'),nullable=False), sa.Column('version_number',sa.Integer(),nullable=False), sa.Column('content',sa.Text(),nullable=False), sa.Column('edit_instruction',sa.Text()), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now()), sa.UniqueConstraint('letter_id','version_number'))
    op.create_table('letter_counters', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('organization_id',sa.Integer(),sa.ForeignKey('organizations.id',ondelete='CASCADE'),nullable=False), sa.Column('year',sa.Integer(),nullable=False), sa.Column('value',sa.Integer(),nullable=False), sa.UniqueConstraint('organization_id','year'))
    op.create_table('settings', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('key',sa.String(255),nullable=False,unique=True), sa.Column('value',sa.Text(),nullable=False))
    op.create_table('audit_logs', sa.Column('id',sa.Integer(),primary_key=True), sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id')), sa.Column('action',sa.String(255),nullable=False), sa.Column('details',sa.Text()), sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now()))

def downgrade():
    for t in ['audit_logs','settings','letter_counters','letter_versions','letters','organization_members','organizations','users']:
        op.drop_table(t)
