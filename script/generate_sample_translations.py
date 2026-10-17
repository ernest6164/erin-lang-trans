import os
from pathlib import Path

SAMPLE_DIR = Path("sample")

TRANSLATIONS = {
    "f642c8dbcc26baabdb8b613aadb6cac0896bf850df06b44e83ad3001f9afcfe2.jpg": {
        "title": "양피지 낙서 (마비노기 여신 모리안, 타르라크, 퍼거스 3인방 일러스트 및 에피소드)",
        "sections": [
            {
                "name": "붉은색 네임택 및 감탄사",
                "erin_jamo": (
                    "1. 좌측 상단 날개 달린 여신: ㅇ ㅕ ㅅ ㅣ ㄴ (여신)\n"
                    "2. 우측 상단 안경 쓴 인물 감탄사: ㅂ ㅏ ㅂ ㅗ ! (바보!)\n"
                    "3. 우측 중단 안경 쓴 인물 이름: ㅌ ㅏ ㄹ ㅡ ㄹ ㅏ ㄱ (타르라크)\n"
                    "4. 좌측 하단 망치를 든 대장장이: ㅍ ㅓ ㄱ ㅓ ㅅ ㅡ (퍼거스)"
                ),
                "korean": "1. 여신 / 2. 바보! / 3. 타르라크 / 4. 퍼거스",
                "english_qwerty": "1. dutls / 2. qkqh! / 3. xkfmffkr / 4. vjritm",
                "note": "마비노기 G1의 핵심 인물인 여신 모리안, 삼용사 타르라크, 대장장이 퍼거스를 캐리커처와 함께 붉은 글씨로 유쾌하게 표현함."
            },
            {
                "name": "우측 상단 (여신 모리안 에피소드 본문)",
                "erin_jamo": (
                    "...ㅇ ㅕ ㅅ ㅣ ㄴ ㅇ ㅣ  ㄴ ㅓ ㄹ  ㅇ ㅣ ㄲ ㅡ ㄴ ㄷ ㅏ\n"
                    "ㄱ ㅜ ㅇ ㅜ ㅓ ㄴ ㅎ ㅐ ㅈ ㅜ ㅓ ,  ㅁ ㅣ ㄹ ㄹ ㅔ ㅅ ㅣ ㅇ ㅏ ㄴ ,  ㅁ ㅣ ㄹ ㄹ ㅔ ㅅ ㅣ ㅇ ㅏ ㄴ ...\n"
                    "ㄱ ㅜ ㅎ ㅐ ㄷ ㅏ ㄹ ㄹ ㅏ ㄱ ㅗ  ㅈ ㅏ ㄲ ㅜ  ㅂ ㅜ ㄹ ㅡ ㄴ ㄷ ㅏ .\n"
                    "ㅇ ㅓ ㄴ ㅈ ㅔ ㄲ ㅏ ㅈ ㅣ  ㄱ ㅣ ㄷ ㅏ ㄹ ㅛ ㅇ ㅑ  ㅎ ㅏ ㄴ ㅡ ㄴ ㄱ ㅏ ."
                ),
                "korean": (
                    "...여신이 널 이끈다\n"
                    "구원해줘, 밀레시안, 밀레시안...\n"
                    "구해달라고 자꾸 부른다.\n"
                    "언제까지 기다려야 하는가."
                ),
                "english_qwerty": (
                    "...dutlsdl sjf dirlsek\n"
                    "rndnjsgowndj, alffptldks, alffptldks...\n"
                    "rngogkffkrwh wkRnr qnfmsek.\n"
                    "djsjprkwl rlekolk gksmsrk."
                ),
                "note": "마비노기 G1 여신강림 오프닝에서 여신 모리안이 꿈속에서 밀레시안을 계속 부르며 구원을 요청하는 상황을 유머러스하게 기록함."
            },
            {
                "name": "좌측 중단 (타르라크를 향한 여신의 부름에 대한 의문)",
                "erin_jamo": (
                    "ㅇ ㅕ ㅅ ㅣ ㄴ ㄲ ㅔ  ㅇ ㅜ ㄹ ㅣ  ㅌ ㅏ ㄹ ㅡ ㄹ ㅏ ㅋ ㅡ ㄹ ㅡ ㄹ\n"
                    "ㅇ ㅏ ㄹ ㄲ ㅏ ㅛ ?  ㅌ ㅏ ㄹ ㅡ ㄹ ㅏ ㅋ ㅡ ㄴ ㅡ ㄴ  ㅇ ㅕ ㅅ ㅣ ㄴ ㅇ ㅣ\n"
                    "ㄱ ㅜ ㅎ ㅐ ㅈ ㅜ ㄹ ㄱ ㅓ ㄹ ㅏ  ㅁ ㅣ ㄷ ㅇ ㅓㅆ ㄴ ㅡ ㄴ ㄷ ㅔ\n"
                    "ㅇ ㅓ ㄴ ㅈ ㅔ ㄲ ㅏ ㅈ ㅣ  ㅈ ㅓ ㄹ ㅓ ㅎ ㄱ ㅔ  ㅅ ㅏ ㄹ ㅇ ㅏ ㅛ ㅏ  ㅎ ㅏ ㄴ ㅡ ㄴ ㄱ ㅏ ."
                ),
                "korean": (
                    "여신께 우리 타르라크를\n"
                    "알까요? 타르라크는 여신이\n"
                    "구해줄거라 믿었는데\n"
                    "언제까지 저렇게 살아야 하는가."
                ),
                "english_qwerty": (
                    "dutlssRo dnfl xkfmffkzmfmf\n"
                    "dkfRkdy? xkfmffkzmmsms dutlsdl\n"
                    "rngownfrjfk aledjTsmsep\n"
                    "djsjprkwl wjfjgro tkfdkdyk gksmsrk."
                ),
                "note": "여신을 구하러 저승으로 갔다가 곰의 저주를 받고 낮에는 곰으로 살아가게 된 타르라크의 처지를 한탄하는 내용."
            },
            {
                "name": "중앙 하단 (곰이 된 마법사 타르라크의 분노)",
                "erin_jamo": (
                    "...ㅌ ㅏ ㄹ ㅡ ㄹ ㅏ ㅋ ㅡ ㄴ ㅡ ㄴ  ㅁ ㅏ ㅂ ㅓ ㅂ ㅅ ㅏ ㅇ ㅣ ㄴ ㄷ ㅔ\n"
                    "ㅇ ㅣ ㄴ ㄱ ㅏ ㄴ ㅇ ㅡ ㄹ  ㅂ ㅓ ㄹ ㅣ ㄱ ㅗ  ㄱ ㅗ ㅁ ㅇ ㅣ  ㄷ ㅚ ㅇ ㅓㅆ ㄷ ㅏ .\n"
                    "ㄴ ㅓ ㅁ ㅜ  ㅅ ㅣ ㄹ ㅎ ㄷ ㅏ ,  ㅅ ㅏ ㄹ ㅏ ㅁ ㅇ ㅡ ㄹ  ㅈ ㅗ ㅎ ㅇ ㅏ ㅎ ㅏ ㅈ ㅣ\n"
                    "ㅇ ㅏ ㄴ ㅎ ㄴ ㅡ ㄴ ㄷ ㅏ  ㅍ ㅕ ㄴ ㅈ ㅣ ㄹ ㅡ ㄹ  ㅈ ㅜ ㅈ ㅣ  ㅁ ㅏ ㄹ ㅏ\n"
                    "ㅍ ㅕ ㄴ ㅈ ㅣ ㄹ ㅡ ㄹ  ㅂ ㅜ ㅅ ㅓ ㅂ ㅓ ㄹ ㅛㅆ ㄷ ㅏ ."
                ),
                "korean": (
                    "...타르라크는 마법사인데\n"
                    "인간을 버리고 곰이 되었다.\n"
                    "너무 싫다, 사람을 좋아하지\n"
                    "않는다 편지를 주지 마라\n"
                    "편지를 찢어버렸다."
                ),
                "english_qwerty": (
                    "...xkfmffkzmmsms akqjqtkindp\n"
                    "dlrksdmf qjflrh rhadl ehljTsek.\n"
                    "sjmu tlfrxek, tkfkadmf whdkgkwl\n"
                    "dksgsmsek vuswlfmf wnwl akfk\n"
                    "vuswlfmf qntjqjfydTsek."
                ),
                "note": "시드 스넷타에서 곰의 모습으로 은둔하는 타르라크가 사람들과 편지를 귀찮아하며 찢어버렸다는 귀여운 일화."
            },
            {
                "name": "우측 하단 (대장장이 퍼거스의 무기 파괴 악명)",
                "erin_jamo": (
                    "...ㅍ ㅓ ㄱ ㅓ ㅅ ㅡ  ㅅ ㅗ ㄴ ㅇ ㅣ  ㅁ ㅣ ㄲ ㅡ ㄹ ㅓ ㅈ ㅛㅆ ㄷ ㅏ\n"
                    "ㅁ ㅏ ㄴ ㅎ ㅣ  ㄷ ㅏ ㅊ ㅣ ㄴ ㄷ ㅏ ,  ㅇ ㅜ ㄹ ㅣ ㄴ ㅡ ㄴ\n"
                    "ㅁ ㅜ ㄱ ㅣ ㄹ ㅡ ㄹ  ㅂ ㅜ ㅅ ㅓ ㅈ ㅛㅆ ㄷ ㅏ !\n"
                    "ㅍ ㅓ ㄱ ㅓ ㅅ ㅡ ㄴ ㅡ ㄴ  ㅁ ㅣ ㅊ ㅛㅆ ㄷ ㅏ\n"
                    "ㅅ ㅓ ㄴ ㅁ ㅜ ㄹ ㅇ ㅡ ㄹ  ㅈ ㅜ ㅈ ㅣ  ㅁ ㅏ ㄹ ㅏ\n"
                    "ㅁ ㅏ ㅇ ㅊ ㅣ ㄹ ㅡ ㄹ  ㄷ ㅓ ㄴ ㅈ ㅛ ㅂ ㅓ ㄹ ㅣ ㄱ ㅗ  ㅅ ㅣ ㅍ ㄷ ㅏ ."
                ),
                "korean": (
                    "...퍼거스 손이 미끄러졌다\n"
                    "많이 다친다, 우리는\n"
                    "무기를 부서졌다!\n"
                    "퍼거스는 미쳤다\n"
                    "선물을 주지 마라\n"
                    "망치를 던져버리고 싶다."
                ),
                "english_qwerty": (
                    "...vjritm thsdl alRmfjwydTsek\n"
                    "aksgl ekclsek, dnflsms\n"
                    "anrflfmf qntjwydTsek!\n"
                    "vjritmsms alcyTsek\n"
                    "tjsanfdmf wnwl akfk\n"
                    "akdclflfmf dejsjydqjflrh tlvek."
                ),
                "note": "티르 코네일의 대장장이 퍼거스가 수리할 때마다 유명한 대사('어이쿠, 손이 미끄러졌네!')를 남기며 무기 내구도를 깨먹어 유저들이 겪었던 고통을 생생하게 풍자함."
            }
        ]
    },
    "MabinogiMobile_2026101714515366.png": {
        "title": "성벽 기념비 비문 (패션 선언 - Fashion Declaration)",
        "sections": [
            {
                "name": "제목 (Title)",
                "erin_jamo": "ㅍ ㅐ ㅅ ㅕ ㄴ  ㅅ ㅓ ㄴ ㅇ ㅓ ㄴ",
                "korean": "패션 선언",
                "english_qwerty": "votus tjsdjs",
                "note": "비석 1행에 음각으로 조각된 메인 타이틀 (고대 기념비 양식으로 모음이 대칭 조각됨)."
            },
            {
                "name": "본문 8행 (Body Lines 1~8)",
                "erin_jamo": (
                    "1행: ㅅ ㅡ ㅌ ㅏ ㅇ ㅣ ㄹ ㅇ ㅡ ㄴ  ㅇ ㅜ ㄹ ㅣ ㄹ ㅡ ㄹ\n"
                    "2행: ㅅ ㅗ ㄱ ㅂ ㅏ ㄱ ㅎ ㅏ ㅈ ㅣ  ㅇ ㅏ ㄴ ㅎ ㄴ ㅡ ㄴ ㄷ ㅏ\n"
                    "3행: ㄱ ㅡ ㅈ ㅓ  ㅅ ㅓ ㄴ ㅌ ㅐ ㄱ ㅎ ㅏ ㄴ ㅡ ㄴ\n"
                    "4행: ㅅ ㅜ ㄴ ㄱ ㅏ ㄴ  ㅈ ㅓ ㅇ ㅇ ㅢ ㄷ ㅚ ㄹ ㅃ ㅜ ㄴ\n"
                    "5행: ㄱ ㅡ ㄹ ㅓ ㄴ ㅣ  ㅍ ㅐ ㅅ ㅕ ㄴ ㅇ ㅣ ㄹ ㅏ ㄴ ㅡ ㄴ\n"
                    "6행: ㅇ ㅓ ㄴ ㅇ ㅓ ㄹ ㅗ  ㅇ ㅜ ㄹ ㅣ ㄱ ㅏ\n"
                    "7행: ㄴ ㅜ ㄱ ㅜ ㅇ ㅣ ㄴ ㅈ ㅣ  ㅈ ㅏ ㅇ ㅜ ㄹ ㅗ ㅂ ㄱ ㅔ\n"
                    "8행: ㅇ ㅚ ㅊ ㅕ ㄹ ㅏ"
                ),
                "korean": (
                    "스타일은 우리를\n"
                    "속박하지 않는다\n"
                    "그저 선택하는\n"
                    "순간 정의될뿐\n"
                    "그러니 패션이라는\n"
                    "언어로 우리가\n"
                    "누구인지 자유롭게\n"
                    "외쳐라"
                ),
                "english_qwerty": (
                    "tmxkdlfdms dnflfmf\n"
                    "thrqkrgkwl dksgsmsek\n"
                    "rmwj tjsxorgksms\n"
                    "tnsrks wjddlehlfQns\n"
                    "rmfjsl votusdlfksms\n"
                    "djsdjfh dnflrk\n"
                    "snrndlswl wkbkfhqro\n"
                    "hlcufk"
                ),
                "note": "마비노기 모바일 세계관의 의상 및 패션 커스터마이징의 철학을 선언하는 기념비적 문구."
            }
        ]
    },
    "MabinogiMobile_2026101719105416.png": {
        "title": "항구 선착장 게시판 (Noticeboard)",
        "sections": [
            {
                "name": "우측 하단 공문서 (Green Banner Notice)",
                "erin_jamo": (
                    "헤더: ㄱ ㅗ ㅇ ㅈ ㅣ ㅅ ㅏ ㅎ ㅏ ㅇ\n"
                    "1행: ㅅ ㅓ ㄴ ㅂ ㅏ ㄱ\n"
                    "2행: ㅇ ㅏ ㄴ ㅈ ㅓ ㄴ ㅅ ㅜ ㅊ ㅣ ㄱ\n"
                    "3행: ㅎ ㅓ ㄱ ㅏ ㅅ ㅓ  ㅇ ㅏ ㄴ ㄴ ㅐ"
                ),
                "korean": (
                    "공지사항\n"
                    "선박\n"
                    "안전수칙\n"
                    "허가서 안내"
                ),
                "english_qwerty": (
                    "rhdwltkgkd\n"
                    "tjsqkr\n"
                    "dksjswtndclr\n"
                    "gjrktj dksso"
                ),
                "note": "항구 출항 관련 안전수칙 및 허가 절차를 알리는 공식 안내문."
            },
            {
                "name": "좌측 중단 전단지 (Left Flyer)",
                "erin_jamo": (
                    "헤더: ㅅ ㅓ ㄴ ㅇ ㅜ ㅓ ㄴ  ㅁ ㅗ ㅈ ㅣ ㅂ\n"
                    "본문: ㅊ ㅜ ㄹ ㅎ ㅏ ㅇ  ㅇ ㅣ ㄹ ㅈ ㅓ ㅇ"
                ),
                "korean": (
                    "선원 모집\n"
                    "출항 일정"
                ),
                "english_qwerty": (
                    "tjsdnjs ahwlq\n"
                    "cnfgkd dflwjd"
                ),
                "note": "먼 바다로 떠나는 상선 및 탐험선의 선원 구인 공고."
            },
            {
                "name": "좌측 상단 마름모 전단지 (Top-Left Flyer)",
                "erin_jamo": "ㄱ ㅣ ㄹ ㄷ ㅡ  ㄱ ㅜ ㅇ ㅣ ㄴ",
                "korean": "길드 구인",
                "english_qwerty": "rlfem rndls",
                "note": "모험가 길드원 모집 벽보."
            }
        ]
    },
    "MabinogiMobile_2026101719152617.png": {
        "title": "레스토랑 입간판 포스터 (Steak & Dessert Restaurant Stand)",
        "sections": [
            {
                "name": "포스터 상단 아치 타이틀 (Top Banners)",
                "erin_jamo": (
                    "상단 1열: ㅇ ㅗ ㄴ ㅡ ㄹ ㅇ ㅢ  ㅊ ㅜ ㅊ ㅓ ㄴ\n"
                    "상단 2열: ㅂ ㅔ ㅅ ㅡ ㅌ ㅡ  ㅁ ㅔ ㄴ ㅠ (ㅂ ㅣ ㅏ ㅅ ㅡ ㅌ ㅡ  ㅁ ㅣ ㅏ ㄴ ㅠ)\n"
                    "중앙 녹색 리본: ㅁ ㅔ ㅇ ㅣ ㄴ  ㅁ ㅔ ㄴ ㅠ (ㅁ ㅣ ㅏ ㅇ ㅣ ㄴ  ㅁ ㅣ ㅏ ㄴ ㅠ)"
                ),
                "korean": (
                    "오늘의 추천\n"
                    "베스트메뉴\n"
                    "메인메뉴"
                ),
                "english_qwerty": (
                    "hsmfdml cncs\n"
                    "qptmxm apsb\n"
                    "dpdls apsb"
                ),
                "note": "스테이크와 베리 디저트 일러스트가 그려진 입간판 상단의 3중 아치형 메뉴 안내."
            },
            {
                "name": "포스터 하단 설명 (Bottom Descriptions)",
                "erin_jamo": (
                    "1행: ㅅ ㅡ ㅌ ㅔ ㅇ ㅣ ㅋ ㅡ  ㅅ ㅔ ㅌ ㅡ\n"
                    "2행: ㅅ ㅣ ㄴ ㅅ ㅓ ㄴ ㅎ ㅏ ㄴ  ㅈ ㅐ ㄹ ㅛ"
                ),
                "korean": (
                    "스테이크 세트\n"
                    "신선한 재료"
                ),
                "english_qwerty": (
                    "tmxpdlzm tpxm\n"
                    "tlstjsgks worfy"
                ),
                "note": "주방장이 추천하는 특제 스테이크 세트 설명 문구."
            }
        ]
    },
    "MabinogiMobile_2026101719155174.png": {
        "title": "음식점 칠판 메뉴판 (Restaurant Blackboard Menu - 9 Food Icons)",
        "sections": [
            {
                "name": "상단 타이틀 (Header)",
                "erin_jamo": "ㅇ ㅗ ㄴ ㅡ ㄹ ㅇ ㅡ ㅣ  ㅁ ㅣ ㅏ ㄴ ㅠ",
                "korean": "오늘의 메뉴",
                "english_qwerty": "hsmfdml apsb",
                "note": "에린어 정통 표기법에 맞춰 ㅔ를 ㅣ+ㅏ로 표기함."
            },
            {
                "name": "좌측 열 메뉴 3종 (Left Column)",
                "erin_jamo": (
                    "1. 고기 아이콘: ㅅ ㅗ ㄱ ㅗ ㄱ ㅣ (소고기)\n"
                    "2. 소시지 아이콘: ㅅ ㅗ ㅅ ㅣ ㅈ ㅣ (소시지)\n"
                    "3. 닭고기 아이콘: ㄷ ㅏ ㄹ ㄱ (닭)"
                ),
                "korean": "1. 소고기 / 2. 소시지 / 3. 닭",
                "english_qwerty": "1. thrhri / 2. thtlwl / 3. ekfr",
                "note": "육류 식재료 3종."
            },
            {
                "name": "중앙 열 메뉴 3종 (Center Column)",
                "erin_jamo": (
                    "1. 곡물 그릇: ㅁ ㅣ ㄹ (밀)\n"
                    "2. 치즈 아이콘: ㅊ ㅣ ㅈ ㅡ (치즈)\n"
                    "3. 채소 아이콘: ㅇ ㅑ ㅊ ㅏ ㅣ (야채)"
                ),
                "korean": "1. 밀 / 2. 치즈 / 3. 야채",
                "english_qwerty": "1. alf / 2. clwm / 3. dico",
                "note": "곡물, 유제품, 신선 채소류."
            },
            {
                "name": "우측 열 메뉴 3종 (Right Column)",
                "erin_jamo": (
                    "1. 생선 아이콘: ㅅ ㅏ ㅣ ㅇ ㅅ ㅓ ㄴ (생선)\n"
                    "2. 잎채소 아이콘: ㅅ ㅏ ㅇ ㅊ ㅜ (상추)\n"
                    "3. 감자 아이콘: ㄱ ㅏ ㅁ ㅈ ㅏ (감자)"
                ),
                "korean": "1. 생선 / 2. 상추 / 3. 감자",
                "english_qwerty": "1. todtjs / 2. tkdcn / 3. rkawk",
                "note": "어류 및 텃밭 수확물."
            },
            {
                "name": "하단 안내 문구 (Bottom Small Line)",
                "erin_jamo": "ㅇ ㅣ ㄹ ㅇ ㅣ ㄹ ㅎ ㅏ ㄴ ㅈ ㅓ ㅇ  ㅅ ㅜ ㄹ ㅛ ㅇ  ㅍ ㅏ ㄴ ㅁ ㅐ",
                "korean": "일일한정 수량판매",
                "english_qwerty": "dlfdlfgkswjd tnfyd vksao",
                "note": "당일 준비된 신선 재료 소진 시 마감됨을 알림."
            }
        ]
    },
    "MabinogiMobile_2026101719163381.png": {
        "title": "테이블 위 미니 칠판 스탠드 (Tabletop Chalkboard Sign)",
        "sections": [
            {
                "name": "상단 안내 (Top Header)",
                "erin_jamo": "ㅇ ㅗ ㄴ ㅡ ㄹ ㅇ ㅢ  ㅇ ㅛ ㄹ ㅣ",
                "korean": "오늘의 요리",
                "english_qwerty": "hsmfdml dyfl",
                "note": "테이블 손님을 위한 금일의 특별 메뉴 헤더."
            },
            {
                "name": "하단 대표 메뉴 (Bottom Main Dish)",
                "erin_jamo": "ㅅ ㅡ ㅌ ㅔ ㅇ ㅣ ㅋ ㅡ",
                "korean": "스테이크",
                "english_qwerty": "tmxpdlzm",
                "note": "오늘의 메인 추천 요리인 스테이크."
            }
        ]
    },
    "MabinogiMobile_2026101719165315.png": {
        "title": "계단 옆 스탠드 메뉴판 및 배경 칠판 (Stairs Menu Stand & Background Blackboard)",
        "sections": [
            {
                "name": "전면 목재 메뉴 스탠드 (Front Wooden Stand)",
                "erin_jamo": "ㅇ ㅗ ㄴ ㅡ ㄹ ㅇ ㅢ  ㅊ ㅜ ㅊ ㅓ ㄴ  ㅇ ㅛ ㄹ ㅣ",
                "korean": "오늘의 추천 요리",
                "english_qwerty": "hsmfdml cncs dyfl",
                "note": "식당 입구 계단 옆에 배치된 손글씨 스타일의 추천 요리 안내판."
            },
            {
                "name": "배경 칠판 메뉴판 (Background Blackboard)",
                "erin_jamo": (
                    "타이틀: ㅇ ㅗ ㄴ ㅡ ㄹ ㅇ ㅡ ㅣ  ㅁ ㅣ ㅏ ㄴ ㅠ (오늘의 메뉴)\n"
                    "품목: ㅅ ㅗ ㄱ ㅗ ㄱ ㅣ (소고기), ㅊ ㅣ ㅈ ㅡ (치즈), ㅅ ㅏ ㅣ ㅇ ㅅ ㅓ ㄴ (생선) 등"
                ),
                "korean": "오늘의 메뉴 (소고기, 소시지, 닭, 밀, 치즈, 야채, 생선, 상추, 감자)",
                "english_qwerty": "hsmfdml apsb (thrhri, thtlwl, ekfr, alf, clwm, dico, todtjs, tkdcn, rkawk)",
                "note": "주방 벽면에 걸린 대형 칠판 메뉴판과 연계됨."
            }
        ]
    },
    "MabinogiMobile_2026101719171474.png": {
        "title": "붉은 머리 여인 빈티지 포스터 (Rose Queen Poster)",
        "sections": [
            {
                "name": "상단 장식 타이틀 (Ornate Title)",
                "erin_jamo": "ㅈ ㅏ ㅇ ㅁ ㅣ ㅇ ㅡ ㅣ  ㅇ ㅕ ㅇ ㅗ ㅏ ㅇ",
                "korean": "장미의 여왕",
                "english_qwerty": "wkdaldml dudhkd",
                "note": "장미 꽃장식과 붉은 드레스를 입은 여인의 모습을 상징하는 문구."
            },
            {
                "name": "하단 리본 문구 (Ribbon Subtitle)",
                "erin_jamo": "ㅇ ㅔ ㄹ ㅣ ㄴ  ㅋ ㅗ ㄹ ㄹ ㅔ ㄱ ㅅ ㅛ ㄴ",
                "korean": "에린 콜렉션",
                "english_qwerty": "dpfls zhffprtyn",
                "note": "에린의 명품 의상 디자이너 브랜드 컬렉션 포스터."
            }
        ]
    },
    "MabinogiMobile_2026101719174550.png": {
        "title": "벽돌 벽면 안내문 및 상점 광고 (Brick Wall Flyers & Ads)",
        "sections": [
            {
                "name": "좌측 노란색 약초 전단지 (Yellow Herb Flyer)",
                "erin_jamo": "ㅇ ㅑ ㄱ ㅊ ㅗ  ㅊ ㅐ ㅈ ㅣ ㅂ",
                "korean": "약초 채집",
                "english_qwerty": "dirch coowlq",
                "note": "베이스 허브, 블러디 허브 등 연금술 및 포션 조제용 약초 채집가 모집."
            },
            {
                "name": "중앙 회색 관공서 벽보 (Grey Official Notices)",
                "erin_jamo": (
                    "1. ㄱ ㅜ ㅇ ㅣ ㄴ  ㄱ ㅗ ㅇ ㄱ ㅗ (구인 공고)\n"
                    "2. ㅎ ㅕ ㄴ ㅅ ㅏ ㅇ ㅅ ㅜ ㅂ ㅐ (현상수배)"
                ),
                "korean": "1. 구인 공고 / 2. 현상수배",
                "english_qwerty": "1. rndls rhdrh / 2. gustkdtnqo",
                "note": "마을 관청의 일자리 공고 및 치안 유지를 위한 지명수배 전단."
            },
            {
                "name": "우측 청색 포션 포스터 (Blue Potion Ad)",
                "erin_jamo": "ㅌ ㅡ ㄱ ㅈ ㅔ  ㅍ ㅗ ㅅ ㅕ ㄴ",
                "korean": "특제 포션",
                "english_qwerty": "xmrwp vhtus",
                "note": "마나 회복 및 체력 증진용 고급 연금술 포션 홍보."
            },
            {
                "name": "우측 상단 목재 표지판 (Top-Right Wooden Sign)",
                "erin_jamo": "ㅅ ㅏ ㅇ ㅈ ㅓ ㅁ  ㅇ ㅏ ㄴ ㄴ ㅐ",
                "korean": "상점 안내",
                "english_qwerty": "tkdwja dksso",
                "note": "인근 잡화점 및 장비점 위치 안내 표지판."
            }
        ]
    },
    "MabinogiMobile_2026101719193229.png": {
        "title": "스트리트 아트 그래피티 벽면 1 (Street Art Wall: Clewoon Cat)",
        "sections": [
            {
                "name": "메인 브랜드 로고 (Neon Sign, Wall Graffiti, Poster Centers)",
                "erin_jamo": "ㅋ ㅡ ㄹ ㅣ ㅇ ㅜ ㄴ (또는 ㅋ ㅡ ㄹ ㅣ ㅇ ㅗ ㄴ)",
                "korean": "클리운 (Clewoon / Cleon)",
                "english_qwerty": "zmffldns (zmffldhs)",
                "note": "힙합 스타일의 고양이 캐릭터를 마스코트로 하는 스트리트 패션 브랜드 또는 아티스트 크루 로고. 네온사인, 벽면 락카 그래피티, 삼색(녹/적/황) 포스터에 동일하게 각인됨."
            },
            {
                "name": "붉은색 포스터 상단 백색 띠 (Red Poster Top Bar)",
                "erin_jamo": "ㅇ ㅔ ㄹ ㅣ ㄴ  ㅅ ㅡ ㅌ ㅡ ㄹ ㅣ ㅌ ㅡ  ㄹ ㅏ ㅇ ㅣ ㅍ ㅡ",
                "korean": "에린 스트리트 라이프",
                "english_qwerty": "dpfls tmxmflxm fkdvtm",
                "note": "에린의 젊은 모험가들과 아티스트들의 자유로운 거리 문화를 표현한 슬로건."
            }
        ]
    },
    "MabinogiMobile_2026101719195160.png": {
        "title": "스트리트 아트 그래피티 벽면 2 (Street Art Wall: Clewoon Cat & Caution Tape)",
        "sections": [
            {
                "name": "흑색/청색 고양이 포스터 (Black & Blue Posters)",
                "erin_jamo": "ㅋ ㅡ ㄹ ㅣ ㅇ ㅜ ㄴ",
                "korean": "클리운 (Clewoon)",
                "english_qwerty": "zmffldns",
                "note": "스케이트보드를 탄 힙합 고양이 캐릭터 포스터의 브랜드 네임."
            },
            {
                "name": "노란색 안전 통제 테이프 (Yellow Caution Tape)",
                "erin_jamo": "ㅈ ㅜ ㅇ ㅢ  ㅈ ㅜ ㅇ ㅢ  ㅈ ㅜ ㅇ ㅢ",
                "korean": "주의  주의  주의",
                "english_qwerty": "wndml  wndml  wndml",
                "note": "공사장이나 접근 통제 구역에 둘러쳐진 노란색 폴리스 라인 스타일의 경고 테이프 문구."
            }
        ]
    },
    "MabinogiMobile_2026101719225307.png": {
        "title": "푸른빛 고대 룬석 1 (Glowing Blue Rune Stone 1)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "라데카(푸른 달)와 이웨카(붉은 달)의 가호를 받는 에린 세계관에서 모험가의 길을 비추는 고대 전승 문구."
            }
        ]
    },
    "MabinogiMobile_2026101719231835.png": {
        "title": "푸른빛 고대 룬석 2 (Glowing Blue Rune Stone 2)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "밤길을 밝혀주는 필드 웨이포인트 룬석 비문."
            }
        ]
    },
    "MabinogiMobile_2026101719232980.png": {
        "title": "푸른빛 고대 룬석 군집 3 (Glowing Blue Rune Stones Group 3)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "유적지 주변 여러 개의 룬석 기둥에 반복해서 새겨진 신성한 인도(Guidance)의 기도문."
            }
        ]
    },
    "MabinogiMobile_2026101719240037.png": {
        "title": "푸른빛 고대 룬석 군집 4 (Glowing Blue Rune Stones Group 4)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "고대 유적 수호 룬스톤의 표준 마법 명문."
            }
        ]
    },
    "MabinogiMobile_2026101719241172.png": {
        "title": "푸른빛 고대 룬석 5 (Rune Stone 5 & Thick Tree Tooltip)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "푸른 룬석 텍스트."
            },
            {
                "name": "게임 내 인터랙션 UI 툴팁 (In-Game Interaction Tooltip)",
                "erin_jamo": "ㄱ ㅜ ㄹ ㄱ ㅇ ㅡ ㄴ  ㄴ ㅏ ㅁ ㅜ",
                "korean": "굵은 나무",
                "english_qwerty": "rnrrdms skan",
                "note": "채집 가능한 상호작용 오브젝트 툴팁."
            }
        ]
    },
    "MabinogiMobile_2026101719241555.png": {
        "title": "푸른빛 고대 룬석 6 (Glowing Blue Rune Stone 6)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "마법 룬스톤 명문."
            }
        ]
    },
    "MabinogiMobile_2026101719242406.png": {
        "title": "푸른빛 고대 룬석 7 (Rune Stone 7 & Thick Tree Tooltip)",
        "sections": [
            {
                "name": "룬석 각명 2행 (Rune Inscription Lines 1~2)",
                "erin_jamo": (
                    "1행: ㄷ ㅏ ㄹ ㅂ ㅣ ㅊ ㅇ ㅣ  ㅇ ㅜ ㄹ ㅣ ㅇ ㅡ ㅣ\n"
                    "2행: ㄱ ㅣ ㄹ ㅇ ㅡ ㄹ  ㅇ ㅣ ㄴ ㄷ ㅗ ㅎ ㅏ ㄹ ㅣ ㄹ ㅏ"
                ),
                "korean": (
                    "달빛이 우리의\n"
                    "길을 인도하리라"
                ),
                "english_qwerty": (
                    "ekfqlcdl dnfldml\n"
                    "rlfdmf dlsehgkflfk"
                ),
                "note": "고대 룬석 텍스트."
            },
            {
                "name": "게임 내 인터랙션 UI 툴팁 (In-Game Interaction Tooltip)",
                "erin_jamo": "ㄱ ㅜ ㄹ ㄱ ㅇ ㅡ ㄴ  ㄴ ㅏ ㅁ ㅜ",
                "korean": "굵은 나무",
                "english_qwerty": "rnrrdms skan",
                "note": "나무 채집 오브젝트 툴팁."
            }
        ]
    },
    "MabinogiMobile_2026101719250450.png": {
        "title": "주전자 모양 돌출 간판 (Teapot Hanging Sign)",
        "sections": [
            {
                "name": "간판 중앙 텍스트 (Signplate Text)",
                "erin_jamo": "ㅁ ㅏ ㅇ ㅡ ㄹ (또는 ㅊ ㅏ ㅅ ㅈ ㅣ ㅂ)",
                "korean": "마을 (또는 찻집 / 티하우스)",
                "english_qwerty": "akdmf (cktwwlq)",
                "note": "주전자 조각이 달린 상점 입구의 목재 돌출 간판에 새겨진 정겨운 찻집/마을 쉼터 안내."
            }
        ]
    },
    "MabinogiMobile_2026101719255506.png": {
        "title": "상점 카운터 목판 명판 (Shop Counter Archway Plaque)",
        "sections": [
            {
                "name": "아치형 목판 상패 (2 Lines)",
                "erin_jamo": (
                    "1행: ㅇ ㅣ ㅂ ㅓ ㄴ ㄷ ㅏ ㄹ ㅇ ㅡ ㅣ\n"
                    "2행: ㅇ ㅜ ㅅ ㅜ ㅅ ㅏ ㅇ ㅍ ㅜ ㅁ  ㅅ ㅏ ㅇ ㅈ ㅓ ㅁ"
                ),
                "korean": (
                    "이번달의\n"
                    "우수상품 상점"
                ),
                "english_qwerty": (
                    "dlqjsekfdml\n"
                    "dntntkdvna tkdwja"
                ),
                "note": "마을 상인 조합에서 품질과 친절도를 인정받아 수여한 '이달의 우수상품 상점' 인증 명판."
            }
        ]
    },
    "MabinogiMobile_2026101719262604.png": {
        "title": "상점 벽면 액자 안내판 (Shop Wall Framed Sign: Special Discount)",
        "sections": [
            {
                "name": "액자 중앙 텍스트 (Framed Sign)",
                "erin_jamo": "ㅌ ㅡ ㄱ ㅂ ㅕ ㄹ ㅎ ㅏ ㄹ ㅇ ㅣ ㄴ",
                "korean": "특별할인",
                "english_qwerty": "xmrqufgkfdls",
                "note": "상점 내 이벤트 및 계절 특가 품목을 알리는 특별할인 액자."
            }
        ]
    },
    "MabinogiMobile_2026101719270028.png": {
        "title": "구걸 소년의 목재 피켓 (Beggar Boy's Wooden Sign)",
        "sections": [
            {
                "name": "원문 조각 글리프 (Original Carved Glyphs - Inverted Vowels)",
                "erin_jamo": "ㄷ ㅜ ㅇ ㅜ ㅏ / ㅈ ㅗ ㅅ ㅓ ㅣ ㅇ ㅠ",
                "korean": "두우아 조세유 (문자 형태 그대로 직독 시)",
                "english_qwerty": "en dndk / wh tpd b",
                "note": "글을 제대로 배우지 못한 어린 소년의 순박한 실수로 상하 대칭 모음(ㅗ↔ㅜ, ㅛ↔ㅠ)이 뒤집혀 조각되었으며, ㅔ 역시 에린어 정규식(ㅣ+ㅏ) 대신 일반 한글 타자 순서(ㅓ+ㅣ)로 파여 있음."
            },
            {
                "name": "의도된 표준 한국어/영어 번역 (Intended Standard Translation)",
                "erin_jamo": "ㄷ ㅗ ㅇ ㅘ  ㅈ ㅜ ㅅ ㅔ ㅇ ㅛ",
                "korean": "도와 주세요",
                "english_qwerty": "ehdhk wntpdyd",
                "note": "행인들에게 도움의 손길을 청하는 따뜻하고 애틋한 구걸 문구."
            }
        ]
    }
}

