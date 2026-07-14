from selene import browser, be, command, have, by, query
from selenium.webdriver.common.keys import Keys
import re


def test_search(setup_browser):
    browser.open('/')
    browser.element('#search-input').should(be.blank).type('Orion').press_enter()
    browser.all('.container body-content').should(have.text('Results for "Orion"'))


def test_non_existent_request(setup_browser):
    browser.open('/')
    browser.element('#search-input').type('Nibiru').press_enter()
    browser.element('#search-noMatches').should(have.text('Based on your selections, no results were found.'))


def test_filter_logic(setup_browser):
    browser.open('/')
    browser.all('.mdc-checkbox__native-control').first.click()
    browser.all('.mdc-checkbox__native-control').second.click()
    browser.element('#search-input').type('Apollo').press_enter()
    results = browser.element('#search-results_container')
    results.element('.audio-asset').should(be.existing)
    results.element('.video-asset').should(be.absent)
    results.element('.image-asset').should(be.absent)


def test_sliders(setup_browser):
    browser.config.timeout = 15
    browser.open('/')
    browser.element('#search-input').type('Earth').press_enter()
    browser.element('.ngx-slider-pointer-min').click().send_keys(Keys.ARROW_RIGHT * 40)
    browser.element('.ngx-slider-pointer-max').click().send_keys(Keys.ARROW_LEFT * 56)
    browser.element('button:has(.desktop-label)').perform(command.js.click)
    browser.should(have.url_containing('1960'))
    browser.should(have.url_containing('1970'))
    img_element = browser.all('.image-asset').second.element('img').should(be.visible)
    alt_text = img_element.get(query.attribute('alt'))
    year_pattern = re.search(r'\b(196[0-9]|1970)\b', alt_text)
    assert year_pattern, f"ОШИБКА: Год не найден в alt! Текст: '{alt_text}'"


def test_downloading_link(setup_browser):
    browser.open('/')
    browser.element('#search-input').type('Mars').press_enter()
    browser.all('.video-asset').second.element('.play').perform(command.js.click)
    browser.element('#video-large-dl a').should(have.attribute('href').value_containing('images-assets.nasa.gov/video'))


def test_mobile_view(setup_browser):
    browser.driver.set_window_size(430, 932)
    browser.open('/')
    browser.element('#search-input').type('Mars').press_enter()
    browser.element('#mobile-menu').should(be.existing)
    browser.element(by.text('Filter Search Results')).should(be.existing)


def test_deep_linking(setup_browser):
    browser.open('/search?q=Orion&page=2&media=image,video,audio&yearStart=1920&yearEnd=2026')
    browser.element('#results-returned_page span').should(have.text('Displaying page 2'))
    browser.element('#results-returned h2').should(have.text('Showing results for "Orion":'))

