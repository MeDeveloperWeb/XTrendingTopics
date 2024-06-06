from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import zipfile
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def proxyHeadFullChrome(PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS):
    """
        Works for head full chrome but while hosting I am using headless chrome
    """
    manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%(host)s",
                port: parseInt(%(port)d)
              },
              bypassList: ["foobar.com"]
            }
          };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%(user)s",
                password: "%(pass)s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
        """ % {
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "user": PROXY_USER,
            "pass": PROXY_PASS,
        }


    pluginfile = 'extension/proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()
    #extension support is not possible in incognito mode for now
    #co.add_argument('--incognito')
    co.add_argument('--disable-gpu')
    #disable infobars
    co.add_argument('--disable-infobars')
    co.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])

    co.add_argument("--start-maximized")
    # co.add_argument("--headless")
    co.add_argument("--disable-notifications")
    co.add_argument('--no-sandbox')
    co.add_argument('--disable-dev-shm-usage')

    co.add_extension(pluginfile)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=co)
    #return the driver with added proxy configuration.
    return driver


def proxyChrome(PROXY_HOST, PROXY_PORT):

    """
    Works only after allowing the host ip in proxy mesh
    """

    options = webdriver.ChromeOptions()

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--proxy-server=http://%s:%s' % (PROXY_HOST, PROXY_PORT))

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)
    return driver

def chrome():

    """
    Works only after allowing the host ip in proxy mesh
    """

    options = webdriver.ChromeOptions()

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)
    return driver