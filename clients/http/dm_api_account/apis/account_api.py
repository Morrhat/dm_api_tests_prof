import allure

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from clients.http.dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class AccountAPI(RestClient):

    @allure.step('Зарегистрировать нового пользователя')
    def post_v1_account(
            self,
            registration: Registration,
    ):
        """
        POST
        /v1/account
        Register new user
        :param registration:
        :return:
        """

        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    @allure.step('Получить инфо о пользователе')
    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        GET
        /v1/account
        Get current user
        :param validate_response:
        :return:
        """

        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step('Активировать токен пользователя')
    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
        PUT
        /v1/account/{token}
        Activate registered user
        :param validate_response:
        :param token:
        :return:
        """

        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Изменить email пользователя')
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response=True
    ):
        """
        PUT
        /v1/account/email
        Change registered user email
        :param validate_response:
        :param change_email:
        :return:
        """

        headers = {
            'accept': 'text/plain'
        }
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True),
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Инициировать сброс пароля пользователя')
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response=True
    ):
        """
        POST
        /v1/account/password
        Reset registered user password
        :param validate_response:
        :param reset_password:
        :return:
        """

        headers = {
            'accept': 'text/plain'
        }
        response = self.post(
            path=f'/v1/account/password',
            headers=headers,
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Изменить пароль пользователя')
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response=True
    ):
        """
        PUT
        /v1/account/password
        Change registered user password
        :param validate_response:
        :param change_password:
        :return:
        """

        headers = {
            'accept': 'text/plain'
        }
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
