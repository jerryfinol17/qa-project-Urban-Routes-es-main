## QA Project: Urban Routes E2E TestingUrban Routes Demo 
Hi there! I'm Jerry, and welcome to my first end-to-end (E2E) testing project. This is a hands-on automation suite for ***Urban Routes***, a specialized web app designed specifically for QA practice—think of it as a playground packed with as many bugs as it is features. It's raw, it's real, and it's where I cut my teeth on full-user-flow testing.

As a complete beginner at the time, this was my very first E2E effort and only my second automation project overall. The code might scream "novice," but that's part of the charm—it's a snapshot of my early journey in QA. If you're here to see polished, production-ready stuff, check out my flagship repo [Automated Testing Project](https://github.com/jerryfinol17/Automated-testing-project.git) for something more robust. Or, follow along on my [GitHub profile](https://github.com/jerryfinol17) to track my growth from newbie to (hopefully) pro. 
## Project Overview
This project automates key user flows in Urban Routes, simulating a real taxi booking experience:
- Setting up a ride with origin/destination.
- Selecting fare types (e.g., Comfort).
- Adding contact details and payment info.
- Customizing the ride (e.g., notes to driver, extras like blankets or ice cream).
- Validating the driver modal on completion.

It's built to catch those sneaky UI glitches in a controlled, buggy environment—perfect for learning how tests can break (and how to fix them!).
## Tech Stack
Python: Core scripting language.
Pytest: Testing framework for organizing and running tests.
Selenium WebDriver: Browser automation to interact with the web UI (clicks, inputs, waits).
ChromeDriver: Specific WebDriver for Chrome browser compatibility.


[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/selenium-4.35-green)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.4-orange)](https://pytest.org/)

Dependencies are listed in requirements.txt—install with pip install -r requirements.txt.

## Running the Tests 
***Quick heads-up***: You won't be able to run these tests directly from your console. The Urban Routes server is a private setup managed by Tripleten Academy, and it's only live for short windows (about 2 hours per session) with restricted access. That's the nature of academy-hosted environments—great for learning, tricky for sharing!To get a feel for it in action, check out this demo video. It walks through the tests firing off, successes, and those fun fails.bash

# If you had access (for reference):
pip install -r requirements.txt

pytest tests/ -v -s  
## Verbose mode with no capture for debugging

## Demo
Here's the video showing the tests in full swing—book a ride, add some flair, and watch the magic (and occasional chaos) unfold:Watch the E2E Tests Demo in **qa-project-Urban-Routes-es-main/Recording 2025-11-17 135624.mp4**  What's Next?This project was my gateway into E2E automation, teaching me the ropes of waits, locators, and assertions. I've come a long way since—dive into my Automated Testing Project for advanced features like Page Object Models and CI integration.Feedback welcome! Star, fork, or drop an issue if something sparks an idea. Follow my profile for more QA adventures.Hugs and happy testing!

*Built with ❤️ during my Tripleten QA bootcamp. Last updated: November 2025.*. Last updated: November 2025.

