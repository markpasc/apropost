# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Author'
        db.create_table('apropost_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('atom_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('homepage_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('apropost', ['Author'])

        # Adding model 'Image'
        db.create_table('apropost_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('apropost', ['Image'])

        # Adding model 'Post'
        db.create_table('apropost_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('atom_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apropost.Author'], null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apropost.Image'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('in_reply_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='replies', null=True, to=orm['apropost.Post'])),
            ('conversation', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='conversation_replies', null=True, to=orm['apropost.Post'])),
            ('render_mode', self.gf('django.db.models.fields.CharField')(default='mixed', max_length=15, blank=True)),
            ('permalink_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('apropost', ['Post'])

        # Adding model 'StreamWhy'
        db.create_table('apropost_streamwhy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apropost.Author'])),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('apropost', ['StreamWhy'])

        # Adding model 'UserStream'
        db.create_table('apropost_userstream', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apropost.Post'])),
            ('display_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('why', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apropost.StreamWhy'], null=True, blank=True)),
        ))
        db.send_create_signal('apropost', ['UserStream'])


    def backwards(self, orm):
        
        # Deleting model 'Author'
        db.delete_table('apropost_author')

        # Deleting model 'Image'
        db.delete_table('apropost_image')

        # Deleting model 'Post'
        db.delete_table('apropost_post')

        # Deleting model 'StreamWhy'
        db.delete_table('apropost_streamwhy')

        # Deleting model 'UserStream'
        db.delete_table('apropost_userstream')


    models = {
        'apropost.author': {
            'Meta': {'object_name': 'Author'},
            'atom_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'homepage_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'apropost.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'apropost.post': {
            'Meta': {'object_name': 'Post'},
            'atom_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apropost.Author']", 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apropost.Image']", 'null': 'True', 'blank': 'True'}),
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conversation_replies'", 'null': 'True', 'to': "orm['apropost.Post']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['apropost.Post']"}),
            'permalink_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'render_mode': ('django.db.models.fields.CharField', [], {'default': "'mixed'", 'max_length': '15', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'apropost.streamwhy': {
            'Meta': {'object_name': 'StreamWhy'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apropost.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'apropost.userstream': {
            'Meta': {'object_name': 'UserStream'},
            'display_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apropost.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'why': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apropost.StreamWhy']", 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['apropost']
