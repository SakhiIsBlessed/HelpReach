import requests, io
print('Posting file...')
files = {'documents': ('test.txt', io.BytesIO(b'hello world'), 'text/plain')}
r = requests.post('http://127.0.0.1:5000/api/ngo/1/documents', cookies={'ngo_id':'1'}, files=files)
print('STATUS', r.status_code)
print('TEXT', r.text)
