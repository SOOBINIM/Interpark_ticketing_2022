from selectors import SelectSelector
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException, UnexpectedAlertPresentException, \
    ElementClickInterceptedException, NoAlertPresentException, ElementNotInteractableException
from tkinter import *
import numpy
import time, datetime
import cv2 as cv
import os

opt = webdriver.ChromeOptions()
opt.add_argument('window-size=800,700')
driver = webdriver.Chrome(executable_path=os.getcwd() + "\\es\\chromedriver.exe", options=opt)
wait = WebDriverWait(driver, 10)
url = "https://ticket.interpark.com/Gate/TPLogin.asp"
driver.get(url)


def login_go():
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_name('userId').send_keys(id_entry.get())
    driver.find_element_by_id('userPwd').send_keys(pw_entry.get())
    driver.find_element_by_id('btn_login').click()


def link_go():
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())


def link_test():
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())
    driver.switch_to.frame(driver.find_element_by_id('ifrmBookStep'))
    driver.execute_script("document.querySelectorAll('.calCont').forEach(function(a) {a.remove()})")


def seat_macro():
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("ifrmSeat"))
    driver.switch_to.frame(driver.find_element_by_name("ifrmSeatDetail"))
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')))
    seats = driver.find_elements_by_css_selector(
        'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
    print(len(seats))
    if int(2) > len(seats):
        seat_count = len(seats)
    else:
        seat_count = int(2)
    for i in range(0, seat_count):
        seats[i].click()
    print("좌석 선택 완료")
    driver.switch_to.default_content()
    # seatSelect = Select(driver.find_element_by_css_selector('#PriceRow002'))    
    # seatSelect.select_by_value("ifrmSeat")
    driver.switch_to.frame(driver.find_element_by_name("ifrmSeat"))
    driver.find_element_by_id("NextStepImage").click()


def date_select():
    # 날짜
    while True:
        driver.switch_to.frame(driver.find_element_by_id('ifrmBookStep'))
        if int(calender_entry.get()) == 0:
            pass
        elif int(calender_entry.get()) >= 1:
            for i in range(1, int(calender_entry.get()) + 1):
                driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/span[3]").click()
        try:
            driver.find_element_by_xpath('(//*[@id="CellPlayDate"])' + "[" + date_entry.get() + "]").click()
            break
        except NoSuchElementException:
            # link_go()
            # go()
            break
        except NoSuchElementException:
            link_go()
            go()
            break
    # 회차
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + round_entry.get() + ']/a'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_id('LargeNextBtnImage').click()


def seat_again():
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.execute_script('$("ifrmSeatDetail").contentWindow.location.reload();')
    driver.execute_script('fnInitSeat();')
    seat_macro()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.find_element_by_id('NextStepImage').click()


def all_go():
    global wait
    wait = WebDriverWait(driver, 10)
    date_select()
    seat_macro()
    # link_go()
    # go()

def paycoPayment():
    driver.switch_to.default_content()
    driver.find_element_by_id('idInputArea').send_keys("01099637434")
    driver.find_element_by_id('pwInput').send_keys("skWkd92!@")
    driver.find_element_by_id('loginBtn').click()


def credit():
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="YYMMDD"]'))).send_keys(birth_entry.get())
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    bank2 = bank_var.get()
    payco2 = payco_var.get()
    if bank2 == 1:
        bank()
    elif payco2 == 1:
        payco()


def bank():
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22004"]/td/input'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BankCode"]/option[7]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()


def payco():
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_Payco"]/td/input'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()


def clock_time():
    clock = time.strftime('%X')
    time_label.config(text=clock)
    time_label.after(1, clock_time)



dp = Tk()
main_frame = Frame(dp)
dp.geometry('300x450')
dp.title("인터파크 티켓팅 프로그램")
main_frame.pack()

id_label = Label(main_frame, text="아이디")
id_label.grid(row=1, column=0)

id_entry = Entry(main_frame)
id_entry.grid(row=1, column=1)

pw_label = Label(main_frame, text="비밀번호")
pw_label.grid(row=2, column=0)

pw_entry = Entry(main_frame)
pw_entry.grid(row=2, column=1)

login_button = Button(main_frame, text="로그인", command=login_go, height=2)
login_button.grid(row=3, column=1)

showcode_label = Label(main_frame, text="공연번호")
showcode_label.grid(row=4, column=0)

showcode_entry = Entry(main_frame)
showcode_entry.grid(row=4, column=1)

calendar_label = Label(main_frame, text="달력")
calendar_label.grid(row=5, column=0)

calender_entry = Entry(main_frame)
calender_entry.grid(row=5, column=1)

date_label = Label(main_frame, text="날짜")
date_label.grid(row=6, column=0)

date_entry = Entry(main_frame)
date_entry.grid(row=6, column=1)

round_label = Label(main_frame, text="회차")
round_label.grid(row=7, column=0)

round_entry = Entry(main_frame)
round_entry.grid(row=7, column=1)

ticket_label = Label(main_frame, text="티켓 수")
ticket_label.grid(row=8, column=0)

ticket_entry = Entry(main_frame)
ticket_entry.grid(row=8, column=1)

link_button = Button(main_frame, text="직링", command=link_go, height=2)
link_button.grid(row=9, column=0, sticky=E)

all_button = Button(main_frame, text='시작', command=all_go, height=2)
all_button.grid(row=9, column=1, sticky=W + E)

chair_button = Button(main_frame, text="좌석", command=seat_macro, height=2)
chair_button.grid(row=9, column=2, sticky=W)

credit_button = Button(main_frame, text="결제", command=credit, height=2)
credit_button.grid(row=10, column=1, sticky=W + E)

bank_var = IntVar(value=0)
bank_check = Checkbutton(main_frame, text='무통장', variable=bank_var)
bank_check.grid(row=9, column=3)

payco_var = IntVar(value=0)
payco_check = Checkbutton(main_frame, text='페이코', variable=payco_var)
payco_check.grid(row=10, column=3)

link_button = Button(main_frame, text="페이코로그인", command=paycoPayment, height=2)
link_button.grid(row=13, column=0, sticky=E)

time_label = Label(main_frame, height=2)
time_label.grid(row=14, column=1)

birth_label = Label(main_frame, text='생년월일')
birth_label.grid(row=15, column=0)

birth_entry = Entry(main_frame)
birth_entry.grid(row=15, column=1)

full_time = (datetime.datetime.combine(datetime.date(1, 1, 1), datetime.datetime.now().time()) + datetime.timedelta(
    seconds=20)).time()

clock_time()
dp.mainloop()
