# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from pipeline.core.constants import PE
from pipeline.validators.utils import format_to_list

from pipeline_web.drawing_new.constants import MIN_LEN


def longest_path_ranker(pipeline):
    """
    @summary: 按照最长路径算法（所有叶子节点层级一样），快速初始化一种 rank
    @return:
    """
    ranks = {}

    def dfs(node):
        if node[PE.id] in ranks:
            return ranks[node[PE.id]]

        outgoing_node_ranks = []
        for flow_id in format_to_list(node[PE.outgoing]):
            flow = pipeline[PE.flows][flow_id]
            outgoing_node = pipeline['all_nodes'][flow[PE.target]]
            outgoing_node_ranks.append(dfs(outgoing_node) - MIN_LEN)

        if not outgoing_node_ranks:
            return 0
        else:
            return min(outgoing_node_ranks)

    for node_id, node in pipeline['all_nodes'].items():
        ranks[node_id] = dfs(node)

    return ranks


def slack(ranks, flow):
    """
    @summary: Returns the amount of slack for the given flow. The slack is defined as the
        difference between the length of the flow and its minimum length.
    @param ranks:
    @param flow:
    @return:
    """
    return ranks[flow[PE.target]] - ranks[flow[PE.source]] - MIN_LEN
