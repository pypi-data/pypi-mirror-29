# encoding: utf-8

import json
import requests
from ..config.constants import ModifierConstant
from ..config.intercept_scenarios import Modifier


def run_ad_hoc_modifier(module,
                        request=None,
                        response=None,
                        filter='',
                        override='',
                        params=''):
    """
    Runs an intercept modifier standalone

    :param module: python module object
    :param request: Supply if the request needs to be made
    :param response: Supply if the request/response object is already known
    :param filter: string
    :param override: string
    :param params: json string or an object that can be json.dumps-ed
    :return:
    """
    if not response:
        response = requests.get(request)

    if not request:
        request = response.url

    if isinstance(params, (list, dict, int, float)):
        params = json.dumps(params)

    parameters = Modifier(cfg_fn=lambda: None,
                          cfg_root=None,
                          key=None,
                          **{ModifierConstant.params: params,
                             ModifierConstant.filter: filter,
                             ModifierConstant.override: override})
    module.modify(request=request,
                  response=response,
                  parameters=parameters)

    return response
