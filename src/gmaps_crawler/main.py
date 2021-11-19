import time
from enum import IntEnum

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from gmaps_crawler.drivers import create_driver
from gmaps_crawler.entities import Place
from gmaps_crawler.storages import Storage

BASE_URL = "https://www.google.com/maps/search/{search}/@-23.9617279,-46.3392223,14z/data=!3m1!4b1?hl=en"
SEARCH = "restaurantes+em+Santos"
FINAL_URL = BASE_URL.format(search=SEARCH)

driver = create_driver()


class PlaceDetailRegion(IntEnum):
    TRAITS = 1
    ADDRESS_EXTRA = 2


class ExtraRegionChild(IntEnum):
    ADDRESS = 0
    HOURS = 1
    EXTRA_ATTRS_START = 3


def find_elements_by_attribute(tag: str, attr_name: str, attr_value: str) -> list[WebElement]:
    query = f"{tag}[{attr_name}='{attr_value}']"
    elements = driver.find_elements(By.CSS_SELECTOR, query)
    return elements


def find_element_by_attribute(tag: str, attr_name: str, attr_value: str) -> WebElement:
    return find_elements_by_attribute(tag, attr_name, attr_value)[0]


def find_element_by_aria_label(tag: str, attr_value: str) -> WebElement:
    return find_element_by_attribute(tag, "aria-label", attr_value)


class GMapsNavigator:
    PLACES_PER_SCROLL = 7
    SECONDS_BEFORE_SCROLL = 1

    def __init__(self) -> None:
        self.place_idx = 0
        self.page = 1

    def _get_places_wrapper(self) -> list[WebElement]:
        search_label = SEARCH.replace("+", " ")
        wrapper = find_element_by_aria_label("div", f"Results for {search_label}")
        return [el for el in wrapper.find_elements(By.XPATH, "*") if el.is_displayed()]

    def _scroll_to_bottom(self, times: int):
        """
        We need to scroll the list div to bottom to load the next places,
        it wouldn't work to calculate the index of a div that is not visible (loaded) yet.

        Google Maps displays 7 places at a time.
        """
        time.sleep(self.SECONDS_BEFORE_SCROLL)

        for _ in range(times):
            anchor_el = driver.find_element(By.CLASS_NAME, "section-scrollbox").find_element(By.CLASS_NAME, "noprint")
            ActionChains(driver).move_to_element(anchor_el).perform()

    def _turn_page(self):
        next_page_arrow = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next page')]")
        next_page_arrow.click()

    @property
    def has_next_place(self) -> bool:
        return True  # TODO: Find out how to decide when to turn page

    def focus_and_get_next_place_element(self) -> WebElement:
        times_to_scroll = self.place_idx // self.PLACES_PER_SCROLL
        self._scroll_to_bottom(times_to_scroll)

        place_divs_with_dividers = self._get_places_wrapper()
        div_idx = self.place_idx * 2
        selected_div = place_divs_with_dividers[div_idx]
        self.place_idx += 1

        ActionChains(driver).move_to_element(selected_div).perform()
        return selected_div

    def __iter__(self):
        return self

    def __next__(self) -> WebElement:
        if self.has_next_place:
            return self.focus_and_get_next_place_element()

        raise StopIteration()


