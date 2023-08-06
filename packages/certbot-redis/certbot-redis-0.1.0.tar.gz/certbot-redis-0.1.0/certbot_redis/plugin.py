import os
import logging

import zope.interface
from acme import challenges
from certbot import interfaces
from certbot.plugins import common
from redis import Redis
from .redisurlparser import RedisUrlParser


logger = logging.getLogger(__name__)


class Authenticator(common.Plugin):
    zope.interface.implements(interfaces.IAuthenticator)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Redis Authenticator"
    @classmethod
    def add_parser_arguments(cls, add):
        add("redis-url", default=os.getenv('REDIS_URL'),
            help="redis-url url of the redis insteance you want to store your challenges in")

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self._httpd = None
        redis_url = RedisUrlParser(self.conf('redis-url'))
        self.redis_client = Redis(host=redis_url.hostname, port=redis_url.port, db=0, password=redis_url.password)


    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("")

    def get_chall_pref(self, domain):
        # pylint: disable=missing-docstring,no-self-use,unused-argument
        return [challenges.HTTP01]

    def _get_key(self, achall):   # pylint: disable=missing-docstring
        key = achall.chall.path[1:].split("/")[2]
        return key

    def perform(self, achalls):  # pylint: disable=missing-docstring
        responses = []
        for achall in achalls:
            responses.append(self._perform_single(achall))
        return responses

    def _perform_single(self, achall):
        # upload the challenge file to redis
        # then run simple http verification
        response, validation = achall.response_and_validation()

        self.redis_client.set(self._get_key(achall), validation, 10)
        if response.simple_verify(
                achall.chall, achall.domain,
                achall.account_key.public_key(), self.config.http01_port):
            return response
        else:
            logger.error(
                "Self-verify of challenge failed, authorization abandoned!")
            return None

    def cleanup(self, achalls):
        # pylint: disable=missing-docstring,no-self-use,unused-argument
        return None