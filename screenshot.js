// executablePath, userDataDir 가져옴
require('dotenv').config(); 


// puppeteer-extra extends the functionality of Puppeteer and provides additional features.
// The StealthPlugin helps to avoid detection by websites that implement anti-bot measures.
// puppeteer.use(StealthPlugin()) applies the StealthPlugin to all Puppeteer instances.
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

// This line retrieves the second argument passed to the script and stores it in the url variable.
// The script expects the URL of the website to be provided as an argument when running it.
const url = process.argv[2];
// This line defines a timeout variable (timeout) set to 5000 milliseconds (5 seconds).
// This timeout will be used for various operations like waiting for page load and screenshots.
const timeout = 5000;

(async () => {
    const browser = await puppeteer.launch({
        ignoreDefaultArgs: ['--disable-extensions'],
        // headless: "false" specifies that the browser window should be visible.
        headless: "false",
        // executable path = chrome canary 위치, user data dir = userdata/default 위치
        executablePath: process.env.EXECUTABLE_PATH,
        userDataDir: process.env.USER_DATA_DIR,
    } );

    const page = await browser.newPage();

    await page.setViewport( {
        width: 1200,
        height: 1200,
        deviceScaleFactor: 1,
    } );

    await page.goto( url, {
        waitUntil: "domcontentloaded",
        timeout: timeout,
    } );

    await page.waitForTimeout(timeout);

    await page.screenshot({
        path: "screenshot.jpg",
        fullPage: true,
    });

    await browser.close();
})();