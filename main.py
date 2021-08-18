import json
from wsimple.api import Wsimple
import yfinance as yf

def get_otp():
    return input("Enter otpnumber: \n>>>")


def main():
    email = str(input("ENTER EMAIL: \n>>>"))
    password = str(input("ENTER PASSWORD: \n>>>"))
    
    ws = Wsimple(email, password, otp_callback=get_otp)
    
    # always check if wealthsimple is working (return True if working or an error)
    if ws.is_operational():
        while True:
            ticker_sym = input("enter security name:")
            
            msft = yf.Ticker(ticker_sym)
            print(msft.info["ask"])
    
    
if __name__ == "__main__":
    main()