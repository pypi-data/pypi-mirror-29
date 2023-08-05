# Copyright (c) 2013 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import warnings

import qumulo.lib.request as request

@request.request
def unconfigured(conninfo, credentials):
    method = "GET"
    uri = "/v1/unconfigured"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def list_unconfigured_nodes(conninfo, credentials):
    method = "GET"
    uri = "/v1/unconfigured/nodes/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def add_node(conninfo, credentials, node_uuids=None):
    warnings.warn(
        'This function has been deprecated in favor of cluster.add_node.',
        DeprecationWarning)

    method = "POST"
    uri = "/v1/cluster/nodes/"

    req = {
        'node_uuids': list() if node_uuids is None else list(node_uuids)
    }

    return request.rest_request(conninfo, credentials, method, uri, body=req)
