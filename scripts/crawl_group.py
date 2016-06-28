from selenium import webdriver

driver = webdriver.Firefox()


class GetMealsFromGroup:
    def __init__(self):
        """클래스의 생성자 입니다.
         webdriver와 로그인에 사용될 email, password,
         어떤 그룹의 신규가입자에게 메세지를 보낼지 결정하는 group_id,
         메세지 내용을 담고있는 msg(message) 를
         settings.ini에서 읽어와 변수에 저장합니다.
        """

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.facebook.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

        from configparser import RawConfigParser
        from os.path import join, abspath, dirname
        import codecs

        settings_path = join(abspath(dirname(__file__)), 'settings.ini')

        cfg = RawConfigParser()
        cfg.read_file(codecs.open(settings_path, "r", "utf8"))

        self.email = cfg.get('setting', "email")
        self.pw = cfg.get('setting', 'pw')
        self.group_id = cfg.get('setting', 'group_id')
        self.group_name = cfg.get('setting', 'group_name')

    def run(self):
        """작업을 실행하는 함수입니다.
        """
        self.login()
        self.parse()

    def login(self):
        """로그인을 수행하는 함수입니다.
        :return: 로그인의 성공, 실패 유무를 반환합니다.
        """
        self.driver.get(self.base_url)
        self.driver.find_element_by_id("email").clear()
        self.driver.find_element_by_id("email").send_keys(self.email)
        self.driver.find_element_by_id("pass").clear()
        self.driver.find_element_by_id("pass").send_keys(self.pw)
        login_button = self.driver.find_element_by_id("u_0_o")
        login_button.click()

        return "login.php" not in self.driver.current_url

    def sold(self, pid):
        url = "https://www.facebook.com/groups/{group_id}/permalink/{post_id}/".format(
            group_id=self.group_id,
            post_id=pid
        )
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        button = self.driver.find_element_by_class_name("_3nnn")
        button.click()
        return True

    def parse(self):
        self.driver.get('https://www.facebook.com/groups/{}/'.format(self.group_id))

        """
        try:
            self.driver.find_element_by_name("message_body").clear()
            send_by_enter = self.driver.find_element_by_class_name('_1r_')

            if send_by_enter.get_attribute('aria-checked') != u'false':
                # aria-checked 가 true,면 get_attribute() 가 null을 리턴합니다..
                send_by_enter.click()  # 엔터키로 전송을 비활성화 하기 위함입니다.

            send_button = self.driver.find_element_by_id("u_0_w")
            send_button.click()
            # 메세지 전송 버튼을 클릭하는 부분입니다.

        # 아래 네줄은 예외상황을 처리하는 코드입니다. 예외가 생긴다면 db에 로그가 기록되지 않습니다.
        except NoSuchElementException:
            return None
        except UnexpectedAlertPresentException:
            return None
        ###

        self.c.execute(
            "INSERT INTO message_log (`fb_id`, `name`, `join_time`, `sended_time`) VALUES((?), (?), (?), (?))",
            (fb_id, name, join_time, datetime.now()))
        self.conn.commit()
        """

    def __del__(self):
        self.driver.quit()


if __name__ == "__main__":
    w = GetMealsFromGroup()
    w.run()
