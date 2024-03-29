import puppeteer from 'puppeteer-extra'
import StealthPlugin from 'puppeteer-extra-plugin-stealth'
import { format } from 'util'

const start_time = Date.now()

function LOG(...data: any[]) {
    let given = '';
    if (data.length == 1) {
        given = data[0]
    } else if (data.length > 1) {
        given = format(...data)
    }

    let current_time = (Date.now() - start_time) / 1000
    console.log('[%s] %s', current_time.toFixed(3), given)
}

LOG('Starting coupon clipper!')

// Create browser
puppeteer.use(StealthPlugin())

puppeteer
    .launch({headless: false, defaultViewport: null})
    .then(async browser => {
        const page = await browser.newPage()

        try {
            // Perform login, wait for user input
            LOG('Navigating to login page.')
            await page.goto('https://www.publix.com/login?redirectUrl=/savings/digital-coupons')
            LOG('Waiting for user login.')
            await page.waitForNavigation({timeout: 0})

            // Navigate to coupons
            LOG('Waiting for coupon page load.')
            await page.waitForSelector('button[data-qa-automation="back-to-top-button"]', {timeout: 0})

            // Load all the coupons
            LOG('Loading all the coupons.')
            while (1) {
                let button = await page.$('button[data-qa-automation="button-Load more"]')
                if (button) {
                    await button.click()
                } else {
                    break;
                }
            }

            // Click all the coupons
            let count = 0;
            LOG('Clicking all the coupons.')
            let buttons = await page.$$('button[data-qa-automation="button-Clip coupon"]')
            for (const button of buttons) {
                await button.click()
                count += 1
            }
            LOG('Clicked %d coupons!', count)

            await page.waitForNetworkIdle({timeout: 0})

            // Quit
            LOG('Done! Quitting browser.')
            browser.close()
        } catch (err) {
            console.error(err)
        }
    })
