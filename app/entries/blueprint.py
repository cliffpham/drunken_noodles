from flask import Blueprint, redirect, render_template, request, url_for

from helpers import object_list, entry_list
from models import Entry, Category, Tag
from entries.forms import EntryForm
from app import db

entries = Blueprint('entries', __name__,
template_folder='templates')

#def entry_list(template, query, **context):
#    search = request.args.get('q')
#    if search:
#        query = query.filter(
#        (Entry.body.contains(search)) |
#        (Entry.title.contains(search)))
#    return object_list(template, query, **context)

@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)

@entries.route('/categories/')
def category_index():
    categories = Category.query.order_by(Category.name)
    return object_list('entries/category_index.html', categories)

@entries.route('/categories/<slug>/')
def category_detail(slug):
    category = Category.query.filter(Category.slug == slug).first_or_404()
    entries = category.entries.order_by(Entry.created_timestamp.desc())
    return object_list('entries/category_detail.html', entries, category=category)

@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)

@entries.route('/tags/<slug>/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return object_list('entries/tag_detail.html', entries, tag=tag)

@entries.route('/create/', methods=['GET'])
def create():
    form = EntryForm()
    return render_template('entries/create.html', form=form)

@entries.route('/create/', methods=['POST'])
def create_post():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
        else:
            return 'error'

@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)

@entries.route('/<slug>/edit/', methods=['GET'])
def edit(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    form = EntryForm(obj=entry)
    return render_template('entries/edit.html', entry=entry, form=form)

@entries.route('/<slug>/edit/', methods=['POST'])
def edit_entry(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
        else:
            return 'error'

@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == "POST":
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries.index'))
    
    return render_template('entries/delete.html', entry=entry)
