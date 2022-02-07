from flask import Flask, url_for, session
from flask import render_template, redirect
# from authlib.integrations.flask_client import OAuth, token_update
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt

import app_config


app = Flask(__name__)
app.config.from_object('app_config')


oauth = OAuth(app)
oauth.register(name='eveonline',
               server_metadata_url='https://login.eveonline.com/.well-known/oauth-authorization-server',
               client_kwargs={
                   'scope': 'publicData',
                   'datasource': 'tranquility'
               })


# @token_update.connect_via(app)
# def on_token_update(sender, name, token, refresh_token=None, access_token=None):
#     if refresh_token:
#         item = OAuth2Token.find(name=name, refresh_token=refresh_token)
#     elif access_token:
#         item = OAuth2Token.find(name=name, access_token=access_token)
#     else:
#         return

#     item.access_token = token['access_token']
#     item.refresh_token = token.get('refresh_token')
#     item.expires_at = token['expires_at']
#     item.save()


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/sso/login')
def sso_login():
    redirect_uri = url_for('sso_callback', _external=True, _scheme='https')
    return oauth.eveonline.authorize_redirect(redirect_uri)


@app.route('/sso/callback')
def sso_callback():
    token = oauth.eveonline.authorize_access_token()

    # Find the signature key
    t_jwk_set = oauth.eveonline.fetch_jwk_set()
    jwt_signature_key = None
    for x in list(t_jwk_set.get('keys') or []):
        if x.get('kid') == 'JWT-Signature-Key':
            jwt_signature_key = x
            break

    # ESI does not (currently) offer an openid id_token.
    # Here we decode the ESI access_token that we are offered
    if jwt_signature_key:
        rval = jwt.decode(token['access_token'], jwt_signature_key)
        if rval:
            session['user'] = rval

    return redirect('/')


@app.route('/sso/logout')
def sso_logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    if app_config.DEBUG:
        app.run(port=app_config.PORT, host=app_config.HOST)
    else:
        import waitress
        waitress.serve(app, port=app_config.PORT, host=app_config.HOST)
