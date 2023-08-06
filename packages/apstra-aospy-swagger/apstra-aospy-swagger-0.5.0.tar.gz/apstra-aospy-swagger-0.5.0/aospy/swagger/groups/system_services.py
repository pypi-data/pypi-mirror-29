# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/eula

# import six
# import retrying
from cached_property import cached_property
from aospy.swagger.indexer import Indexer, IndexItem


class SystemServiceItem(IndexItem):
    DEFAULT_INTERVAL = 30

    @cached_property
    def url(self):
        base_url = super(SystemServiceItem, self).url
        return base_url.format(**self.index.run_kwargs)

    def get_data(self):
        """ returns the current collector data items """
        got = self.api.get(self.url + "/data")
        if not got.ok:
            raise RuntimeError("unable to retrieve service data", self, got)

        return got.json()['items']

    def read(self):
        """ override the read method to return the current collector data """
        return self.get_data()


class SystemServices(Indexer):

    def __init__(self, aos, system):

        super(SystemServices, self).__init__(
            rqst=aos.request.systems.all_services,
            index_item_type=SystemServiceItem)

        self.run(system_id=system.id)
