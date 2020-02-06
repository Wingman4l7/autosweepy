# -*- coding: utf-8 -*-

import sys
import time
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Style
# import getpass

init(autoreset=True)

opts = Options()  # options for chromedriver
opts.add_argument("--window-size=1000,1000")  # specifies window width,height
# opts.add_argument("headless")  # runs without the browser visible

# initialize chromedriver global variable.
chromedriver = None

# global font variables
bright_green = Fore.GREEN + Style.BRIGHT
bright_yellow = Fore.YELLOW + Style.BRIGHT
bright_magenta = Fore.MAGENTA + Style.BRIGHT
bright_cyan = Fore.CYAN + Style.BRIGHT
bright_red = Fore.RED + Style.BRIGHT
bright_white = Fore.WHITE + Style.BRIGHT


def get_balance():
    global chromedriver  # use the global chromedriver variable.
    balance = chromedriver.find_element_by_class_name("test_balance-tile-currency").text
    print(bright_yellow + "Balance: %s" % balance)
    return balance


def select_payout_method():
    chromedriver.find_element_by_class_name("test_standardRadioOption").click()
    # name withdraw-fiSelectRadio looks like it would also work
    chromedriver.find_element_by_class_name("test_analyze-withdraw-submit").click()
    # chromedriver.find_element_by_name("selectFiNext").click() should also work
    # .find_element_by_link_text("Next") might also work
    print(bright_yellow + "Fee-free bank payout method selected.")


def submit_transfer_request(balance):
    global chromedriver  # use the global chromedriver variable.
    transfer_amount_field = chromedriver.find_element_by_name("js_withdrawInput")
    balance = balance[1:]  # strip $ sign from string
    transfer_amount_field.send_keys(balance)
    chromedriver.find_element_by_class_name("test_analyze-withdraw-submit").click()
    # chromedriver.find_element_by_name("review").click() should also work
    # .find_element_by_link_text("Next") might also work
    print(bright_yellow + "Transfer request successfully submitted.")


def result():
    global chromedriver  # use the global chromedriver variable.
    transfer_amt = chromedriver.find_element_by_class_name("fiActionResult-header").text
    print(bright_green + "\n %s \n to default bank account." % transfer_amt)
    chromedriver.find_element_by_class_name("test_withdraw-funds-success-done").click()  # click "Done" button
    countdown(5)


def countdown(seconds):
    # print '\n'
    for count in range(seconds, 0, -1):
        if(seconds > 3):
            print(bright_yellow + '    **** Sleeping for %d seconds...\r' % count),
            sys.stdout.flush()
        time.sleep(1)


def login(email, password):
    global chromedriver  # use the global chromedriver variable.

    print(bright_cyan + "\nLogging into PayPal...")
    email_field = chromedriver.find_element_by_name('login_email')
    email_field.send_keys(email)
    chromedriver.find_element_by_id("btnNext").click()  # Next button
    countdown(3)

    password_field = chromedriver.find_element_by_name('login_password')
    password_field.send_keys(password)
    chromedriver.find_element_by_id('btnLogin').click()  # Log In button
    countdown(3)

    # probably a cleaner way to do the conditional, like with a try / catch
    one_touch = chromedriver.find_elements_by_class_name("scTrack\\:unifiedlogin-activate-one-touch")
    if len(one_touch):
        chromedriver.find_element_by_link_text("Not now").click()
        countdown(3)  
    
    # probably a cleaner way to do the conditional, like with a try / catch
    ad_page = chromedriver.find_elements_by_link_text("Proceed to Account Overview")
    if len(ad_page):
        chromedriver.find_element_by_link_text("Proceed to Account Overview").click()
        countdown(3)

    success = chromedriver.find_elements_by_class_name("welcome-container")

    if len(success):  # element found
        print(bright_green + "Login Successful!  Continuing...")
        countdown(3)
    else:  # element not found
        print(bright_red + "Login Unsuccessful!  Exiting...")
        countdown(3)
        chromedriver.quit()
        exit(1)


def logout():
    global chromedriver  # use the global chromedriver variable.
    chromedriver.get('https://www.paypal.com/signout')
    countdown(5)

    success = chromedriver.find_elements_by_link_text("Log In")

    if len(success):  # element found
        print(bright_green + "Logout Successful!  Continuing...")
        countdown(3)
    else:  # element not found
        print(bright_red + "ERROR: Logout Unsuccessful!")
        countdown(3)


def main():
    # use the global chromedriver variable.
    global chromedriver

    chromedriver = webdriver.Chrome(executable_path='/Python27/selenium/webdriver/chromedriver', chrome_options=opts)
    chromedriver.get('https://www.paypal.com/signin?country.x=US&locale.x=en_US')

    ### parse config file with login credentials ###
    config = configparser.ConfigParser()
    config.read('autosweepy_config.ini')
    email = config.get('paypal.com', 'Email')
    password = config.get('paypal.com', 'Password')
    # print(bright_green + "Login credentials loaded from config file!")

    login(email, password)  # uses config_file

    # if check_funds(transfer_link):
    balance = get_balance()
    if balance == "$0.00":
        print (bright_yellow + "PayPal balance is zero.  Nothing to do.  Exiting!")
        logout()
    else:
        chromedriver.get('https://www.paypal.com/myaccount/money/balances/withdraw')
        countdown(5)
        select_payout_method()
        countdown(5)
        submit_transfer_request(balance)
        countdown(5)
        chromedriver.find_element_by_class_name("test_withdraw-submit").click()
        # chromedriver.find_element_by_name("submit").click() should also work
        countdown(5)
        result()
        countdown(5)
        logout()

    print(bright_cyan + "\n Exiting script!")
    chromedriver.close()  # remove if you want to visually compare console results against actual results
    exit(0)


# process main method call
if __name__ == '__main__':
    main()
