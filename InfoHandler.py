import JDSeleniumSpyderling
import CSVFactory


def get_info(controller):
    """Obtains the appropriate info as described in the customization attribute"""

    custom = controller.get_custom()
    if custom["pages"] == "all":
        if custom["prices"] is True:
            JDSeleniumSpyderling.next_page()
            pass
        elif custom["titles"] is True:
            pass
    else:
        pass

