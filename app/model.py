import ssl
import json
from jsondb import Database
from ldap3 import Tls, NTLM, Connection, Server, SUBTREE, MODIFY_REPLACE

file = open("src/config.json")
variables = json.loads(file.read())


def conx(domain, user, passwd):
    tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
    s = Server(domain, port=636, use_ssl=True, tls=tls_configuration)
    conn = Connection(s, domain + "\\" + user, passwd, authentication=NTLM)
    conn.start_tls()
    conn.bind()

    return conn


def search_userx(username, conn, basedn):
    search_filter = '(&(|' \
                    f'(userPrincipalName={username})' \
                    f'(samaccountname={username})' \
                    f'(mail={username}))' \
                    '(objectClass=person))'

    conn.search(search_base=basedn, search_filter=search_filter,
                search_scope=SUBTREE, attributes=['cn', 'mail'], paged_size=5)

    for entry in conn.response:
        if entry.get('dn') and entry.get('attributes'):
            user_dn = entry.get('dn')
            user_mail = entry.get('attributes').get('mail')
            return user_dn, user_mail


def authenticate(domain, username, password):
    tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
    s = Server(domain, port=636, use_ssl=True, tls=tls_configuration)
    conn = Connection(s, domain + "\\" + username, password, authentication=NTLM)
    conn.start_tls()
    conn.bind()
    try:
        if not conn.bind():
            print("Not Connected")
            conn.unbind()
            return False
        else:
            print("Connected")
            conn.unbind()
            return True
    finally:
        pass


def reset_passwd(domain, user_admin, passwd_admin, basedn, username, current, new_passwd):
    conn = conx(domain, user_admin, passwd_admin)
    user_dn, email = search_userx(username, conn, basedn)

    if not authenticate(domain, username, current):
        return False

    enc_pwd = f'"{new_passwd}"'.encode('utf-16-le')
    changes = {'unicodePwd': [(MODIFY_REPLACE, [enc_pwd])]}

    conn.modify(user_dn, changes=changes)

    return True
