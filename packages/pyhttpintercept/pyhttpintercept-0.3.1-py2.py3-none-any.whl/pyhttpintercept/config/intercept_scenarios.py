
import logging_helper
from copy import deepcopy
from configurationutil import Configuration, cfg_params, CfgItems, CfgItem
from .._metadata import __version__, __authorshort__, __module_name__
from ..resources.templates import intercept_template
from ..resources.schema import intercept_schema
from .constants import ScenarioConstant, INTERCEPT_SCENARIO_CONFIG

logging = logging_helper.setup_logging()

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

TEMPLATE = intercept_template.scenario
SCHEMA = intercept_schema.scenario


def _register_scenario_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=INTERCEPT_SCENARIO_CONFIG,
                 config_type=cfg_params.CONST.json,
                 template=TEMPLATE,
                 schema=SCHEMA)

    return cfg


class Modifier(CfgItem):

    def __init__(self,
                 **parameters):
        super(Modifier, self).__init__(**parameters)
        self.filter = self.filter.strip()  # Assume that we never want to

    @property
    def raw_items(self):
        items = self._cfg[self._cfg_root][self._key_attr]

        # Return a copy so that modifications of the retrieved do not get saved in config unless explicitly requested!
        return deepcopy(items)

    def save_changes(self):
        # TODO: Remove and check!  Why was this copied up from CfgItem?
        # This method is buggy and those bugs are fixed in the CfgItem.save_changes() method!

        updated_item = deepcopy(self.parameters)

        # remove any hidden parameters
        for k in [key for key in updated_item.keys()
                  if str(key).startswith(u'_')]:
            del updated_item[k]

        self._cfg[self._cfg_root][self._key_attr] = updated_item

    def passes_filter(self,
                      value,
                      wildcards=None,
                      case_sensitive=False):
        """
        :param value: value to check against filter (e.g. url)
        :param wildcards: A value or list of values that always match, e.g. '*'
        :param case_sensitive: Whether the checks should be case sensitive.
        :return: boolean
        """
        wildcards = (([wildcards]
                      if isinstance(wildcards, basestring)
                      else wildcards)
                     if wildcards else [])

        if not case_sensitive:
            return self.filter.lower() in value.lower() or self.filter.lower() in wildcards
        else:
            return self.filter in value or self.filter in wildcards


class Scenario(CfgItem):

    @property
    def modifiers(self):
        return [Modifier(cfg_fn=_register_scenario_config,
                         cfg_root=u'{k}.{c}.{m}'.format(k=self._cfg_root,
                                                        c=self._key_attr,
                                                        m=ScenarioConstant.modifiers),
                         key=i,
                         key_name=i) for i in range(len(self.parameters.get(u'modifiers', [])))]

    def get_active_modifiers(self):
        return [modifier for modifier in self.modifiers if modifier.active]


class Scenarios(CfgItems):

    def __init__(self):
        super(Scenarios, self).__init__(cfg_fn=_register_scenario_config,
                                        cfg_root=INTERCEPT_SCENARIO_CONFIG,
                                        key_name=ScenarioConstant.name,
                                        item_class=Scenario)
