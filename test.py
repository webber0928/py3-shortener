def test():
    def gen(alias):
        if alias is None:
            chars = string.ascii_letters + string.digits
            length = 6
            alias = ''.join(choice(chars) for x in range(length))
        exists = db.session.query(db.exists().where(Url.alias == alias)).scalar()
        if not exists:
            return code
    code = gen()
    while code is None:
        code = gen()
    return code

test()