from flask import render_template, request
from models import Entry, Category, Tag

def object_list(template_name, query, paginate_by=5, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)

#def entry_list(template, query, **context):
#    search = request.args.get('q')
#    if search:
#        query = query.filter(
#        (Entry.body.contains(search)) |
#        (Entry.title.contains(search)))
#    return object_list(template, query, **context)

def entry_list(template, query, **context):
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = query.filter(Entry.status.in_(valid_statuses))
    if request.args.get('q'):
        search = request.args['q']
        query = query.filter(
            (Entry.body.contains(search)) | (Entry.title.contains(search)))
    return object_list(template, query, **context)
