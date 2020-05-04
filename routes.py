import string, json, urllib.parse, datetime
from random import choice
from flask import request, redirect, abort
from app import app, db
from models import Url, Count


@app.route("/", methods=['GET', 'POST'])
def index():
    body = request.get_json()
    alias = body.get('alias')
    origin = body.get('origin')

    if request.method == 'POST' and alias is not None:
        exists = db.session.query(db.exists().where(Url.alias == alias)).scalar()
        if exists:
            return { 'code': 410, 'message': 'Alias repeat' }, 410

    if request.method == 'POST' and alias is None:
        def gen():
            chars = string.ascii_letters + string.digits
            length = 6
            alias = ''.join(choice(chars) for x in range(length))
            exists = db.session.query(db.exists().where(Url.alias == alias)).scalar()
            if not exists:
                return alias
        alias = gen()
        while alias is None:
            alias = gen()

    if request.method == 'POST' and alias is not None:
        if origin is not None:
            url = Url(alias=alias, origin=origin)
            db.session.add(url)
            db.session.commit()
        else:
            return { 'code': 400, 'message': 'Validation Failed' }, 400
    return { 'code': 200, 'message': 'ok.' }


@app.route('/<alias>')
def redirect_to_old(alias):
    new = Url.query.filter_by(alias=alias).first()
    if new is None:
        abort(404)
    else:
        new.counts += 1
        date = int(datetime.datetime.today().strftime('%Y%m%d'))
        count = Count.query.filter_by(url_id=new.id, date=date).first()
        if count is None:
            count = Count(url_id=new.id, date=date)
        else:
            count.counts += 1
        db.session.add_all([new, count])
        db.session.commit()
        return redirect(new.origin)


@app.route("/search")
def stats():

    def urlDataFormat(l, s):
        array = []
        for item in l:
            array.append({
                'alias'    : item.alias,
                'origin'   : item.origin,
                'counts'   : item.counts
            })
        if s is not None:
            return array
        return json.dumps(array)
    
    start = request.args.get('start')
    end = request.args.get('end')
    stats = []
    if start is not None and end is not None :
        l = Count.query.filter(Count.date.between(int(start), int(end))).order_by(Count.date.asc()).all()
        for item in l:
            url = Url.query.filter_by(id=item.url_id).all()
            stats.append({
                'Date': "%s-%s-%s" % (str(item.date)[0:4], str(item.date)[4:6], str(item.date)[6:8]),
                'Values': urlDataFormat(url, True)
            })
        return json.dumps(stats)
    else:
        stats = Url.query.order_by(Url.counts.desc()).limit(3).all()
        return urlDataFormat(stats)


@app.errorhandler(404)
def page_not_found(e):
    return { 'code': 404, 'message': 'Page Not Found' }, 404