class GMapsPlacesCrawler:
    MIN_BUSINESS_HOURS_LENGTH = 3
    WAIT_SECONDS_RESTAURANT_TITLE = 10

    def __init__(self) -> None:
        self.storage = Storage()
        self.navigator = GMapsNavigator()

    def hit_back(self):
        elements = find_elements_by_attribute("button", "aria-label", "Back")
        for el in elements:
            if el.is_displayed():
                el.click()
                break

    def get_places(self):
        for place_div in self.navigator:
            place_div.click()
            self.get_place_details()

    def wait_restaurant_title_show(self):
        WebDriverWait(driver, self.WAIT_SECONDS_RESTAURANT_TITLE).until(
            EC.presence_of_element_located((By.XPATH, '//h1[text() != ""]'))
        )

    def get_place_details(self):
        self.wait_restaurant_title_show()

        # DATA
        restaurant_name = self.get_restaurant_name()
        address = self.get_address()
        place = Place(restaurant_name, address)

        if self.expand_hours():
            place.business_hours = self.get_business_hours()

        # TRAITS
        place.extra_attrs = self.get_place_extra_attrs()
        traits_handler = self.get_region(PlaceDetailRegion.TRAITS)
        traits_handler.click()
        place.traits = self.get_traits()

        # REVIEWS
        place.rate, place.reviews = self.get_review()

        # PHOTOS
        place.photo_link = self.get_image_link()

        self.storage.save(place)
        self.hit_back()

    def get_region(self, region: PlaceDetailRegion) -> WebElement:
        """
        Regions are sections inside the place details, often:
            0: ActionButtons e.g. Directions / Save
            1: DeliveryOptions e.g. Takeway / Delivery
            2: Address
            3: Popular Times
        """
        regions = find_elements_by_attribute("div", "role", "region")
        return regions[region]

    def get_extra_region_child(self, region_child: ExtraRegionChild) -> WebElement:
        extra_region = self.get_region(PlaceDetailRegion.ADDRESS_EXTRA)
        children = extra_region.find_elements(By.XPATH, "*")
        return children[region_child]

    def expand_hours(self) -> bool:
        try:
            find_element_by_aria_label("img", "Hours").click()
        except Exception:
            # Maybe it's a "complex" view with more data:
            # driver.find_element(By.XPATH, "//*[img[contains(@src, 'schedule_gm')]]").click()
            return False
        else:
            return True

    def get_restaurant_name(self) -> str:
        return driver.find_element(By.TAG_NAME, "h1").text

    def get_address(self) -> str:
        element = self.get_extra_region_child(ExtraRegionChild.ADDRESS)
        return element.text

    def get_place_extra_attrs(self):
        """
        May contain many random attributes, some are common like:
        - web address
        - phone number
        - plus code
        """
        region = self.get_region(PlaceDetailRegion.ADDRESS_EXTRA)
        children = region.find_elements(By.XPATH, "*")

        result = {}
        for child in children[ExtraRegionChild.EXTRA_ATTRS_START :]:
            key = child.find_element(By.TAG_NAME, "button").get_attribute("aria-label")
            result[key] = child.text

        return result

    def get_review(self) -> tuple[str, str]:
        review_wrapper = driver.find_element(By.XPATH, "//div[button[contains(text(), 'review')]]")
        rate, reviews = review_wrapper.text.split("\n")
        return rate, reviews

    def get_traits(self) -> dict[str, list[str]]:
        all_divs = driver.find_element(By.CLASS_NAME, "section-scrollbox").find_elements(By.XPATH, "*[text() != '']")
        result = {}
        for div in all_divs:
            category, *items = div.text.split("\n")
            result[category] = items

        self.hit_back()
        self.wait_restaurant_title_show()
        return result

    def get_business_hours(self) -> dict[str, str]:
        element = self.get_extra_region_child(ExtraRegionChild.HOURS)

        def get_first_line(raw):
            return raw.split("\n")[0]

        all_dates_times = [
            get_first_line(x.text)
            for x in element.find_elements(By.XPATH, "//tr/*")
            if len(x.text) > self.MIN_BUSINESS_HOURS_LENGTH
        ]

        return {all_dates_times[x]: all_dates_times[x + 1] for x in range(0, len(all_dates_times), 2)}

    def get_image_link(self) -> str:
        cover_img = driver.find_element(By.XPATH, "//img[@decoding='async']")
        return cover_img.get_property("src")


if __name__ == "__main__":
    driver.get(FINAL_URL)
    crawler = GMapsPlacesCrawler()
    crawler.get_places()
