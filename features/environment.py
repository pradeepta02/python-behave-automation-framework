# -*- coding: UTF-8 -*-

import os
import yaml
import time
import glob

from utils import loggerutils
from time import strftime

from features.driverfactory import SeleniumDriverFactory
from features.support.core.elementaction import ElementAction


# ----------------------------------------------------------------------------
# before_step(context, step), after_step(context, step)
#   * These run before and after every step.
#   * The step passed in is an instance of Step.
# before_scenario(context, scenario), after_scenario(context, scenario)
#   * These run before and after each scenario is run.
#   * The scenario passed in is an instance of Scenario.
# before_feature(context, feature), after_feature(context, feature)
#   * These run before and after each feature file is exercised.
#   * The feature passed in is an instance of Feature.
# before_tag(context, tag), after_tag(context, tag)
#   * These run before and after each tag.
#   * The tag passed in is an instance of Tag
# ----------------------------------------------------------------------------


def before_all(context):
    """Set up test environment
    Create driver based on the desired capabilities provided.
    Valid desired capabilities can be 'firefox', 'chrome' or 'ie'.
    For adding new drivers add a new static method in DriverFactory class.

    :param context: Holds contextual information during the running of tests
    :return: None
    """
    context.config = None

    with open(os.getcwd() + os.path.sep + "config.yml", 'r') as ymlfile:
        context.config = yaml.load(ymlfile)

    loggerutils.setup_logging()

    loggerutils.setup_formatted_logging(context)

    # Delete log files older than the days specified in config file
    now = time.time()
    number_of_days_to_keep_log_files = int(context.config['env']['number_of_days_to_keep_log_files'])

    try:
        for f in os.listdir('logs'):
            if os.stat(os.path.join('logs', f)).st_mtime < now - number_of_days_to_keep_log_files * 86400:
                os.remove(os.path.join('logs', f))
    except Exception as e:
        context.logger.error("Unable to delete old log files! Error: %s" % e)

    # Delete old screenshots directory, junit xml reports before running the tests
    try:
        map(os.remove, glob.glob(os.getcwd() + os.path.sep + "screenshots" + os.path.sep + "*.png"))
        context.logger.info("Deleted old screenshot files")
    except Exception as e:
        context.logger.error("Unable to delete old screenshot files! Error: %s" % e)

    try:
        map(os.remove, glob.glob(os.getcwd() + os.path.sep + "reports" + os.path.sep + "*.xml"))
        context.logger.info("Deleted old xml report files")
    except Exception as e:
        context.logger.error("Unable to delete xml report files! Error: %s" % e)

    context.test_started_milli_time = int(round(time.time() * 1000))

    loggerutils.setup_unformatted_logging(context)

    context.logger.info("\n")
    context.logger.info("=============================================================================================")
    context.logger.info("TESTING STARTED AT : " + strftime("%Y-%m-%d %H:%M:%S"))
    context.logger.info("=============================================================================================")
    context.logger.info("\n")

    loggerutils.setup_formatted_logging(context)

    context.browser = context.config['env']['browser']

    # Get the appropriate driver for the browser specified in config file
    driver_factory = SeleniumDriverFactory(context.browser)

    context.driver = driver_factory.get_driver()

    # Set driver implicit timeout. Webdriver will keep polling for the element for the specified timeout
    # period.
    timeout = context.config['env']['implicit_timeout']

    context.driver.implicitly_wait(timeout)
    context.logger.info("Driver implicit timeout is set to '" + str(timeout) + "' seconds")

    context.application_url = context.config['env']['application_url']
    context.username = context.config['env']['username']
    context.password = context.config['env']['password']

    context.passed_scenarios = []
    context.failed_scenarios = []
    context.skipped_scenarios = []


def before_feature(context, feature):
    """Log starting of execution of feature
   :param context: Holds contextual information during the running of tests
   :param feature: Holds contextual information about the feature during the running of tests
   :return: None
   """
    loggerutils.setup_unformatted_logging(context)

    context.logger.info("\n")
    context.logger.info("---------------------------------------------------------------------------------------------")
    context.logger.info("STARTED EXECUTION OF FEATURE: " + str(feature.name))
    context.logger.info("Tags: " + str([str(item) for item in feature.tags]))
    context.logger.info("Filename: " + str(feature.filename))
    context.logger.info("Line: " + str(feature.line))
    context.logger.info("---------------------------------------------------------------------------------------------")

    loggerutils.setup_formatted_logging(context)


