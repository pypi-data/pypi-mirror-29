"""
sentry_swift_nodestore.backend
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2017 by Phillip Couto.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import json
from time import sleep

import swiftclient

from sentry.nodestore.base import NodeStorage

class SwiftNodeStorage(NodeStorage):

    def __init__(self, container_name=None, auth_url=None, user=None, key=None,
        ttl=None, cacert=None):
        print(cacert, end='\n')
        self.conn = swiftclient.Connection(auth_url, user, key, cacert, auth_version=1)
        
        self.container = container_name
        self.ttl = ttl

    def delete(self, id):
        if self.ttl != None:
            hdrs = {
                'X-Delete-After': str(self.ttl)
            }
            self.conn.post_object(self.container, id, hdrs)
        else:
            self.conn.delete_object(self.container, id)
    def get(self, id):
        hdrs, body = self.conn.get_object(self.container, id)
        return json.loads(body)
    def set(self, id, data):
        self.conn.put_object(self.container, id, json.dumps(data))