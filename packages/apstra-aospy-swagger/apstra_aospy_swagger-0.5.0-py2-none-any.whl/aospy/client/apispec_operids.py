# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

import six
from inflection import singularize

API_BLUEPRINT = "/api/blueprints/{blueprint_id}"
API_PROBE = "/api/blueprints/{blueprint_id}/predefined_probes"

API_PREDEFINED_PROBE_LIST = [
    'eastwest_traffic',
    'external_ecmp_imbalance',
    'fabric_ecmp_imbalance',
    'fabric_hotcold_ifcounter',
    'fabric_interface_flapping',
    'headroom',
    'mlag_imbalance',
    'specific_hotcold_ifcounter',
    'specific_interface_flapping'
]

# This file contains "overrides" that the algoritmic approach does not presently account for.

AOS_2_1_PLATFORM_OPERIDS = {

    # version overrides

    "/api/version": {
        'get':      'get_version'
    },

    "/api/versions/api": {
        'get':      'get_api_version'
    },

    "/api/versions/build": {
        'get':      'get_build_version'
    },

    "/api/versions/server": {
        'get':      'get_server_version'
    },

    "/api/versions/device": {
        "post":     "query_device"
    },

    "/api/systems/{system_id}/configuration": {
        'get':      'get_configuration'
    },

    "/api/systems/{system_id}/services/xcvr/data": {
        "get":      "get_xcvr_data"
    },

    "/api/systems/{system_id}/services/configuration/data": {
        'get':      'get_configuration_data'
    },

    # user and aaa overrides

    "/api/aaa/check-login": {
        'post':     'query_settings_login'
    },

    "/api/aaa/check-query": {
        'post':     'query_settings'
    },

    "/api/aaa/users/{user_id}/roles": {
        'get': 'all_user_roles'
    },

    "/api/aaa/login": {
        'post':     'login'
    },

    "/api/aaa/logout": {
        'post':     'logout'
    },

    "/api/user/login": {
        'post':     'login'
    },

    "/api/user/logout": {
        "post":     'logout'
    },

    API_BLUEPRINT + "/qe": {
        'post':     'query_qe'
    },

    API_BLUEPRINT + "/ql": {
        'post':     'query_ql'
    },

    API_BLUEPRINT + "/query/arp": {
        'post':     'query_arp'
    },

    API_BLUEPRINT + "/query/mac": {
        'post':     'query_mac'
    },

    API_BLUEPRINT + "/revert": {
         "post":    'revert'
    },

    API_BLUEPRINT + "/series": {
        "post":     'get_series_data'
    }
}

AOS_2_1_REFERENCE_DESIGN_OPERIDS = {
    # Blueprint overrides

    API_BLUEPRINT + "/cabling-map": {
        'get':      'get_cabling_map'
    },

    # TODO: investigate
    API_BLUEPRINT + "/headroom-aggregations/{src_system}/{dst_system}/link_based_paths": {
        'get':      'get_headroom_aggregations_link_based_paths'
    },

    # TODO: investigate
    API_BLUEPRINT + "/headroom-aggregations/{src_system}/{dst_system}/paths": {
        'get':      'get_headroom_aggregations_paths'
    },

    API_BLUEPRINT + "/resource_groups/{resource_type}/{group_name}": {
        'put':      'set_resource_group',
        'get':      'get_resource_group'
    },
}


def patch_operation_ids(spec, operids):
    """ used to assign caller provided operationId values into a spec """

    empty_dict = {}

    for path_name, path_data in six.iteritems(spec['paths']):
        for method, method_data in six.iteritems(path_data):
            oper_id = operids.get(path_name, empty_dict).get(method)
            if oper_id:
                method_data['operationId'] = oper_id


def patch_aos_2_1_platform_operation_ids(spec):
    patch_operation_ids(spec, AOS_2_1_PLATFORM_OPERIDS)


def patch_aos_2_1_reference_design_operation_ids(spec):
    patch_operation_ids(spec, AOS_2_1_REFERENCE_DESIGN_OPERIDS)

    patch_operation_ids(spec, {
        API_PROBE + "/%s" % probe: {
            'post':     'create_probe_%s' % probe
        }
        for probe in API_PREDEFINED_PROBE_LIST
    })


operid_cmd_prefix = {
    'get': 'get',
    'delete': 'delete',
    'options': 'list',
    'post': 'create',
    'put': 'set',
    'patch': 'update'
}


def operid_as_child(path_head, _path_tail, path_spec):
    front, _, back = path_head.rpartition('/')
    item_name = singularize(back.replace('-', '_'))
    front_vars = front.count('{')

    if front_vars > 1:
        # this means that we have a composite set of variables, e.g. virtual-networks
        compose_from = front.partition('}/')[2]
        compose_from = '_'.join([word.replace('-', '_')
                                 for word in compose_from.split('/')
                                 if not word.startswith('{')])
        item_name = "%s_%s" % (compose_from, item_name)

    for cmd, cmd_spec in six.iteritems(path_spec):
        prefix = operid_cmd_prefix[cmd]
        operid = "%s_%s" % (prefix, item_name)
        cmd_spec['operationId'] = operid


def operid_as_parent(path_head, path_tail, path_spec):
    item_name = path_tail.replace('-', '_')

    if path_head.count('}') > 1:
        # this means that we have a composite set of variables, e.g. virtual-networks
        compose_from = path_head.partition('}/')[2]
        compose_from = '_'.join([word.replace('-', '_')
                                 for word in compose_from.split('/')
                                 if not word.startswith('{')])
        item_name = "%s_%s" % (compose_from, item_name)

    for cmd, cmd_spec in six.iteritems(path_spec):
        prefix = operid_cmd_prefix[cmd]
        if prefix != 'create':
            operid = "%s_%s" % ('all' if prefix == 'get' else prefix, item_name)
        else:
            operid = "%s_%s" % (prefix, singularize(item_name))
        cmd_spec['operationId'] = operid


def autoassign_path_operids(path_name, path_spec):
    head, _, tail = path_name.rpartition('/')
    set_operid = operid_as_child if tail[0] == '{' else operid_as_parent
    set_operid(head, tail, path_spec)


def autoassign_operationids(spec):
    for path_name, path_spec in six.iteritems(spec['paths']):
        autoassign_path_operids(path_name, path_spec)