def before_scenario(context, scenario):
    """Launch browser and open application
    :param context: Holds contextual information during the running of tests
    :param scenario: Holds contextual information about scenario during the running of tests
    :return: None
    """
    loggerutils.setup_unformatted_logging(context)

    context.logger.info("\n")
    context.logger.info("---------------------------------------------------------------------------------------------")
    context.logger.info("STARTED EXECUTION OF SCENARIO: " + str(scenario.name))
    context.logger.info("Tags: " + str([str(item) for item in scenario.tags]))
    context.logger.info("Filename: " + str(scenario.filename))
    context.logger.info("Line: " + str(scenario.line))
    context.logger.info("---------------------------------------------------------------------------------------------")

    loggerutils.setup_formatted_logging(context)

    context.logger.info("Opening application url '" + context.application_url + "'")
    context.driver.get(context.application_url)
    context.driver.maximize_window()

    context.elementaction = ElementAction(context)


def after_step(context, step):
    """Save screenshot in case of test step failure
    This function runs everytime after a step is executed. Check is step passed, then just log it and return
    if step fails and step is a part of portal scenario, take the screenshot of the failure. The screenshot file name
    is scenario_name.png where spaces within step name is replaced by '_'
    example: book_a_roundtrip_ticket_2016-12-01_12-34-32.png
    :param context: Holds contextual information during the running of tests
    :param step: Holds contextual information about step during the running of tests
    :return: None
    """
    if step.status == "failed":
        context.logger.info(step.name + " : FAILED, Line: " + str(step.line))

        try:
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')

            __current_scenario_name = context.scenario.name.split("--")[0]
            __screenshot_file_name = "screenshots" + os.path.sep + __current_scenario_name.replace(" ", "_") + "_" + \
                                     strftime("%Y-%m-%d_%H-%M-%S") + '.png'

            context.driver.save_screenshot(__screenshot_file_name)
            context.logger.info("Screenshot is captured in file '" + __screenshot_file_name + "'")
        except Exception as e:
            context.logger.error("Unable to take screenshot! Error: %s" % e, exc_info=True)

    else:
        context.logger.info(step.name + " : PASSED")


def after_scenario(context, scenario):
    """Close browser and quit driver
    :param context: Holds contextual information during the running of tests
    :param scenario: Holds contextual information about scenario during the running of tests
    :return: None
    """
    loggerutils.setup_unformatted_logging(context)

    context.logger.info("\n")
    context.logger.info("---------------------------------------------------------------------------------------------")
    context.logger.info("FINISHED EXECUTION OF SCENARIO: " + str(scenario.name))
    context.logger.info("Result: " + scenario.status.upper())
    context.logger.info("Time taken: " + str("{0:.2f}".format(scenario.duration / 60)) + " mins, " +
                        str("{0:.2f}".format(scenario.duration % 60)) + " secs")
    context.logger.info("---------------------------------------------------------------------------------------------")

    loggerutils.setup_formatted_logging(context)

    if context.driver is not None:
        try:
            context.driver.close()
        except Exception as e:
            context.logger.error("Unable to close browser window! Error: %s" % e, exc_info=True)

        try:
            context.driver.quit()
        except Exception as e:
            context.logger.error("Unable to quit driver! Error: %s" % e, exc_info=True)


def after_feature(context, feature):
    """Log finished execution of feature
    :param context: Holds contextual information during the running of tests
    :param feature: Holds contextual information about feature during the running of tests
    :return: None
    """
    loggerutils.setup_unformatted_logging(context)

    context.logger.info("\n")
    context.logger.info("---------------------------------------------------------------------------------------------")
    context.logger.info("FINISHED EXECUTION OF FEATURE: " + str(feature.name))
    context.logger.info("Result: " + feature.status.upper())
    context.logger.info("Time taken: " + str("{0:.2f}".format(feature.duration / 60)) + " mins, " +
                        str("{0:.2f}".format(feature.duration % 60)) + " secs")
    context.logger.info("---------------------------------------------------------------------------------------------")

    loggerutils.setup_formatted_logging(context)


def after_all(context):
    """Log test finished
    :param context: Holds contextual information during the running of tests
    :return: None
    """
    loggerutils.setup_unformatted_logging(context)

    context.logger.info("\n")
    context.logger.info("=============================================================================================")
    context.logger.info("TESTING FINISHED AT : " + strftime("%Y-%m-%d %H:%M:%S"))
    context.logger.info("=============================================================================================")
    context.logger.info("\n")

    loggerutils.setup_formatted_logging(context)