def main():
    created_files = []
    for filename, data in TRANSLATIONS.items():
        stem = Path(filename).stem
        out_path = SAMPLE_DIR / f"{stem}.txt"
        
        content = []
        content.append("=" * 80)
        content.append(f" [마비노기 모바일 에린어 번역 결과 보고서]")
        content.append(f" - 대상 이미지 파일: {filename}")
        content.append(f" - 이미지 테마/설명: {data['title']}")
        content.append("=" * 80)
        content.append("")
        
        for idx, sec in enumerate(data["sections"], 1):
            content.append(f"[{idx}. {sec['name']}]")
            content.append("  * 에린어 자모 풀어쓰기 (Erin Linear Jamo):")
            for line in sec["erin_jamo"].split("\n"):
                content.append(f"    {line}")
            content.append("")
            content.append("  * 한국어 번역 (Korean Translation):")
            for line in sec["korean"].split("\n"):
                content.append(f"    {line}")
            content.append("")
            content.append("  * 영어 두벌식 쿼티 키 매핑 (English 2-Set QWERTY):")
            for line in sec["english_qwerty"].split("\n"):
                content.append(f"    {line}")
            content.append("")
            content.append(f"  * 해독 분석 및 배경 설명 (Notes): {sec['note']}")
            content.append("-" * 80)
            content.append("")
        
        out_path.write_text("\n".join(content), encoding="utf-8")
        created_files.append(out_path.name)
        
        # Also create filename.txt if someone looks for <stem>.ext.txt
        # (keeping both or standard <stem>.txt)
    
    print(f"Successfully generated {len(created_files)} translation files in sample/:")
    for f in sorted(created_files):
        print(f" - {f}")

if __name__ == "__main__":
    main()
