# import requests
# import sqlalchemy
import aiohttp
import asyncio
import multidict



async def make_event(user, password, event_name, event_location, start_hour, start_minute, start_ampm, end_hour, end_minute, end_ampm, start_date, end_date):
    payload = {
    'j_username': user,
    'j_password': password,
    'shib_idp_revokeConsent': True,
    '_eventId_proceed': '',
    }

    async with aiohttp.ClientSession() as client:
        async with client.get('https://icatcard.ucmerced.edu/attendance') as resp:
            pass
            # print(f"{await resp.text()=!s}")
            # print(f"{resp.cookies=}")
            # print(f"{resp.url=}")
        # for cookie in client.cookie_jar:
        #     print(f"{cookie.key=} {cookie.value=}")
        
        async with client.post('https://shib.ucmerced.edu/idp/profile/cas/login?execution=e1s1', data=payload) as resp:
            print(f"{await resp.text()=!s}")
        
        # print('before clear cookies') 
        # for cookie in client.cookie_jar:
        #     print(f"{cookie.key=} {cookie.value=}", end=f" {expires}" if (expires := cookie['expires']) else '\n')
        
        # print('after clear cookies') 
        # for cookie in client.cookie_jar:
        #     print(f"{cookie.key=} {cookie.value=}", end=f" {expires}" if (expires := cookie['expires']) else '\n')

        event_dict = {
            'event_name': event_name,
            'event_location': event_location,
            'start_hour': start_hour,
            'start_minute': start_minute,
            'start_ampm': start_ampm,
            'end_hour': end_hour,
            'end_minute': end_minute,
            'end_ampm': end_ampm,
            'start_date': start_date,
            'end_date': end_date,
            'status': 1,
            'age': 0,
            'prereg': 0,
            'prereg_max': '',
            'prereg_only_manuel': 0,
            'duplicates': 0,
            'notes': 0,
            'affiliation[]': 'all',
            'max': '',
            'grade[]': 'any',
            'residence': 0,
            'checkio': 0,
            'group': '52',
            'perk_private': 0,
            'perk_multiple': 0,
            'action': 'create',
            'submit_create': 'Create Event',
        }
        async with client.post('https://icatcard.ucmerced.edu/attendance/', data=event_dict) as resp:
            with open('index.html', 'w') as file:
                file.write(await resp.text())

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(make_event(, ))


# url = 'http://127.0.0.1:8000/get-clubs'
# myobj = {'stuid': 100412333, "code": 1234}

# x = requests.post(url, params = myobj)
# x = requests.get(url)
# print(x.text)

# https://icatcard.ucmerced.edu/attendance

