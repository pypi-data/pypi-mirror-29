def smoke_test():
    from seaborn import LocalData
    local_data = LocalData()

    class User_Login(Endpoint):
        def post(self, username, password):
            """
            :param username: str of the username
            :param password: str of the password
            :return:         None
            """
            return self.connection.post('user/login', username=username,
                                        password=password)

    class User(Endpoint):
        login = User_Login()

    class Connection(ConnectionEndpoint):
        user = User()

    conn = Connection(base_uri='https://api.mechanicsofplay.com')

    assert conn.user.connection == conn and isinstance(conn.user, Endpoint)
    assert conn.user.login.connection == conn and isinstance(conn.user.login,
                                                             Endpoint)

    try:
        conn.user.login.post(username=local_data.username,
                             password=local_data.password)
    except Exception as e:
        if conn[-1].url == u'https://api.mechanicsofplay.com/user/' \
                           u'login?username=%s&password=%s' % (
        local_data.username,

        local_data.password):
            print(
            "Remote host is down, but connection_endpoint "
            "appears to be doing the right things")
        else:
            raise
    print(conn.cookies.keys())


if __name__ == '__main__':
    smoke_test()