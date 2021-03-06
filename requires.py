#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class EtcdClient(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:etcd-proxy}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection_string():
            self.set_state('{relation_name}.available')

    @hook('{requires:etcd-proxy}-relation-{broken, departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def cluster_string(self):
        """
        Get the cluster string, if available, or None.
        """
        return self.get_remote('cluster_string')
