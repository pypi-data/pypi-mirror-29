# -*- coding: utf-8 -*-
u"""
Copyright 2017 Telefónica Investigación y Desarrollo, S.A.U.
This file is part of Toolium.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import warnings
import sys


# constants
# pre-actions in feature files
ACTIONS_BEFORE_FEATURE = u'actions before the feature'
ACTIONS_BEFORE_SCENARIO = u'actions before each scenario'
ACTIONS_AFTER_SCENARIO = u'actions after each scenario'
ACTIONS_AFTER_FEATURE = u'actions after the feature'
KEYWORDS = ["Setup", "Check", "Given", "When", "Then", "And", "But"]  # prefix in steps to actions
GIVEN_PREFIX = u'Given'
SEPARATOR = u' '
TABLE_SEPARATOR = u'|'
EMPTY = u''

warnings.filterwarnings('ignore')


class Logger:
    def __init__(self, logger, show):
        """
        constructor
        :param logger: logger instance
        :param show: determine if messages are displayed by console
        """
        self.logger = logger
        self.show = show

    def warn(self, exc):
        """
        log an error message:
        :param exc: exception message
        """
        msg = 'trying to execute a step in the environment: \n' \
              '           - Exception: %s' % exc
        if self.logger is not None:
            self.logger.warn(msg)
        self.by_console('      WARN - %s' % msg)

    def debug(self, value):
        """
        log a debug message
        :param value: text to log
        """
        if self.logger is not None:
            self.logger.debug(value)

    def by_console(self, text_to_print):
        """
        print in console avoiding output buffering
        :param text_to_print: Text to print by console
        """
        if self.show:
            sys.stdout.write("%s\n" % text_to_print)
            sys.stdout.flush()


class DynamicEnvironment:
    """
    This class is useful when we would like execute generic steps: before the feature, before each scenario, after the feature or/and after each scenario.
    It is necessary to append certain lines in the environment.py:

        from common.utils.env_utils import DynamicEnvironment


        def before_all(context):
            context.dyn_env = DynamicEnvironment(logger=context.logger)


        def before_feature(context, feature):
            # ---- get all steps defined in the feature description associated to each action ----
            context.dyn_env.get_steps_from_feature_description(context, feature.description)
            # ---- actions before the feature ----
            context.dyn_env.execute_before_feature_steps(context)


        def before_scenario(context, scenario):
            # ---- actions before each scenario ----
            context.dyn_env.execute_before_scenario_steps(context)


        def after_scenario(context, scenario):
            # ---- actions after each scenario ----
            context.dyn_env.execute_after_scenario_steps(context)


        def after_feature(context, feature):
            # ---- actions after feature ----
            context.dyn_env.execute_after_feature_steps(context)
    """

    def __init__(self, **kwargs):
        """
        constructor
        :param kwargs: parameters set
        :param logger: logger instance
        :param show: determine if messages are displayed by console
        """
        logger_class = kwargs.get("logger", None)
        self.show = kwargs.get("show", True)
        self.logger = Logger(logger_class, self.show)
        self.init_actions()
        self.scenario_counter = 0

    def init_actions(self):
        """clear actions lists"""
        self.actions = {ACTIONS_BEFORE_FEATURE: [],
                        ACTIONS_BEFORE_SCENARIO: [],
                        ACTIONS_AFTER_SCENARIO: [],
                        ACTIONS_AFTER_FEATURE: []}

    def get_steps_from_feature_description(self, description):
        """
        get all steps defined in the feature description associated to each action
        :param description: feature description
        """
        self.init_actions()
        label_exists = EMPTY
        for row in description:
            if label_exists != EMPTY:
                if any(row.startswith(x) for x in KEYWORDS):
                    self.actions[label_exists].append(row)
                elif row.find(TABLE_SEPARATOR) >= 0:
                    self.actions[label_exists][-1] = "%s\n      %s" % (self.actions[label_exists][-1], row)
                else:
                    label_exists = EMPTY
            for action_label in self.actions:
                if row.lower().find(action_label) >= 0:
                    label_exists = action_label

    def __execute_steps_by_action(self, context, action):
        """
        execute a steps set by action
        :param context: It’s a clever place where you and behave can store information to share around, automatically managed by behave.
        :param action: action executed: see labels allowed above.
        """
        if len(self.actions[action]) > 0:
            if action in [ACTIONS_BEFORE_FEATURE, ACTIONS_BEFORE_SCENARIO, ACTIONS_AFTER_FEATURE]:
                self.logger.by_console('\n')
                if action == ACTIONS_BEFORE_SCENARIO:
                    self.scenario_counter += 1
                    self.logger.by_console("  ------------------ Scenario Nº: %d ------------------" % self.scenario_counter)
                self.logger.by_console('  %s:' % action)
            for item in self.actions[action]:
                try:
                    self.logger.by_console('    %s' % item)
                    context.execute_steps(u'''%s ''' % item.replace(item.split(SEPARATOR)[0], GIVEN_PREFIX))
                    self.logger.debug("step defined in pre-actions: %s" % item)
                except Exception as exc:
                    self.logger.warn(exc)

    def execute_before_feature_steps(self, context):
        """
        actions before the feature
        :param context: It’s a clever place where you and behave can store information to share around, automatically managed by behave.
        """
        self.__execute_steps_by_action(context, ACTIONS_BEFORE_FEATURE)

    def execute_before_scenario_steps(self, context):
        """
        actions before each scenario
        :param context: It’s a clever place where you and behave can store information to share around, automatically managed by behave.
        """
        self.__execute_steps_by_action(context, ACTIONS_BEFORE_SCENARIO)

    def execute_after_scenario_steps(self, context):
        """
        actions after each scenario
        :param context: It’s a clever place where you and behave can store information to share around, automatically managed by behave.
        """
        self.__execute_steps_by_action(context, ACTIONS_AFTER_SCENARIO)

    def execute_after_feature_steps(self, context):
        """
        actions after the feature
        :param context: It’s a clever place where you and behave can store information to share around, automatically managed by behave.
        """
        self.__execute_steps_by_action(context, ACTIONS_AFTER_FEATURE)
