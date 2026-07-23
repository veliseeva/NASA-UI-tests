import os
import requests
import logging
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


def add_video(session_id: str):
    if not session_id:
        return

    server_ip = os.getenv('SELENOID_IP')
    if not server_ip:
        logging.warning("SELENOID_IP не задан, видео не будет сохранено.")
        return

    video_url = f"http://{server_ip}:4444/video/{session_id}.mp4"

    max_retries = 10

    for attempt in range(max_retries):
        try:
            response = requests.get(video_url, timeout=5)

            if response.status_code == 200:
                allure.attach(
                    body=response.content,
                    name=f'Video_{session_id}',
                    attachment_type=AttachmentType.MP4,
                    extension='.mp4'
                )
                return

            elif response.status_code == 404:
                import time
                time.sleep(1)

        except requests.RequestException as e:
            logging.warning(f"Попытка {attempt + 1} получить видео не удалась: {e}")
            import time
            time.sleep(1)

    logging.error(f"Не удалось скачать видео {session_id} после {max_retries} попыток.")