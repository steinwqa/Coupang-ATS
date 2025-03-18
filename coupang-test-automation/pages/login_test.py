from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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


# 📌 **메인 페이지 클래스 (MainPage)**
class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def click_login_button(self):
        """메인 페이지에서 로그인 버튼 클릭"""
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/a'))
        )
        login_button.click()
        print("✅ 로그인 버튼 클릭, 로그인 페이지로 이동")

# 📌 **로그인 페이지 클래스 (LoginPage)**
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_credentials(self, username, password):
        """아이디 & 비밀번호 입력"""
        try:
            id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="login-email-input"]'))
            )
            pw_input = self.driver.find_element(By.XPATH, '//*[@id="login-password-input"]')

            id_input.send_keys(username)
            pw_input.send_keys(password)
            print("✅ 로그인 정보 입력 완료")

        except NoSuchElementException:
            print("❌ 로그인 입력 필드를 찾을 수 없음")
            driver.save_screenshot("login_input_error.png")

    def click_login_button(self):
        """로그인 버튼 클릭"""
        try:
            login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="memberLogin"]/div[1]/form/div[5]/button'))
            )
            login_btn.click()
            print("✅ 로그인 버튼 클릭")
        except TimeoutException:
            print("❌ 로그인 버튼을 찾을 수 없음")
            driver.save_screenshot("login_button_click_error.png")

# 📌 **로그인 테스트 실행 (TestLogin)**
class TestLogin:
    def __init__(self, driver):
        self.driver = driver
        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)

    def test_login(self, username, password):
        """로그인 테스트 실행"""
        self.main_page.click_login_button()
        WebDriverWait(self.driver, 10).until(EC.url_contains("https://login.coupang.com"))  # 로그인 페이지 확인
        print("✅ 로그인 페이지로 이동 확인")
        
        self.login_page.enter_credentials(username, password)
        self.login_page.click_login_button()
        
        # 로그인 확인 (예: 로그인 후 나타나는 특정 요소 확인)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="logout"]'))
            )
            print("✅ 로그인 성공!")
        except TimeoutException:
            print("❌ 로그인 실패")
            driver.save_screenshot("login_failed.png")

# 📌 **로그인 테스트 실행**
test = TestLogin(driver)

# ✨ 여기에 본인 계정 정보 입력
test.test_login("", "")

driver.find_element(By.XPATH, '//*[@id="logout"]/a').click() #로그아웃
print("✅ 로그아웃 성공!")


time.sleep(3)

# 테스트 완료 후 브라우저 닫기
driver.quit()