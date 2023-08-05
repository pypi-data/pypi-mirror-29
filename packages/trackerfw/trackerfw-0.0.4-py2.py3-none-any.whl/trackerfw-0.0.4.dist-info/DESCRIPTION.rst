# ![Logo](extensions/firefox/icons/TrackerFW-48.svg) TrackerFw - <small>Intelligent Firewall for trackers</small>

## Installation

### Webserver

You can install TrackerFw from PyPi using `pip`:

```bash
pip install trackerfw
```

For testing you can install it locally:

```bash
git clone https://github.com/PrivacySec/TrackerFw.git
cd TrackerFw
pip install -e .
```

After this you can run the webserver using the `trackerfw` command.
There is also a systemd service file present in the project if you want to autostart the webserver.
We are working on packages for Linux and Windows.

### Browser plugin
Only the Firefox browser plugin is available at the moment but it will be ported to Google Chrome as well (which should be quite easy since they seem to use the same webExtensions API).
The first alpha version of the firefox browser plugin can be downloaded using [Github Releases](https://github.com/PrivacySec/TrackerFw/releases/).

## What?
TrackerFw is a software firewall for trackers. It includes a browser plugin which routes all traffic that invades the user its privacy to a local python server. Instead of only cancelling all bad traffic we want to make sure most (if not all) websites keep working but just don't invade your privacy.

TrackerFW **is not** an ad-blocker but a tracker-blocker. It's often used in combination with uBlock Origin.

## Why?
I was using Ghostery, uBlock, Anti Tracker Protection (Firefox) and a lot of other plugins to block trackers but over time this has a couple of disadvantages:

- Multiple plugins try to block the same traffic
- Websites broke because scripts couldn't load
- Websites could see if trackers were being blocked

With this open-source project I'm trying to solve all these problems.

## How?
The browser plugin fetches a list of URL patterns from a locally installed Python server. When a request matches one of the routes the traffic is sent through the Python server which will take further action. Apart from a static file of patterns and actions it also includes some more 'intelligent' block methods.

## Features
### Currently working
- List of URL patterns to block traffic or serve another Javascript file so that the website things the tracker is working
- Firefox browser plugin (will be ported to Google Chrome as well)
- Python aiohttp basic webserver including SSL support
- Bit.ly auto-fetcher which uses the BitLy API to fetch the final URL
- Click tracking redirector which redirects to the final URL without going through a click tracker such as google.nl/url..

### Upcoming
- Auto-update static tracker list
- Create ArchLinux, Debian, Fedora packages
- Port Firefox extension to Google Chrome
- Auto-install SSL certificate for local webserver
- Auto remove URL parts that invade privacy (UTM codes etc.)
- Add A LOT of trackers

## Support
We succesfully tested TrackerFw on Linux and Windows.
Mac Osx should be supported as well.

The webserver is written in Python, you need at least python 3.5 or higher.
We will **never** support Python 2.

