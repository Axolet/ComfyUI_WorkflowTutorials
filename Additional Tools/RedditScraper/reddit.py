from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import os

def scrape_comments(url, driver):
    driver.get(url)

    main_thread_content = ""
    try:
        # Scrape main thread content
        main_thread_element = driver.find_element(By.CSS_SELECTOR, 'div.thing.link div.usertext-body.may-blank-within.md-container div.md')
        main_thread_content = main_thread_element.text
    except NoSuchElementException:
        print(f"Main thread element not found on page: {url}")

    # Scroll down to load all comments
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            load_more_button = driver.find_element(By.CSS_SELECTOR, '.PrimaryComments__loadMore')
            load_more_button.click()
            time.sleep(2)
        except:
            break

    # Scrape comments
    comments = []
    comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div.thing.comment div.entry div.usertext-body.may-blank-within.md-container div.md')
    for comment_element in comment_elements:
        comment_text = comment_element.text
        comments.append(comment_text)

    return main_thread_content, comments

def main():
    thread_urls = [
        'https://old.reddit.com/r/StableDiffusion/comments/13l2tyf/why_do_you_think_midjourney_is_so_much_better/',
        'https://old.reddit.com/r/StableDiffusion/comments/11xfzc4/can_stable_diffusion_get_as_good_as_midjourney/',
        'https://old.reddit.com/r/StableDiffusion/comments/16pfivw/why_is_midjourneys_model_so_much_better_than/',
        'https://old.reddit.com/r/StableDiffusion/comments/10liqip/if_midjourney_runs_stable_diffusion_why_is_its/',
        'https://old.reddit.com/r/StableDiffusion/comments/y0hxfo/how_is_stable_diffusion_compared_to_midjourney_ai/',
        'https://old.reddit.com/r/StableDiffusion/comments/12bnazq/what_is_midjourney_doing_better_than_us/',
        'https://old.reddit.com/r/StableDiffusion/comments/1b7axxk/why_some_people_choose_midjourney_over/',
        'https://old.reddit.com/r/StableDiffusion/comments/19bfh7e/stable_diffusion_or_midjourney/',
        'https://old.reddit.com/r/StableDiffusion/comments/1027nod/is_it_just_me_or_does_anyone_get_more/',
        'https://old.reddit.com/r/StableDiffusion/comments/192buhv/i_think_stable_diffusion_is_powerful_enough_but/',
        'https://old.reddit.com/r/midjourney/comments/198pr35/gen_ai_art_tools_and_tutorials/',
        'https://old.reddit.com/r/StableDiffusion/comments/13l2tyf/why_do_you_think_midjourney_is_so_much_better/',
        'https://old.reddit.com/r/comfyui/comments/1apk7s8/as_a_fellow_beginner_i_have_to_say_this/',
        'https://old.reddit.com/r/StableDiffusion/comments/180bwrn/do_you_use_comfyui_professionally_if_so_howwhy/',
        'https://old.reddit.com/r/comfyui/comments/184uga4/how_many_of_you_are_struggling_with_comfyui/',
        'https://old.reddit.com/r/comfyui/comments/16q1tgv/time_to_adopt_comfyui/',
        'https://old.reddit.com/r/StableDiffusion/comments/1am4ibh/are_we_ever_going_to_reach_midjourney_or/',
        'https://old.reddit.com/r/StableDiffusion/comments/196r6ai/ai_beginner_help_midjourney_vs_stable_diffusion/',
        'https://old.reddit.com/r/StableDiffusion/comments/12jjvyl/why_i_pick_stablediffusion_over_midjourney_5min/'
    ]

    # Set up Selenium WebDriver (make sure you have the appropriate driver installed)
    driver = webdriver.Chrome()  # or use the appropriate driver for your browser

    data = []
    for url in thread_urls:
        main_thread_content, comments = scrape_comments(url, driver)
        data.append(main_thread_content)
        data.extend(comments)

    driver.quit()

    # Get the current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Save data to a single Excel file
    output_file_path = os.path.join(current_dir, 'reddit_data.xlsx')
    df = pd.DataFrame({'Content': data})
    df.to_excel(output_file_path, index=False)

    print(f"Scraped data from {len(thread_urls)} URLs and saved to {output_file_path}")

if __name__ == '__main__':
    main()

