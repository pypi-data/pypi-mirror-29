# pknulms-py

부경대학교 Smart-LMS Python 클라이언트

## 사용법

```python
import sys

from pknulms import LMSClient

lms = LMSClient()
if not lms.login('사용자 아이디', '사용자 비밀번호'):
    print('로그인에 실패했습니다.')
    sys.exit(0)

if lms.send_note('받는 사람 아이디', '제목', '내용'):
    print('쪽지 전송 성공')
else:
    print('쪽지 전송 실패')
    
lms.logout()
```
