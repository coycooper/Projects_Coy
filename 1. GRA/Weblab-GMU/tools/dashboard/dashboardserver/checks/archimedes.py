import os
from selenium import webdriver
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from checks import celery_app, CheckException, report, TASK_STATE
import time


def _wait_by_css(driver, css):
    max_times = 20
    times = 0
    while True:
        try:
            elem = driver.find_element_by_css_selector(css)
            if elem is not None:
                return
        except:
            times += 1
            if times > max_times:
                raise Exception("Timeout")
            time.sleep(0.5)


def read_weights(driver):
    weights = []
    weight_elements = driver.find_elements_by_xpath("//td[text()='Ball Weight']/following-sibling::td")
    for w in weight_elements:
        text = w.text
        grams = float(text.split(" ")[0])
        weights.append(grams)
    return weights


@celery_app.task(name="check.archimedes")
def check_archimedes(check_id, headless, experiment_url, user, password, msg):
    """
    This is currently not working on PhantomJS due to its use of an old Qt-related JS core which
    does not have function.Prototype.bind.
    There may be some workarounds.
    :param check_id: Identifier for the check. In this particular check, several sub-checks will be reported.
    :param headless: If True the selenium test will use PhantomJS and thus be invisible.
    :param experiment_url:
    :param user:
    :param password:
    :param msg: Msg to display for the full check.
    :return:
    """

    report(TASK_STATE.RUNNING, "%s" % (check_id), msg, "OK")

    # Initialize the driver

    if headless:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        #     "(KHTML, like Gecko) Chrome/30.0.87"
        # )
        # dcap["phantomjs.page.customHeaders"] = {
        #     "Accept-Language": "en-US,en;q=0.5"
        # }
        driver = webdriver.PhantomJS("phantomjs", desired_capabilities=dcap,
                                     service_args=["--ignore-ssl-errors=true", "--ssl-protocol=tlsv1",
                                                   "--web-security=no", "--remote-debugger-port=6500"])
    else:
        profile = FirefoxProfile()
        profile.set_preference("intl.accept_languages", "en")
        driver = webdriver.Firefox(profile)

    driver.set_window_size(1400, 1000)

    driver.implicitly_wait(30)
    base_url = experiment_url

    try:

        # Login
        driver.get("""https://weblab.deusto.es/weblab/web/webclient/""")

        time.sleep(1)

        # Find username & password fields.
        usernameField = driver.find_element_by_css_selector("input[type=text]")
        usernameField.send_keys(user)
        passwordField = driver.find_element_by_css_selector("input[type=password]")
        passwordField.send_keys(password)
        loginButton = driver.find_element_by_id("login")
        if "Log in" not in loginButton.get_attribute("value"): raise CheckException("Log in button not found")
        loginButton.click()

        time.sleep(2)

        # Go to the actual experiment
        driver.get(base_url)

        print "[We are in the experiment reserve screen]"

        archimedes = driver.find_element_by_id("reserve-free-btn")

        archimedes.click()

        # Reserve can take a long while if there is a queue.
        # Wait a while for the frame to load. For now, in seconds.
        _wait_by_css(driver, "img.arch-control")

        time.sleep(6)

        # Find all the up buttons and ensure they are disabled.
        buttons = driver.find_elements_by_css_selector("img.arch-control")

        # Wait a while before checking
        time.sleep(2)

        print "Buttons found: %d" % len(buttons)
        if len(buttons) != 4 * 7: raise CheckException("Not the expected number of buttons")

        # Check that the up buttons are all disabled
        for i in range(7):
            up = buttons[0 + i * 4]
            bn = os.path.basename(up.get_attribute("src"))
            if bn != "up.png": raise CheckException("Button is not disabled (basename: %s)" % bn)

        # Read the reported weights
        initial_weights = read_weights(driver)
        print "INITIAL WEIGHTS: %r" % initial_weights


        # Lower each ball
        for i in range(7):
            down = buttons[2 + i * 4]
            up = buttons[0 + i * 4]
            down.click()

        time.sleep(7)
        for i in range(7):
            down = buttons[2 + i * 4]
            up = buttons[0 + i * 4]

            # Check that indeed the ball was apparently lowered and raise again.
            if os.path.basename(up.get_attribute("src")) != "up_green.png": raise CheckException(
                "Up button not enabled after lowering ball (instance %d)" % i)
            if os.path.basename(down.get_attribute("src")) != "down.png": raise CheckException(
                "Down button not disabled after lowering ball (instance %d)" % i)
            up.click()

        lowered_weights = read_weights(driver)
        print "LOWERED_WEIGHTS: %r" % lowered_weights

        # Check whether they were indeed lowered right.
        evaluated_weights = []
        for i in range(len(lowered_weights)):
            w0 = initial_weights[i]
            wf = lowered_weights[i]
            r = wf / w0
            diff = w0 - wf
            if diff > 20 or r < 0.8:
                # Valid change
                evaluated_weights.append(True)
            else:
                # Something is wrong
                evaluated_weights.append(False)

        print "EVALUATED WEIGHTS: %r" % evaluated_weights

        i = 0
        for eval in evaluated_weights:
            if eval:
                result = "OK"
            else:
                result = "FAIL"

            report(TASK_STATE.FINISHED, "%s>lower-%d" % (check_id, i), "Instance %d: Lowering ball and measuring" % (i),
                   result)
            i += 1

        time.sleep(7)
        for i in range(7):
            down = buttons[2 + i * 4]
            up = buttons[0 + i * 4]
            # Check that it was re-raised properly.
            if os.path.basename(up.get_attribute("src")) != "up.png": raise CheckException(
                "Up button not disabled after raising ball again (instance %d)" % i)
            if os.path.basename(down.get_attribute("src")) != "down_green.png": raise CheckException(
                "Down button not enabled after raising ball again (instance %d)" % i)

        time.sleep(2)

        # Check whether they were raised right again.
        raised_weights = read_weights(driver)
        print "RAISED_WEIGHTS: %r" % raised_weights

        # Check whether they were indeed lowered right.
        evaluated_weights = []
        for i in range(len(lowered_weights)):
            w0 = lowered_weights[i]
            wf = raised_weights[i]
            r = w0 / wf
            diff = wf - w0
            if diff > 20 or r < 0.8:
                # Valid change
                evaluated_weights.append(True)
            else:
                # Something is wrong
                evaluated_weights.append(False)

        print "EVALUATED WEIGHTS (after raising): %r" % evaluated_weights

        i = 0
        for eval in evaluated_weights:
            if eval:
                result = "OK"
            else:
                result = "FAIL"

            report(TASK_STATE.FINISHED, "%s>raise-%d" % (check_id, i), "Instance %d: Raising ball and measuring" % (i),
                   result)
            i += 1

        print "[ARCHIMEDES]: Everything seems all right"

        report(TASK_STATE.FINISHED, "%s" % (check_id), msg, "OK")

    except:
        driver.save_screenshot("out.png")
        print "[ARCHIMEDES]: Thorough archimedes test threw an exception"
        report(TASK_STATE.FINISHED, check_id, msg, "FAIL")
        raise

    driver.close()


if __name__ == "__main__":
    url = "https://weblab.deusto.es/weblab/web/webclient/lab.html?category=Aquatic+experiments&type=js&name=archimedes"
    import config

    user = config.WEBLAB_USER
    password = config.WEBLAB_PASSWORD

    check_id = "archimedes.arch_thorough"

    check_archimedes(check_id, True, url, user, password, "Thorough archimedes test")


