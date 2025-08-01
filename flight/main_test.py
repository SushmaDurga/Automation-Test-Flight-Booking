import asyncio
import random
import string
from playwright.async_api import async_playwright

def random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=6)).capitalize()

def random_email():
    return random_name().lower() + "@example.com"

def random_phone():
    return "9" + ''.join(random.choices(string.digits, k=9))

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://phptravels.net/")
        await page.screenshot(path="1_homepage.png")
        await page.click('a[href*="flights/lhe/dxb"]')
        await page.wait_for_timeout(3000)

        await page.wait_for_selector("button:has-text('Select Flight')")
        await page.screenshot(path="2_flight_list.png")
        await page.click("button:has-text('Select Flight')")
        await page.wait_for_timeout(3000)

        await page.fill('#p-first-name', random_name())
        await page.fill('#p-last-name', random_name())
        await page.fill('#p-email', random_email())
        await page.fill('#p-phone', random_phone())
        await page.fill('#p-address', "123 Main Street")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="3_personal_details_filled.png")

        await page.fill('#t-first-name-1', random_name())
        await page.fill('#t-last-name-1', random_name())
        await page.fill('#t-passport-1', "P" + ''.join(random.choices(string.digits, k=7)))
        await page.fill('#t-email-1', random_email())
        await page.fill('#t-phone-1', random_phone())
        await page.wait_for_timeout(3000)
        await page.screenshot(path="4_traveler_details_filled.png")

        await page.check('#agreechb')
        await page.wait_for_timeout(3000)
        await page.screenshot(path="5_agreement_checked.png")

        await page.click('#booking')
        await page.wait_for_timeout(3000)
        await page.screenshot(path="6_booking_confirmed.png")

        await page.wait_for_selector('#form', timeout=20000)
        await page.wait_for_timeout(30000)  
        await page.screenshot(path="7_payment_info_page.png")
        await page.click('#form')
        await page.wait_for_timeout(3000)

        await page.wait_for_selector("div.paypal-buttons", timeout=30000)
        await page.screenshot(path="8_before_paypal_click.png")
        await page.click("div.paypal-buttons")
        await page.wait_for_timeout(3000)

        pages = context.pages
        paypal_page = pages[-1] if len(pages) > 1 else page

        await paypal_page.wait_for_selector('input#email', timeout=30000)
        await paypal_page.fill('input#email', "sb-itxir5994130@personal.example.com")
        await paypal_page.click('button#btnNext')
        await paypal_page.wait_for_timeout(3000)
        await paypal_page.screenshot(path="9_paypal_email_filled.png")

        await paypal_page.wait_for_selector('input#password', timeout=30000)
        await paypal_page.fill('input#password', "testpayment")
        await paypal_page.click('button#btnLogin')
        await paypal_page.wait_for_timeout(3000)
        await paypal_page.screenshot(path="10_paypal_logged_in.png")

        await paypal_page.wait_for_selector('button[data-testid="submit-button-initial"]', timeout=30000)
        await paypal_page.click('button[data-testid="submit-button-initial"]')
        await paypal_page.wait_for_timeout(3000)
        await paypal_page.screenshot(path="11_paypal_payment_confirmed.png")

        await page.wait_for_selector('button:has-text("Download as PDF")', timeout=30000)
        await page.click('button:has-text("Download as PDF")')
        await page.wait_for_timeout(3000)
        await page.screenshot(path="12_pdf_downloaded.png")

        for i in range(0, 3000, 300):
            await page.evaluate(f"window.scrollTo(0, {i})")
            await page.wait_for_timeout(3000)

        await page.wait_for_timeout(3000)
        await browser.close()

asyncio.run(main())
