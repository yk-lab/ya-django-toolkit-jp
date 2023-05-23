from __future__ import annotations


class BaseAppSettings(object):
    """アプリケーション設定のベースクラス.

    このクラスを継承して、アプリケーション設定を定義する。

    例:
        app_settings.py:

        class AppSettings(BaseAppSettings):
            prefix = 'CUSTOM_APP_'

            @property
            def BASE_URL(self):
                return 'https://example.com'

            @property
            def API_KEY(self) -> str | None:
                api_key = self._setting('API_KEY', None)
                if not isinstance(api_key, str):
                    return None
                return api_key


        import sys  # noqa

        app_settings = AppSettings()
        app_settings.__name__ = __name__  # type: ignore
        sys.modules[__name__] = app_settings  # type: ignore


        呼び出し元:

        from . import app_settings

        print(app_settings.BASE_URL, app_settings.API_KEY)

    """

    prefix: str

    def _setting(self, name, dflt):
        from django.conf import settings

        getter = getattr(
            settings,
            f'{self.prefix}SETTING_GETTER',
            lambda name, dflt: getattr(settings, name, dflt),
        )
        return getter(self.prefix + name, dflt)
