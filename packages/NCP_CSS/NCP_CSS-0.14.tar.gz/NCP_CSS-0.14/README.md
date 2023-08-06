# NCP CSS Python Module

## 1. Usage

1. translate_text
    - String 을 지정된 디렉토리에 mp3 파일에 저장한다.
2. translate_file
    - User 가 지정한 File 을 읽어 지정된 디렉토리에 mp3 파일에 저장한다.
    
## 2. Voice & Language
    jinho : 한국어, 남성 음색
    clara : 영어, 여성 음색
    matt : 영어, 남성 음색
    yuri : 일본어, 여성 음색
    shinji : 일본어, 남성 음색
    meimei : 중국어, 여성 음색
    liangliang : 중국어, 남성 음색
    jose : 스페인어, 남성 음색
    carmen : 스페인어, 여성 음색
    
## 3. Speed Rnage 
    -5 < speed < 5

## 4. Example :
```
from NCP_CSS.CSS import CSS
from pathlib from Path

css = CSS(client_id="client_id", client_secret="client_secret")
css.translate_text(text="만나서 반갑습니다. 안녕 말포이. 안녕 해리포터,안녕 해리포터,안녕 해리포터,안녕 말포이,"
                   , file_path=Path(Path.cwd() / "test.mp3")
                   , speaker="jinho"
                   , speed=1
                   )
css.translate_file(text_file=Path("/Users/naver/test.txt")
                   , file_path=Path("~/home/download/result.mp3")
                   , speaker="jinho"
                   , speed=1
                   )

```
