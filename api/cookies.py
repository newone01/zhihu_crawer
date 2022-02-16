import time
from CookiePool.api import app
from flask.views import MethodView
from flask import request, jsonify
from CookiePool.spiders import zhihu_login
from CookiePool.database import zhihu_cookies_db
from CookiePool.utils.req_utils import get_params


class CookieAPT(MethodView):

    def get(self):
        un  = request.args.get('username')
        # 不显示
        ignore_id = {
            'id': 0
        }
        if not un:
            # 随便取一个值
            result = zhihu_cookies_db.find_one(projection=ignore_id)
        else:
            find_condition = {
                'username': un,
                'enable': 1
            }
            result = zhihu_cookies_db.find_one(find_condition, projection=ignore_id)
        data = {
            'code': 0,
            'data': result if result else {}
        }
        return jsonify(data)

    def post(self):
        un = get_params('username')
        pw = get_params('password')
        if not un or not pw:
            return jsonify({'code': 1, 'msg': 'username或password不可为空'})

        update_condition = {
            'username': un,
        }
        time_str = time.strftime('%Y-%m-%d %H:%M%S', time.localtime(time.time()))
        # 软删除
        update_data = {
            'enable': 0,
            'date': time_str,
        }
        # 以上为更新mongo数据库
        zhihu_cookies_db.update_one(update_condition, {'%set': update_data})
        # 删除成功
        return jsonify({'code': 0})

app.add_url_rule('/cookie/', view_func=CookieAPT.as_view('cookie'))