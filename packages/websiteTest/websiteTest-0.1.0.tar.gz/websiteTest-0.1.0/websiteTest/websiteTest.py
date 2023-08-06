# -*- coding: utf-8 -*-

"""Main module."""
from .baseSelenium import BaseSelenium
from . import tools

functions = ("template, check")


def template(url, template_name, template_path):
    """ Creates a template taking a screencap from the url website """
    print("[INFO] Attempting to get URL")
    tester = BaseSelenium()
    print("[INFO] Saving template")
    tester.save_screencap(url=url, path=template_path, file_name=template_name)
    tester.close_browser()
    print("[INFO] finished")
    return True


def test(url, template_name, template_path, check_name, check_path):
    """ Takes a testing image screencap from the website and compares it with
    a previous stored template """
    print("[INFO] Attempting to get URL")
    tester = BaseSelenium()
    print("[INFO] Saving check")
    tester.save_screencap(url=url, path=check_path, file_name=check_name)
    tester.close_browser()
    print("[INFO] comparing images")
    template_path = "{}/{}.png".format(template_path, template_name)
    check_path = "{}/{}.png".format(check_path, check_name)
    result = tools.compare_images(template_path, check_path)
    if not result:
        print("[WARNING] Your website does not match with the template")
        print("[INFO] Saving differences")
        differences = tools.paint_image_difference(template_path, check_path)
        tools.save_image("differences/differences.png", differences)
        print("[INFO] Finished")
    return result


def tester(*args, **kwargs):
    """ main function to create template or check the website """
    # Required parameters
    url = kwargs["url"]
    function = kwargs["function"]
    template_name = kwargs["template_name"]

    # Optional arguments
    check_name = kwargs.get("check_name", "check")
    template_path = kwargs.get("template_path", "template")
    check_path = kwargs.get("check_path", "check")

    if function == "template":
        template(url, template_name, template_path)
        return True
    if function == "test":
        return test(url, template_name, template_path, check_name, check_path)

    print("[ERROR] your function is not valid")
    return False