=====
Usage
=====

To use Website-Test in a project::

    from websiteTest.websiteTest import tester

    # Websites to check
    url = "https://jotathebest.github.io/invie-responsive/"

    # Call the available functions: template or test
    function = "template"  # Let's create a template
    template_name = "template"

    # creates the template inside the path template/template.png
    tester(url=url, function=function, template_name=template_name)

    # Let's check the website
    function = "test"
    tester(url=url, function=function, template_name=template_name)
