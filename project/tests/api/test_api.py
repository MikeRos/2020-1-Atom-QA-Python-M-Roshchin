import pytest
from sqlalchemy.exc import IntegrityError

from data.testing_data import invalid_reg_data
from exeptions import UnexpectedDBData, DBDataNotFound
from data.urls import API_URL
from db.model import User

"""Tests for app API"""


@pytest.mark.Positive
@pytest.mark.API
class TestPositiveApi:  # Positive tests
    def test_status_check(self, api_client):
        """Testing:
        that app API is up and responses correct on /status endpoint

        Steps:
        - check somehow that app is up
        - send GET http://<APP_HOST>:<APP_PORT>/status request
        - check that response is as expected

        Expected result:
        Response should be like
        Status: 200 OK
        Content-Type: application/json
        Body:
        {
            "status": "ok"
        }
        """
        api_client.get_req(API_URL)  # check that server is up
        req_resp = api_client.check_status()
        assert req_resp.status == 200 and req_resp.content_type == 'application/json' and req_resp.body == {"status": "ok"}

    def test_add_valid_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user with <username>, <password>, <email> is added after request
        Test is parametrized to check data validation

        Steps:
        - send POST http://<APP_HOST>:<APP_PORT>/api/add_user request
        with
        Content-Type: application/json
        Body:
        {
           "username": "<username>",
           "password": "<password>",
           "email": "<email>"
        }
        - check that user with <username>, <password>, <email> is added to DB
        - delete test data from DB

        Expected result:
        - Resp code 201
        - User is added to DB
        """
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is not None:
            raise UnexpectedDBData()
        adding = api_client.add_user(tst_username, tst_email, tst_password)

        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user is not None and test_user.username == tst_username and adding.status == 201

    def test_del_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user is deleted after request

        Steps:
        - add user with <username> to DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/del_user/<username> request
        - check that user with <username> is removed from DB
        - delete test data from DB

        Expected result:
        - Resp code 204
        - No user in DB with <username>
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound()
        deleting = api_client.del_user(tst_username)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        # delete test data from DB if it is still there
        if test_user is not None:
            db_session.query(User).filter_by(username=tst_username).delete()
            db_session.commit()
        assert test_user is None and deleting.status == 204

    def test_block_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user is blocked after request

        Steps:
        - add user with <username> to DB
        - check that user with <username> is not blocked
        - send GET http://<APP_HOST>:<APP_PORT>/api/block_user/<username> request
        - check that user with <username> is blocked
        - delete test data from DB

        Expected result:
        - Resp code 200
        - 'access' filed for <username> is 0
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=1))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound()
        blocking = api_client.block_user(tst_username)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 0 and blocking.status == 200

    def test_accept_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user is accepted after request

        Steps:
        - add user with <username> to DB
        - check that user with <username> is blocked
        - send GET http://<APP_HOST>:<APP_PORT>/api/accept_user/<username> request
        - check that user with <username> is accepted
        - delete test data from DB

        Expected result:
        'access' filed for <username> is 1
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=0))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound()
        accepting = api_client.accept_user(tst_username)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 1 and accepting.status == 200


@pytest.mark.Negative
@pytest.mark.API
class TestNegativeApi:  # Negative tests
    @pytest.mark.parametrize("user", invalid_reg_data)
    def test_add_invalid_user(self, api_client, db_session, user):
        """Testing:
        that user with <username>, <password>, <email> is added after request
        Test is parametrized to check data validation

        Steps:
        - send POST http://<APP_HOST>:<APP_PORT>/api/add_user request
        with
        Content-Type: application/json
        Body:
        {
           "username": "<username>",
           "password": "<password>",
           "email": "<email>"
        }
        - check that user with <username>, <password>, <email> is added to DB
        - delete test data from DB

        Expected result:
        - Resp code 400
        - No user in DB with <username>
        """
        test_user = db_session.query(User).filter_by(username=user[0]).first()
        db_session.commit()
        if test_user is not None:
            raise UnexpectedDBData()
        adding = api_client.add_user(user[0], user[1], user[2])
        test_user = db_session.query(User).filter_by(username=user[0]).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=user[0]).delete()
        db_session.commit()
        assert test_user is None and adding.status == 400

    def test_add_existing_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        that user with <username>, <password>, <email> is not added after request if user is already in DB

        Steps:
        - add user to DB
        - send POST http://<APP_HOST>:<APP_PORT>/api/add_user request
        with
        Content-Type: application/json
        Body:
        {
           "username": "<username>",
           "password": "<password>",
           "email": "<email>"
        }
        - check that user with <username>, <password>, <email> is added to DB
        - delete test data from DB

        Expected result:
        - Resp code 304
        - User is still in DB
        """
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is not None:
            raise UnexpectedDBData()
        api_client.add_user(tst_username, tst_email, tst_password)
        adding = api_client.add_user(tst_username, tst_email, tst_password)
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user is not None and test_user.username == tst_username and adding.status == 304

    def test_non_existing_endpoint(self, api_client):
        """Testing:
        trying to access non existing endpoint

        Steps:
        send GET http://<APP_HOST>:<APP_PORT>/api/some request

        Expected result:
        Resp code 404
        """
        req_resp = api_client.get_req(API_URL + 'some_endpoint')
        assert req_resp.status == 404

    # TODO parametrize to send to all urls
    def test_bad_request(self, api_client):
        """Testing:
        response to bad request (invalid symbols in username)

        Steps:
        send GET http://<APP_HOST>:<APP_PORT>/api/del_user/<bad_data> request

        Expected result:
        Resp code 400
        """
        req_resp = api_client.bad_request('a1%#%$@%%', password='pass', email='mail')
        assert req_resp.status == 400

    def test_del_non_existing_user(self, api_client, db_session, tst_username):
        """Testing:
        deleting of non existing user

        Steps:
        - check that there's no user with <username> in DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/del_user/<username> request

        Expected result:
        Resp code 404
        """
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is not None:
            raise UnexpectedDBData()
        deleting = api_client.del_user(tst_username)
        assert deleting.status == 404

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_del_other_user(self, api_client, db_session, tst_username):
        """Testing:
        deleting of other user (not the authorized)

        Steps:
        - add test users to DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/del_user/<other_user> request

        Expected result:
        - Resp code 401
        - check that <other_user> is still in DB
        """
        # TODO
        pass

    def test_block_blocked_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        blocking user that already is blocked

        Steps:
        - add user with <username> to DB
        - block user with <username>
        - send GET http://<APP_HOST>:<APP_PORT>/api/block_user/<username> request
        - check that user with <username> is still blocked
        - delete test data from DB

        Expected result:
        - Resp code 304
        - 'access' filed for <username> is 0
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=0))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound()
        blocking = api_client.block_user(tst_username)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 0 and blocking.status == 304

    def test_block_non_existing_user(self, api_client, db_session, tst_username):
        """Testing:
        blocking of non existing user

        Steps:
        - check that there's no user with <username> in DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/block_user/<username> request

        Expected result:
        Resp code 404
        """
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is not None:
            raise UnexpectedDBData()
        blocking = api_client.block_user(tst_username)
        assert blocking.status == 404

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_block_other_user(self, api_client, db_session, tst_username):
        """Testing:
        blocking of other user (not the authorized)

        Steps:
        - add test users to DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/block_user/<other_user> request

        Expected result:
        - Resp code 401
        - check that <other_user> status access is 1 in DB
        """
        # TODO
        pass

    def test_accept_accepted_user(self, api_client, db_session, tst_username, tst_email, tst_password):
        """Testing:
        accepting user that already is accepted

        Steps:
        - add user with <username> to DB
        - accept user with <username>
        - send GET http://<APP_HOST>:<APP_PORT>/api/accept_user/<username> request
        - check that user with <username> is still accepted
        - delete test data from DB

        Expected result:
        - Resp code 304
        - 'access' filed for <username> is 1
        """
        try:
            db_session.add(
                User(username=tst_username, password=tst_password, email=tst_email, access=1))
            db_session.commit()
        except IntegrityError:
            raise UnexpectedDBData()
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is None:
            raise DBDataNotFound()
        accepting = api_client.accept_user(tst_username)
        # delete test data from DB
        db_session.query(User).filter_by(username=tst_username).delete()
        db_session.commit()
        assert test_user.access == 1 and accepting.status == 304

    def test_accept_non_existing_user(self, api_client, db_session, tst_username):
        """Testing:
        accepting of non existing user

        Steps:
        - check that there's no user with <username> in DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/accept_user/<username> request

        Expected result:
        Resp code 404
        """
        test_user = db_session.query(User).filter_by(username=tst_username).first()
        db_session.commit()
        if test_user is not None:
            raise UnexpectedDBData()
        accepting = api_client.accept_user(tst_username)
        assert accepting.status == 404

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_accept_other_user(self, api_client, db_session, tst_username):
        """Testing:
        accepting of other user (not the authorized)

        Steps:
        - add test users to DB
        - send GET http://<APP_HOST>:<APP_PORT>/api/block_user/<other_user> request

        Expected result:
        - Resp code 401
        - check that <other_user> status access is 0 in DB
        """
        # TODO
        pass
