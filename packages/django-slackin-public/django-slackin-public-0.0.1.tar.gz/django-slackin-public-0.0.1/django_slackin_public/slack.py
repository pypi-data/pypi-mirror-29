import logging

import requests

from django_slackin_public.signals import (
    email_address_already_invited,
    email_address_already_in_team,
    sent_invite_to_email_address
)

log = logging.getLogger(__name__)


class SlackError(Exception):
    pass


class SlackThrottledCall(SlackError):
    pass


class Slack(object):
    def __init__(self, token, subdomain):
        self.token = token
        self.subdomain = subdomain

    def api_request(self, api, data=None):
        data = data or {}
        url = 'https://{}.slack.com/api/{}'.format(self.subdomain, api)
        data['token'] = self.token
        response = requests.post(url, data=data)

        if response.status_code != 200:
            log.error("Slack API call failed (%s) Headers:\n%s", response.status_code, response.headers)
            exc_class = SlackThrottledCall if response.status_code == 429 else SlackError
            raise exc_class('API request failed (status: %s)' % response.status_code)

        response_dict = response.json()
        if 'error' in response_dict:
            self.raise_error(error_code=response_dict['error'], data=data)
        return response_dict

    def raise_error(self, error_code, data):
        # generic errors
        if error_code == 'not_authed':
            raise SlackError('Missing Slack token. Please contact an administrator.')
        elif error_code == 'invalid_auth':
            raise SlackError('Invalid Slack token. Please contact an administrator.')
        elif error_code == 'account_inactive':
            raise SlackError('Slack token is inactive. Please contact an administrator.')

        # invite errors
        elif error_code == 'missing_scope':
            raise SlackError('Slack token is for a non-admin user. Please contact an administrator.')
        elif error_code == 'already_invited':
            if 'email' in data:
                email_address = data['email']
                email_address_already_invited.send(sender=self.__class__, email_address=email_address)
                raise SlackError('{} has already been invited.'.format(email_address))
            else:
                raise SlackError('That email address has already been invited.')
        elif error_code == 'already_in_team':
            if 'email' in data:
                email_address = data['email']
                email_address_already_in_team.send(sender=self.__class__, email_address=email_address)
                raise SlackError('{} is already in this team.'.format(email_address))
            else:
                raise SlackError('That email address is already in this team.')
        elif error_code == 'paid_teams_only':
            raise SlackError('{} {}'.format(
                'Ultra-restricted invites are only available for paid accounts.',
                'Please contact an administrator.'))

        # default error
        else:
            raise SlackError('Unknown error: {}'.format(error_code))

    def get_team(self):
        return self.api_request('team.info')

    def get_users(self):
        return self.api_request('users.list', data={'presence': 1})

    def invite_user(self, email_address):
        data = {'email': email_address}
        response = self.api_request('users.admin.invite', data=data)
        sent_invite_to_email_address.send(sender=self.__class__, email_address=email_address)
        return response
