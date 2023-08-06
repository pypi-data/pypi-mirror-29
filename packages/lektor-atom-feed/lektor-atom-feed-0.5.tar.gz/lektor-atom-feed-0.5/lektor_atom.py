# -*- coding: utf-8 -*-
import sys
import hashlib
import uuid
from datetime import datetime, date
from functools import wraps
import click
import pkg_resources
from lektor.build_programs import BuildProgram
from lektor.db import F
from lektor.environment import Expression
from lektor.pluginsystem import Plugin
from lektor.context import get_ctx, url_to
from lektor.sourceobj import VirtualSourceObject
from lektor.utils import build_url

from werkzeug.contrib.atom import AtomFeed
from markupsafe import escape

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
else:
    text_type = str


class AtomFeedSource(VirtualSourceObject):
    def __init__(self, parent, feed_id, plugin):
        VirtualSourceObject.__init__(self, parent)
        self.plugin = plugin
        self.feed_id = feed_id

    @property
    def path(self):
        return self.parent.path + '@atom/' + self.feed_id

    @property
    def url_path(self):
        p = self.plugin.get_atom_config(self.feed_id, 'url_path')
        if p:
            return p

        return build_url([self.parent.url_path, self.filename])

    def __getattr__(self, item):
        try:
            return self.plugin.get_atom_config(self.feed_id, item)
        except KeyError:
            raise AttributeError(item)

    @property
    def feed_name(self):
        return self.plugin.get_atom_config(self.feed_id, 'name') or self.feed_id


def get(item, field, default=None):
    if field in item:
        return item[field]
    return default


def get_id(s):
    b = hashlib.md5(s.encode('utf-8')).digest()
    return uuid.UUID(bytes=b, version=3).urn

def fix_empty_item_title(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        s = func(*args, **kwds)
        if s is None:
            return ' '
        if s.strip() == '':
            return '  '
        return s
    return wrapper


@fix_empty_item_title
def get_item_title(item, field):
    if field in item:
        return item[field]
    return item.record_label


def get_item_body(item, field, body_template):
    if field not in item:
        raise RuntimeError('Body field %r not found in %r' % (field, item))

    if body_template:
        rv = get_ctx().env.render_template(body_template, get_ctx().pad, this=item, values={'body': item[field]})
        return text_type(rv)
    else:
        with get_ctx().changed_base_url(item.url_path):
            return text_type(escape(item[field]))


def get_item_updated(item, field):
    if field in item:
        rv = item[field]
    else:
        rv = datetime.utcnow()
    if isinstance(rv, date) and not isinstance(rv, datetime):
        rv = datetime(*rv.timetuple()[:3])
    return rv


class AtomFeedBuilderProgram(BuildProgram):
    def produce_artifacts(self):
        self.declare_artifact(
            build_url([self.source.parent.url_path, self.source.filename]),
            sources=list(self.source.iter_source_filenames()))

    def build_artifact(self, artifact):
        ctx = get_ctx()
        feed_source = self.source
        blog = feed_source.parent

        summary = get(blog, feed_source.blog_summary_field) or ''
        if hasattr(summary, '__html__'):
            subtitle_type = 'html'
            summary = text_type(summary.__html__())
        else:
            subtitle_type = 'text'
        blog_author = text_type(get(blog, feed_source.blog_author_field) or '')
        generator = ('Lektor Atom Feed Plugin',
                     'https://github.com/VaultVulp/lektor-atom',
                     pkg_resources.get_distribution('lektor-atom-feed').version)

        feed = AtomFeed(
            title=feed_source.feed_name,
            subtitle=summary,
            subtitle_type=subtitle_type,
            author=blog_author,
            feed_url=url_to(feed_source, external=True),
            url=url_to(blog, external=True),
            id=get_id(ctx.env.project.id),
            generator=generator)

        if feed_source.items:
            # "feed_source.items" is a string like "site.query('/blog')".
            expr = Expression(ctx.env, feed_source.items)
            items = expr.evaluate(ctx.pad)
        else:
            items = blog.children

        if feed_source.item_model:
            items = items.filter(F._model == feed_source.item_model)

        order_by = '-' + feed_source.item_date_field
        items = items.order_by(order_by).limit(int(feed_source.limit))

        for item in items:
            try:
                item_author_field = feed_source.item_author_field
                item_author = get(item, item_author_field) or blog_author

                feed.add(
                    get_item_title(item, feed_source.item_title_field),
                    get_item_body(item, feed_source.item_body_field, feed_source.body_template),
                    xml_base=url_to(item, external=True),
                    url=url_to(item, external=True),
                    content_type='html',
                    id=get_id(u'%s/%s' % (
                        ctx.env.project.id,
                        item['_path'].encode('utf-8'))),
                    author=item_author,
                    updated=get_item_updated(item, feed_source.item_date_field))
            except Exception as exc:
                msg = '%s: %s' % (item.path, exc)
                click.echo(click.style('E', fg='red') + ' ' + msg)

        with artifact.open('wb') as f:
            f.write(feed.to_string().encode('utf-8'))


class AtomPlugin(Plugin):
    name = u'Lektor Atom plugin'
    url_map = {}

    defaults = {
        'source_path': '/',
        'name': None,
        'url_path': None,
        'filename': 'feed.xml',
        'blog_author_field': 'author',
        'blog_summary_field': 'summary',
        'items': None,
        'limit': 50,
        'item_title_field': 'title',
        'item_body_field': 'body',
        'item_author_field': 'author',
        'item_date_field': 'pub_date',
        'item_model': None,
        'body_template': None,
    }

    def get_atom_config(self, feed_id, key):
        default_value = self.defaults[key]
        return self.get_config().get('%s.%s' % (feed_id, key), default_value)

    def on_setup_env(self, **extra):
        self.env.add_build_program(AtomFeedSource, AtomFeedBuilderProgram)

        @self.env.urlresolver
        def url_resolver(node, url_path):
            u = build_url([node.url_path] + url_path)
            return AtomPlugin.url_map.get(u)

        @self.env.virtualpathresolver('atom')
        def feed_path_resolver(node, path_segments):
            assert len(path_segments) == 1, 'Need to tell lektor_atom which feed you mean. ' \
                + 'Use @atom/$FEED_ID where $FEED_ID is a section name from configs/atom.ini'
            
            _id = path_segments[0]
            config = self.get_config()
            assert _id in config.sections(), '%r is not a valid feed id from configs/atom.ini. Valid ids are: %r' \
                 % (_id, config.sections())
            
            source_path = self.get_atom_config(_id, 'source_path')
            assert node.path == source_path, 'You tried to locate the atom feed at a different place %r than what was configured %r' \
                % (node.path, source_path)
            return AtomFeedSource(node, _id, plugin=self)
        
        @self.env.generator
        def generate_feeds(source):
            for _id in self.get_config().sections():
                if source.path == self.get_atom_config(_id, 'source_path'):
                    page = AtomFeedSource(source, _id, self)
                    AtomPlugin.url_map[page.url_path] = page
                    yield page
