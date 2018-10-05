<h1 align="center">autoswee.py</h1>

<p align="center"><b>Automatically send all of your Paypal balance into your default linked bank account.</b></p>

<p align="center">
  <img src="https://raw.github.com/Wingman4l7/autosweepy/master/screenshot.png"/>
</p>

## About ##
I'd been selling lots of things on eBay and getting paid via PayPal, and it was annoying to have to keep logging into PayPal to withdraw my funds to my bank account.  PayPal supposedly offers a feature called "Autosweep", which will sweep any outstanding funds to your linked bank account on a regular basis.  However, accessing this feature requires contacting customer support *(if it's still available at all)* and may be restricted to US-only accounts in any case.

Since I had been recently working on browser automation projects using Selenium, this tool seemed like a naturally useful and quick practice project.

I've only found one other example of a tool like this -- dwilkie's [paypal_autosweep](https://github.com/dwilkie/paypal_autosweep) -- which is 8+ years old (so I don't know if it works anymore), and it appears to need additional setup (although it has advanced functionality like minimum balances and minimum transfer amounts that my script currently lacks).

As of my initial commit, I've been running this regularly for a couple months with no issues.  I'll likely update this repo if I notice that any website changes break the tool.

Autosweepy currently only supports a single PayPal user -- it is not intended for "commercial" use -- but it would be trivial to extend this script to support multiple user accounts via a config file modification and an additional function in the script that would iterate across the multiple logins provided.

## Installation ##
This was written for [Python 2.7.x](https://www.python.org/downloads/).

The two dependencies are `selenium` *(for browser automation)* and `colorama` *(for nice pretty colored console text that is also Windows-compatible)*.

You can use `pip` to install these dependencies from the project folder:

 - `pip install -r requirements.txt`

Tested & working on several versions of Chrome, up to 69.x.

## How to Run ##
For now, this is as simple as:

	python autoswee.py

If there are no funds that need to be withdrawn, it will output that message and complete.

It is most useful when scheduled to run via cron / Windows Task Scheduler / etc.  The way it is written, it should not leave any spawned console or browser windows open upon successful completion.

### Config File ###
Simply add in your PayPal email and password to the config file, and you should be good to go!

**WARNING:** If you clone this repo so you can use it or modify it, BE CAREFUL and DO NOT UPLOAD a commit of your config file with your PayPal email & password in it!!

## How It Works ##
This uses Selenium to hook directly into a Chrome window and seeks out elements in the page DOM so it can step through the process of automatically withdrawing the full balance of your PayPal account to the default linked bank account.

I haven't tested it with a PayPal account that has more than one bank account attached *(which I think is atypical)*; it may still work.  It also may not work properly if funds in your PayPal account are currently "on hold" -- I have not been able to test this either.

It's possible you could run this headless *(without a browser window spawning)* -- take a look at the options for a commented-out example -- but I haven't really tested this.  A quick hack that will get much the same result is to modify the spawned window dimensions to be negative values; this will place it offscreen.  Warning -- if you set the window width too small, the `logout()` function will break *(the page dynamically hides the needed link element)*.

## License ##
I haven't bothered to formally declare which license this is going to be under, but it's obviously open-source, and it will probably be some flavor of [Creative Commons](http://creativecommons.org/licenses/), or maybe [GPL](http://www.gnu.org/licenses/licenses.html).
