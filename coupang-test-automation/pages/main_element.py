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

# 요소가 화면에 나타날 때까지 스크롤 이동하는 함수
def scroll_to_element(xpath=None, css=None):
    try:
        element = None
        if xpath:
            element = driver.find_element(By.XPATH, xpath)
        elif css:
            element = driver.find_element(By.CSS_SELECTOR, css)

        if element:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)  # 스크롤 후 2초 대기
    except NoSuchElementException:
        print(f"⚠️ 스크롤 실패: 요소 없음 - {xpath if xpath else css}")

# 요소 검증 함수 (XPATH → CSS_SELECTOR 순으로 실행)
def verify_element(xpath=None, css=None, description=""):
    try:
        scroll_to_element(xpath, css)  # 요소가 화면에 나타날 수 있도록 스크롤 이동
        wait = WebDriverWait(driver, 20)  # 최대 20초 대기
        element = None

        # XPATH로 먼저 찾고, 실패하면 CSS Selector로 찾기
        if xpath:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if not element and css:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        
        assert element.is_displayed(), f"❌ 요소가 보이지 않습니다: {description}"
        print(f"✅ 요소 확인 성공: {description}")
    except NoSuchElementException:
        print(f"❌ 요소 없음: {description}")
        driver.save_screenshot(f"{description.replace(' ', '_')}_error.png")  # 오류 시 스크린샷 저장
    except Exception as e:
        print(f"⚠️ 오류 발생: {description} - {e}")

# 요소 리스트 (XPATH & CSS Selector)
elements_to_check = [
    {"xpath": '//*[@id="subscribeHeader"]/li[1]/a', "css": "#subscribeHeader > li:nth-child(1) > a", "description": "즐겨찾기 버튼"},
    {"xpath": '//*[@id="subscribeHeader"]/li[2]/a', "css": "#subscribeHeader > li:nth-child(2) > a", "description": "입점신청 버튼"},
    {"xpath": '//*[@id="login"]/a', "css": "#login > a", "description": "로그인 버튼"},
    {"xpath": '//*[@id="join"]/a', "css": "#join > a", "description": "회원가입 버튼"},
    {"xpath": '//*[@id="headerMenu"]/li[3]/a', "css": "#headerMenu > li:nth-child(3) > a", "description": "고객센터"},
    {"xpath": '//*[@id="vendor-login-improveC"]/a', "css": "#vendor-login-improveC > a", "description": "판매자 가입"},
    {"xpath": '//*[@id="header"]/div', "css": "#header > div", "description": "카테고리 버튼"},
    {"xpath": '//*[@id="header"]/section/div[1]/span', "css": "#header > section > div:nth-child(1) > span", "description": "쿠팡 로고"},
    {"xpath": '//*[@id="header"]/section/div[1]/div', "css": "#header > section > div:nth-child(1) > div", "description": "검색 옵션바"},
    {"xpath": '//*[@id="headerSearchKeyword"]', "css": "#headerSearchKeyword", "description": "검색 바"},
    {"xpath": '//*[@id="headerSearchForm"]/fieldset/div/a', "css": "#headerSearchForm > fieldset > div > a", "description": "검색 바 음성검색"},
    {"xpath": '//*[@id="headerSearchBtn"]', "css": "#headerSearchBtn", "description": "검색 버튼"},
    {"xpath": '//*[@id="header"]/section/div[1]/ul/li[1]/a', "css": "#header > section > div:nth-child(1) > ul > li:nth-child(1) > a", "description": "마이쿠팡"},
    {"xpath": '//*[@id="header"]/section/div[1]/ul/li[2]/a', "css": "#header > section > div:nth-child(1) > ul > li:nth-child(2) > a", "description": "장바구니"},
    {"xpath": '//*[@id="gnb-menu-container"]', "css": "#gnb-menu-container", "description": "메인카테고리 메뉴레이어"},
    {"xpath": '//*[@id="todaysHot"]', "css": "#todaysHot", "description": "메인 배너"},
    {"xpath": '//*[@id="todayDiscoveryUnit"]/div', "css": "#todayDiscoveryUnit > div", "description": "오늘의 발견"},
    {"xpath": '//*[@id="personalizedGW"]', "css": "#personalizedGW", "description": "좋아할만한 카테고리 상품 영역 요소" },
    {"xpath": '//*[@id="categoryBestUnit"]', "css": "#categoryBestUnit", "description": "카테고리별 추천 광고상품"},
    {"xpath": '//*[@id="categoryBest_travel"]/dl[2]', "css": "#categoryBest_travel dl:nth-child(2)", "description": "하단 배너"},
    {"xpath": '//*[@id="footer"]', "css": "#footer", "description": "하단 푸터"}
]

# 모든 요소 검증 실행
for element in elements_to_check:
    verify_element(xpath=element["xpath"], css=element["css"], description=element["description"])

# 테스트 완료 후 브라우저 닫기
driver.quit()