import random
import time
from playwright.sync_api import sync_playwright


def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


def type_like_human(page, text):
    for char in text:
        page.keyboard.insert_text(char)
        time.sleep(random.uniform(0.05, 0.15))


def click_with_mouse(page, locator):
    box = locator.bounding_box()
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    page.mouse.move(x, y, steps=10)
    time.sleep(0.5)
    page.mouse.click(x, y)


def smooth_scroll_js(page, scroll_y=500, duration=1000):
    page.evaluate(f'''
        const total = {scroll_y};
        const duration = {duration};
        const stepTime = 16;
        let current = 0;
        const step = total / (duration / stepTime);
        const scroll = () => {{
            current += step;
            window.scrollBy(0, step);
            if (current < total) {{
                setTimeout(scroll, stepTime);
            }}
        }};
        scroll();
    ''')
    time.sleep(duration / 1000 + 0.2)


def main():
    print("Starting script...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto("https://demoqa.com/text-box")
            time.sleep(2)

            print("Scrolling...")
            smooth_scroll_js(page, scroll_y=350, duration=1200)
            human_delay()

            print("Filling form fields...")

            name_input = page.locator("#userName")
            click_with_mouse(page, name_input)
            type_like_human(page, "Test User")
            human_delay()

            email_input = page.locator("#userEmail")
            click_with_mouse(page, email_input)
            type_like_human(page, "test@example.com")
            human_delay()

            curr_addr = page.locator("#currentAddress")
            click_with_mouse(page, curr_addr)
            type_like_human(page, "123 Test Street")
            human_delay()

            perm_addr = page.locator("#permanentAddress")
            click_with_mouse(page, perm_addr)
            type_like_human(page, "456 Permanent Ave")
            human_delay()

            print("Scrolling...")
            smooth_scroll_js(page, scroll_y=350, duration=1200)
            human_delay()

            print("Submitting form...")
            submit_button = page.locator("#submit")
            click_with_mouse(page, submit_button)
            human_delay()

            page.screenshot(path="final_screen.png")
            print("Form submitted and screenshot saved.")
        except Exception as e:
            print(f"Something went wrong: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
