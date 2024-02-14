# publix-coupon-clipper
## What
I just wanted to make it easy to get my Publix coupons because I can't be bothered to scan a QR code
at the store. I would've handled login for you and made the whole operation headless but there is
some bot detection on Publix's login portal. I had tried on the Python end Selenium, and then
Undetected Chrome, but both were detected. I then went to the Javascript side after reading some
internet discussion mentioning better success with `puppeteer` with `extra` and `stealth`. Alas,
also no dice. I'm no expert on this by any means so maybe someone will have a better idea on how to
get around it.

## How
1. Clone the repository
2. In the project root, `npm install`
3. Ensure `ts-node` is installed via `npm install -g ts-node`
4. Run `npx ts-node main.ts`
5. Login when the Chromium window pops up

## Requirements
### Javascript (node.js)
- ts-node
- puppeteer
- puppeteer-extra
- puppeteer-extra-plugin-stealth

## Future
Ideally I could get the login stuff working. Ideally it's working with Python and Undetected Chrome.
I don't really enjoy the Javascript ecosystem for stuff like this, especially since my main OS is
Windows so it can be a little quirky. It's working for me now though and hopefully does for you, so
cheers.
