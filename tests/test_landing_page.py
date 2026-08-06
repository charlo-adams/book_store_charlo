from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001")

    h1 = page.locator("h1")
    expect(h1).to_have_text("Welcome to the Book Corner")

def test_has_image(page: Page):
    page.goto("http://127.0.0.1:5001")

    image = page.get_by_alt_text("did you talk during independent reading time")
    expect(image).to_be_visible()