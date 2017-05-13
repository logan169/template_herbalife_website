from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = 'm51ze181fsfzedplez15ze78'
SECURITY_PASSWORD_SALT='actga45zdnlqi453o545ziehqdnc464quycbi56qelncqi864lcqus'

def generate_confirmation_token(username):
    s=URLSafeTimedSerializer(SECRET_KEY)
    return s.dumps(username,salt=SECURITY_PASSWORD_SALT)

def confirm_token(token,expiration):
    s=URLSafeTimedSerializer(SECRET_KEY)
    username=s.loads(token,max_age=expiration,salt=SECURITY_PASSWORD_SALT)
    return username

