from dataclasses import dataclass, field
from selenium import webdriver
from selenium.webdriver.remote import webelement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains


BASE_URL="https://www.google.com/maps/search/{search}/@-23.9617279,-46.3392223,14z/data=!3m1!4b1?hl=en"
SEARCH="restaurantes+em+Santos"
FINAL_URL=BASE_URL.format(search=SEARCH)
IMPLICT_WAIT = 5

chrome_options = Options()
# chrome_options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver.get(FINAL_URL)
driver.implicitly_wait(IMPLICT_WAIT)

@dataclass
class Place:
    name: str
    address: str
    business_hours: dict[str, str]
    extra_attrs: dict[str, str] = field(default_factory=lambda: {})
    traits: dict[str, list[str]] = field(default_factory=lambda: {})


class Storage:
    def save(self, place: Place):
        print(place)


class GMapsPlacesCrawler:
    PLACES_PER_SCROLL = 7

    def __init__(self) -> None:
        self.storage = Storage()

    def find_elements_by_attribute(self, tag: str, attr_name: str, attr_value: str) -> list[WebElement]:
        query = f"{tag}[{attr_name}='{attr_value}']"
        elements = driver.find_elements_by_css_selector(query)
        return elements

    def find_element_by_attribute(self, tag: str, attr_name: str, attr_value: str) -> WebElement:
        return self.find_elements_by_attribute(tag, attr_name, attr_value)[0]

    def find_element_by_aria_label(self, tag: str, attr_value: str) -> WebElement:
        return self.find_element_by_attribute(tag, "aria-label", attr_value)

    def hit_back(self):
        elements = self.find_elements_by_attribute("button", "aria-label", "Back")
        for el in elements:
            if el.is_displayed():
                el.click()
                break

    def get_places_wrapper(self) -> list[WebElement]:
        search_label = SEARCH.replace("+", " ")
        wrapper = driver.find_elements_by_css_selector(f"div[aria-label='Results for {search_label}']")
        return wrapper[0].find_elements_by_xpath("*")

    def scroll_to_bottom(self, times: int):
        for _ in range(times):
            anchor_el = driver.find_element_by_class_name("section-scrollbox").find_element_by_class_name("noprint")
            ActionChains(driver).move_to_element(anchor_el).perform()

    def get_places_in_current_page(self):
        idx = 0
        while True:
            times_to_scroll = int(idx/self.PLACES_PER_SCROLL)
            self.scroll_to_bottom(times_to_scroll)

            place_divs_with_dividers = self.get_places_wrapper()
            div_idx = idx * 2
            selected_div = place_divs_with_dividers[div_idx]

            ActionChains(driver).move_to_element(selected_div).perform()
            selected_div.click()

            self.get_place_details()
            idx += 1

    def wait_restaurant_title_show(self):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text() != ""]'))
        )

    def get_place_details(self):
        self.wait_restaurant_title_show()
        restaurant_name = driver.find_elements_by_tag_name("h1")[0].text

        self.find_element_by_aria_label("img", "Hours").click()
        regions = self.find_elements_by_attribute("div", "role", "region")

        data_wrapper = regions[2]
        traits_handler = regions[1]
        direct_data_children = data_wrapper.find_elements_by_xpath("*")

        address = direct_data_children[0].text
        business_hours = self.get_business_hours(direct_data_children[1])

        place = Place(restaurant_name, address, business_hours)

        for child in direct_data_children[3:]:
            key = child.find_elements_by_tag_name("button")[0].get_attribute("aria-label")
            place.extra_attrs[key] = child.text

        traits_handler.click()
        place.traits = self.get_traits()

        self.storage.save(place)
        self.hit_back()

    def get_traits(self) -> dict[str, list[str]]:
        all_divs = driver.find_element_by_class_name("section-scrollbox").find_elements_by_xpath("*[text() != '']")
        result = {}
        for div in all_divs:
            category, *items = div.text.split("\n")
            result[category] = items

        self.hit_back()
        self.wait_restaurant_title_show()

    def get_business_hours(self, element: WebElement) -> dict[str, str]:
        all_dates_times = element.text.split("\n")[1:-1]
        return {
            all_dates_times[x] : all_dates_times[x+1]
            for x in range(0, len(all_dates_times), 2)
        }


if __name__ == "__main__":
    crawler = GMapsPlacesCrawler()
    crawler.get_places_in_current_page()
