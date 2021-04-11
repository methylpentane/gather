# vim:set foldmethod=marker:
from django.shortcuts import render
from .models import LabMembers
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt

import json
import requests
from datetime import datetime

session = requests.Session()
user = None
gitlab = 'https://git.esslab.jp'
chat = 'https://chat.esslab.jp'
chat_me = chat + '/api/v4/users/me'

# not view {{{
def login():
    global user

    if user is None:
        user = {
            'username': settings.USERNAME,
            'password': settings.PASSWORD
        }

        r = session.get(chat + '/oauth/gitlab/login')
        csrf_token = r.text[r.text.index('csrf-token'):].split('"')[2]

        r = session.post(
            gitlab + '/users/auth/ldapmain/callback',
            cookies=r.cookies,
            data={
                'authenticity_token': csrf_token,
                'username': user['username'],
                'password': user['password']
            }
        )

        me = session.get(chat_me, cookies=r.cookies)
        _me = me.json()
        user['id'] = _me['id']

        # print('Logging in to: {}\n'.format(
        #     json.dumps(_me, indent=2)
        # ))

def get_channel():
    r = session.get(chat_me + '/teams')
    _id = r.json()[0]['id']

    target = None
    channels = session.get(chat_me + f'/teams/{_id}/channels').json()
    for channel in channels:
        if channel['display_name'] == '':
            _from, _to = channel['name'].split('__')
            if _from == _to:
                target = channel
                break

    assert target is not None

    # print('Channel info: {}\n'.format(
    #     json.dumps(target, indent=2)
    # ))

    return channel['id']


def post_msg(user_id, msg, test=True):
    time = datetime.now().strftime('%s%f')[:-3]
    channel_id = get_channel() if test else settings.CHANNEL_ID
    r = session.post(
        chat + '/api/v4/posts',
        data=json.dumps({
            'file_ids': [],
            'message': msg,
            'channel_id': channel_id,
            'pending_post_id': f'{user_id}:{time}',
            'user_id': user_id,
            'create_at': 0,
            'metadata': {},
            'props': {},
            'update_at': int(time),
        }),
        headers={
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-Token': session.cookies.get_dict()['MMCSRF'],
        }
    )
# }}}

# Create your views here.
@xframe_options_exempt
def index(request):
    member = request.GET.get('member', default=None)
    if member:
        login()
        post_msg(user['id'], f'(bot) **{member}** : "hello virtual esslab!"', settings.DEBUG)

    object_list = LabMembers.objects.all().order_by('name')
    context = {'debug': settings.DEBUG, 'object_list': object_list, 'member': member}
    return render(request, 'index.html', context)

