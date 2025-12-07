# publix-coupon-clipper
## What
I just wanted to make it easy to get my Publix coupons because I can't be bothered to scan a QR code at the store. There
are two approaches in this repo:
1. Python (preferred) using Selenium
2. Javascript (legacy) using Puppeteer.

## How
### Python
1. (preferably in a venv) `python -m pip install -r requirements.txt`
2. `python main.py`
3. Update the generated `config.json` with your Publix login information
4. `python main.py`
5. Hopefully save some money, times are hard out there.

### Javascript (node.js)
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
### Python
- Check `requirements.txt`

## Future
I may delete the JavaScript code now that the Python solution is working.
