from itsdangerous import TimedJSONWebSignatureSerializer as Serializer_
from itsdangerous import JSONWebSignatureSerializer, BadSignature, BadHeader, SignatureExpired
from config import Config
from flask import current_app, make_response

r = Config.SESSION_REDIS


class Serializer(Serializer_):

    def __init__(self, secret_key, expires_in, **kwargs):
        self.expires_in = expires_in
        super(Serializer, self).__init__(secret_key, expires_in, **kwargs)

    def make_header(self, header_fields):
        header = JSONWebSignatureSerializer.make_header(self, header_fields)
        iat = self.now()
        exp = iat + self.expires_in
        refresh_exp = iat + Config.PERMANENT_SESSION_LIFETIME
        header['iat'] = iat
        header['exp'] = exp
        header['refresh_exp'] = refresh_exp
        return header

    def loads(self, s, salt=None, return_header=False):
        payload, header = JSONWebSignatureSerializer.loads(self, s, salt, return_header=True)

        if 'exp' not in header:
            raise BadSignature("Missing expire date", payload=payload)

        int_date_error = BadHeader("Expiry date is not an IntDate", payload=payload)

        try:
            header["exp"] = int(header["exp"])
        except ValueError:
            raise int_date_error
        if header["exp"] < 0:
            raise int_date_error
        now = self.now()
        if header["exp"] < now:
            if header["refresh_exp"] < now:
                # 已经过了可刷新时间，直接抛出异常
                raise SignatureExpired(
                    "Signature expired",
                    payload=payload,
                    date_signed=self.get_issue_date(header),
                )
            else:
                # TODO 增加判断，看是否有存储在redis中，如果有存储过，表示token已经被刷新过了，直接放行即可。
                if r.get(s):
                    return payload
                pxt = header["refresh_exp"] - now
                if pxt > 0:
                    r.set(s, header["exp"], px=pxt)
                # 还在可刷新时间内
                # 生成新的token返回给前端
                serializer = Serializer(current_app.config["SECRET_KEY"], expires_in=self.expires_in)
                # 调用serializer的dumps方法将uid和type写入生成token
                token = serializer.dumps(payload)
                res = make_response()
                res.headers["Authorization"] = token
                res.set_cookie("authorization", token.decode("ascii"))
                return payload, token
        if return_header:
            return payload, header
        return payload