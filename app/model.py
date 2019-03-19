#!/usr/bin/python3
# import class and constants
import ssl
import json
from jsondb import Database
from ldap3 import Tls, NTLM, Connection, Server, SUBTREE, MODIFY_REPLACE
from slackclient import SlackClient

# ===============

file = open("src/config.json")
variables = json.loads(file.read())

# ===============

SLACK_BOT_TOKEN = variables['SLACK_BOT_TOKEN']          #
slack_db = "src/" + variables['slack_db']               # slack db users

db = Database(slack_db)

sc = SlackClient(SLACK_BOT_TOKEN)

# ===============


def disconnect():
    """
    Force to disconnect the ldap connection with the server.
    """
    pass


def conx(servername, domain, user, passwd):
    """
    Connection to the server
    """
    tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)

    # define the server and the connection
    s = Server(servername + "." + domain, port=636, use_ssl=True, tls=tls_configuration)
    conn = Connection(s, domain + "\\" + user, passwd, authentication=NTLM)
    conn.start_tls()
    conn.bind()

    # perform the Bind operation
    try:
        if not conn.bind():
            conn.unbind()
            raise ValueError("Invalid credentials")
    finally:
        pass

    # print("Connected")

    return conn


def search_slack_id(email):
    for users in db['members']:
        # print(users)
        if not (users['is_bot'] and users['deleted']):
            # noinspection PyBroadException
            try:
                if users['profile']['email'] == email:
                    # print(users['id'], users['profile']['email'])
                    return users['id']
            except:
                print("User with this email: " + email + " no found!!")


def search_userx(username, conn, basedn):
    """
        Verifies credentials for username and password.
        Returns True on success or False on failure
    """
    global user_dn
    SEARCHFILTER = '(&(|' \
                   '(userPrincipalName=' + username + ')' \
                                                      '(samaccountname=' + username + ')' \
                                                                                      '(mail=' + username + '))' \
                                                                                                            '(objectClass=person))'
    # SEARCHFILTER_DEFAULT = '(objectClass=person)'

    conn.search(search_base=basedn, search_filter=SEARCHFILTER,
                search_scope=SUBTREE, attributes=['cn',
                                                  'mail'], paged_size=5)
    for entry in conn.response:
        # print(entry)
        # user_dn1 = entry.get("dn")
        user_mail = entry.get("attributes")["mail"]
        if entry.get("dn") and entry.get("attributes"):
            if entry.get("attributes").get("cn"):
                user_dn = entry.get("dn")

        return user_dn, user_mail


def authenticate(servername, domain, username, password):
    """
    Verifies credentials for username and password.
    Returns True on success or False on failure
    """

    tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
    # define the server and the connection
    s = Server(servername + "." + domain, port=636, use_ssl=True, tls=tls_configuration)
    conn = Connection(s, domain + "\\" + username, password, authentication=NTLM)
    conn.start_tls()
    conn.bind()
    # print(conn.usage)
    # perform the Bind operation
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


def reset_passwd(servername, domain, user_admin, passwd_admin, basedn, username, current, new_passwd, enable):
    """
    Verifies credentials for username and password.
    Returns True on success or False on failure
    """

    conn = conx(servername, domain, user_admin, passwd_admin)
    user, email = search_userx(username, conn, basedn)

    try:
        if not authenticate(servername, domain, username, current):
            return False
        else:
            # perform the Bind operation

            enc_pwd = '"{}"'.format(new_passwd).encode('utf-16-le')

            changes = {'unicodePwd': [(MODIFY_REPLACE, [enc_pwd])]}

            x = conn.modify(user, changes=changes)

            print(x)
            # Slack Notification for the user
            if enable:
                x = search_slack_id(email)

                result = sc.api_call("chat.postMessage", channel=x,
                                     text="You password was reset! testing :) not panic :tada:", as_user=True)

                print("Result: ", result['ok'])
            else:
                pass

        # a new password is set, hashed with sha256 and a random salt
        return True

    finally:
        conn.unbind()


# =================================================
