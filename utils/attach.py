import os
import allure
from allure_commons.types import AttachmentType


def add_screenshot(browser):
    try:
        png = browser.driver.get_screenshot_as_png()
        allure.attach(
            body=png,
            name='Screenshot',
            attachment_type=AttachmentType.PNG,
            extension='.png'
        )
    except Exception:
        pass


def add_logs(browser):
    try:
        log = "".join(
            f'{text}\n' for text in browser.driver.get_log(log_type='browser')
        )
        allure.attach(
            body=log,
            name='Logs',
            attachment_type=AttachmentType.TEXT,
            extension='.log'
        )
    except Exception:
        pass


def add_html(browser):
    try:
        html = browser.driver.page_source
        allure.attach(
            body=html,
            name='HTML',
            attachment_type=AttachmentType.HTML,
            extension='.html'
        )
    except Exception:
        pass


def add_video(browser):
    try:
        session_id = browser.driver.session_id
        if not session_id:
            return
        server_ip = os.getenv('SELENOID_IP')
        if not server_ip:
            return
        video_url = f"http://{server_ip}:8080/video/{session_id}.mp4"
        html = (
            "<html><body>"
            "<video width='100%' height='100%' controls autoplay>"
            f"<source src='{video_url}' type='video/mp4'>"
            "</video></body></html>"
        )

        allure.attach(
            body=html,
            name=f'video_{session_id}',
            attachment_type=AttachmentType.HTML,
            extension='.html'
        )
    except Exception:
        pass