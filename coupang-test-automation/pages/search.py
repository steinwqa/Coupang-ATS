from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# 🚀 Selenium 감지 우회 옵션 추가
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 크롬 드라이버 실행
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # navigator.webdriver 우회

driver.get("https://www.coupang.com")
driver.maximize_window()

# 페이지가 완전히 로딩될 때까지 대기
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ 페이지 로드 완료")

time.sleep(5)

# 📌 **검색 기능 클래스 (SearchPage)**
class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    def search_item(self, keyword):
        """검색창에 키워드 입력 후 검색 버튼 클릭"""
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="headerSearchKeyword"]'))
        )
        search_button = self.driver.find_element(By.XPATH, '//*[@id="headerSearchBtn"]')

        search_bar.clear()  # 검색창 초기화
        search_bar.send_keys(keyword)  # 검색어 입력
        search_button.click()  # 검색 버튼 클릭
        print(f"✅ '{keyword}' 검색 실행")

    def wait_for_results(self):
        """검색 결과 페이지 로딩 대기"""
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="searchServiceFilter"]'))  # 왼쪽 필터 존재 확인
        )
        print("✅ 검색 결과 페이지 로드 완료")

    def click_rocket_button(self):
        """로켓배송 필터 클릭"""
        rocket_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="searchServiceFilter"]/ul/li[1]/label'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", rocket_button)  # 스크롤 이동
        time.sleep(1)
        rocket_button.click()
        print("✅ 로켓배송 필터 클릭")

    def wait_for_results(self):
        """로켓배송 필터 클릭 후 페이지 로딩 대기"""
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="searchServiceFilter"]'))  # 왼쪽 필터 존재 확인
        )
        print("✅ 검색 결과 페이지 로드 완료")

    def scroll_down(self):
        """로켓배송 필터 적용 후 스크롤 다운"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for _ in range(3):  # 3번 스크롤 (원하는 만큼 조절 가능)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 페이지 로딩 대기
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # 더 이상 스크롤할 내용이 없으면 종료
            last_height = new_height

        print("✅ 검색 결과 페이지 스크롤 완료")

#메인 페이지로 이동
driver.find_element(By.XPATH, '//*[@id="sticky-wrapper"]/section/div[1]/span').click()

time.sleep(2)


# 📌 **검색 테스트 실행**
search_test = SearchPage(driver)
search_test.search_item("노트")  # 검색 실행
search_test.wait_for_results()  # 검색 결과 페이지 로드 확인
search_test.click_rocket_button()  # 로켓 필터 클릭
search_test.scroll_down()  # 검색 결과 페이지 스크롤

# 테스트 완료 후 브라우저 닫기
driver.quit()