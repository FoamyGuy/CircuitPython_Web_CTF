# CircuitPython Web CTF

This is a web based [capture the flag](https://en.wikipedia.org/wiki/Capture_the_flag_(cybersecurity)) exercise that is made to run on CircuitPython devices.

The excercise is intended to help bring awareness to and provide an opportunity to practice looking for common vulnerabilities within web applications. 

There are 11 flags hidden within vulnerabilites of the fictional web host LazyHosts.com. Can you find them all?

If you find all the flags feel free to submit a PR adding your nick to the [CTF_HOF.md](CTF_HOF.md) file.

The [OWASP Top 10 List](https://owasp.org/www-project-top-ten/) might be a good thing to peruse for inspiration about where to look 😉



## Installation Instructions

0. This project is made for CircuitPython on devices with built-in `wifi` core module. All testing and development was performed on a Feather ESP32-S2 TFT. It should also run on ESP32-S3, and perhaps even ESP32, and PicoW. Between the code, static web files, and libraries needed the project needs a few hundred kb of storage space. Requires [Adafruit_CircuitPython_HTTPServer](https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer)
1. Create and populate your `settings.toml` file in the root of `CIRCUITPY`. Follow the instructions here if you've not done this before: https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor/device-setup#creating-a-settings-dot-toml-file-3125968
2. Copy `code.py`, `fake_passwd`, `fake_env.env` and `ctf_statc/` to your `CIRCUITPY` drive. (Be sure to backup your existing `code.py` contents if they are important!)
3. Install the required libraries [Adafruit_CircuitPython_HTTPServer](https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer), and `EasyCrypt.py` into the `lib/` directory on your device.
4. If you connect to the serial console, or if your device has a display you should see it output a message like:

    ```Started development server on http://192.168.1.119:80```
5. Open your browser (on a PC connected to the same network as the micro-controller) and load the indicated IP in the browser. For my example it was `http://192.168.1.119/`. You don't need to include the port because `80` is the default port for http traffic.
6. If you see the home page for LazyHosts.com the fictional insecure web hosting company then you are all set to start hunting for flags!

## Flag Hunting Tips

### General Tips

The flags in this exercise are intended to be realtively basic or introductory level web vulnerabilities or failure of best practices. However every person has different levels of experience with both web application development, and penetration testing which means it could vary quite a bit from person to person on how challenging it is to find the flags.

Do not be discouraged if you're having trouble! Set it down for a while if you need to (if you're brain will allow that) and come back to it with fresh eyes.

There are a few more specific hints below hidden by a "spoiler" expander. If you feel stuck take a look at them.

Another good resource if you feel stuck is reading over the OWASP Top 10 and looking into some of the specific vulnerabilities included int he higher level categories included in the list.

Most of the flags can be found using only your browser, the view page source function, and the developer tools within the browser. If you're unfamiliar with the developer tools, this MDN write-up is a good albeit brief introduction: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/What_are_browser_developer_tools. You're encouraged to search only for things like "Browser Developer Tools" and read up, or watch videos on resources that are available.

### More Specific (Spoiler-ish)
<details>
  <summary>Slightly more specific hints (spoiler-ish)</summary>

   Flags are hidden in many places. Here are a few hints and things to look out for:
   
   - sometimes developers leave more information than they should in comments
   - hidden pages
   - headers and data sent by the server that isn't ordinarily visible directly to the user
   - elements within pages that are intended to be hidden for some users
   - weak username / password combinations
   - read the text on all the pages, it can contain hints about other things to look for
   - files that were "unintentionally" made public

</details>

### The BossFlag
The most challenging flag (The BossFlag) can technically be completed in the browser, but is perhaps easier to complete by using an additional separate tool that allows sending HTTP requests. There are many such tools available here are a few that I've used:
- Postman
- cURL
- Python Requests Library
- Insomnia
- Burp Suite 

There are lots of others search around online for "HTTP Client" if you want to find more choices. 

### Alternative Approach: Code Analysis
<details>
  <summary>Alternative Approach (spoiler-ish)</summary>
   
   The primary intended user path is to explore and inspect the web application using browsers and other web based tools. However, the CTF could be completed via alternative means by analysis of the python code and static web files to understand how the web application works and recover the flags that way.

   If you already found the flags via the web front end you could make a second attempt a while later by analyzing the code. This could add a slight bit of replay-ability to the CTF.
</details>

## Miscellaneous

### Utils

The `utils/` directory contains code and resources that don't need to be put on the `CIRCUITPY` drive under normal circumstances. They're helper utilities that I used during the creation of the CTF. Feel free to take a look if you're interested, but you might want to hold off if you haven't completed the CTF and don't want potential spoiler information.

### More CTFs?

If you enjoyed this CTF and would be interested in more or perhaps more challenging exercises feel free to reach out to me. I have a few more ideas for potential ways to hide flags, but I don't know when or if I'll get to them. Hearing from folks who enjoyed it would serve to motivate the expansion of this repo to additional CTFs.

## Credits & Thank You's

All of these entities helped in the creation of this CTF. Listed in no particular order:

- Dan Halbert for creating the initial HTTPServer library
- Michael Pokusa for many improvements to the HTTPServer library which were crucial in the making of this CTF
- Mark McGookin for publishing a helper module for AES encryption on CircuitPthon
- TryHackMe.com for the tutorials I used to learn about this material, and inspiration for the CTF
- CircuitPython Project and Community for making it so easy to build and run a project like this
- Darknet Diaries podcast for offering amazing and intriguing stories about cybersecurity and other dark corners of the web. 
- You for being interested in or attempting the CTF