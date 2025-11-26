import time
from json import loads

import allure

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count}")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена")
            if token:
                return token
            time.sleep(1)
    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    # Авторизованный клиент
    @allure.step('Авторизованный клиент')
    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)
        token: dict[str, str] = {'x-dm-auth-token': response.headers['x-dm-auth-token']}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    # Получить инфо о пользователе
    @allure.step('Получить инфо о пользователе')
    def get_account_info(
            self,
            validate_response=True
    ):
        response = self.dm_account_api.account_api.get_v1_account(validate_response=validate_response)
        return response

    # Регистрация и активация нового пользователя
    @allure.step('Регистрация и активация нового пользователя')
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login= login,
            email= email,
            password= password)

        # Регистрация пользователя
        self.dm_account_api.account_api.post_v1_account(registration=registration)
        # Активация пользователя
        start_time = time.time()
        token = self.get_token_by_login(login=login, token_type='activation')
        end_time = time.time()
        assert end_time - start_time < 3, 'Время ожидания активации превышено'
        response = self.activate_user(token=token)
        return response


    #Активация пользователя
    @allure.step('Активация пользователя')
    def activate_user(self, token: str):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response


    # Авторизация
    @allure.step('Авторизация пользователя')
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password= password,
            remember_me= remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response)
        if validate_headers:
            assert response.headers['x-dm-auth-token'], 'Токен не был получен'
        return response

    # Смена email
    @allure.step('Смена email пользователя')
    def change_email(
            self,
            login: str,
            password: str,
            email: str
    ):
        change_email = ChangeEmail(
            login=login,
            password= password,
            email= email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        return response

    # Инициализация сброса пароля
    @allure.step('Инициализация сброса пароля пользователя')
    def change_password(
            self,
            login: str,
            email: str,
            password: str,
            new_password: str
    ):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        token = self.get_token_by_login(login=login, token_type='password')
        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=password,
            new_password=new_password,
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        return response

    # Получение токена из письма
    @retrier
    @allure.step('Получение токена из письма')
    def get_token_by_login(
            self,
            login: str,
            token_type: str
    ):
        # Получение писем
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        # Получение токена
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if token_type == 'password':
                if user_login == login:
                    token = user_data['ConfirmationLinkUri'].split('/')[-1]
                    break
            if token_type == 'activation':
                if user_login == login:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                    break
        assert token is not None, f"Токен сброса пароля {login} не был получен"
        return token

    # Логаут пользователя
    @allure.step('Логаут пользователя')
    def logout_user(
            self
    ):
        self.dm_account_api.login_api.delete_v1_account_login()

    # Логаут со всех устройств
    @allure.step('Логаут со всех устройств пользователя')
    def logout_user_all(
            self
    ):
        self.dm_account_api.login_api.delete_v1_account_login_all()
