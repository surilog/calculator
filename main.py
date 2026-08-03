import json
import random

class User:
    def __init__(self, username, point = 0, best_score=0):
        self.username = username
        self.point = point
        self.best_score = best_score

    def to_dict(self):
        return {"username" : self.username, "point" : self.point, "best_score" : self.best_score}
    


class Quiz:
    def __init__(self, question:str, choices: list, answer:str):
        self.question = question
        self.choices = choices
        self.answer = answer

    def check_answer(self, user_answer: str):
        return user_answer == self.answer

    def get_answer_number(self):
        return self.choices.index(self.answer) + 1

class QuizGame:
    def __init__(self, data_file: str ="state.json"):
        self.data_file = data_file
        self.quizzes = []
        self.users = []
        self.quizzes, self.users = self.load_data()
        #덮어쓰기(save_data)를 해서 기존 파일을 백지로 만들기 전에, 
        # 옛날 내용을 파이썬 머릿속으로 먼저 옮겨 담는 작업(load_data)이 반드시 필요!
        #위치: __init__은 프로그램 시작 시 단 한 번 실행되는 초기화 장소
        #즉, 바로 데이터를 메모리에 저장하기 위해서
        
        #a모드로 파일 여는 방법 안되는 이유:
        #"a" 모드는 파일 끝에 글자를 그냥 덧붙이는 기능이다.
        #JSON은 문법 구조([...])가 엄격해서 그냥 덧붙이면 파일이 깨진다.



    def load_data(self):
        default_quiz_data = [
                    {
                        "question": "다음 중 상대경로의 설명으로 적절한 것은?",
                        "choices": [
                            "현재 디렉토리에서 파일을 찾는 경로",
                            "루트 디렉토리에서 파일을 찾는 경로",
                            "절대 경로",
                            "고정된 경로"
                        ],
                        "answer": "현재 디렉토리에서 파일을 찾는 경로"
                    },
                    {
                        "question": "바인드 마운트에 대한 설명으로 적절한 것은?",
                        "choices": [
                            "호스트의 디렉토리를 컨테이너에 연결하는 방식",
                            "정해진 위치에서만 데이터를 읽고 쓸 수 있는 방식",
                            "영속성이 없는 임시 저장 방식",
                            "컨테이너 내부에서만 데이터를 저장하는 방식"
                        ],
                        "answer": "호스트의 디렉토리를 컨테이너에 연결하는 방식"
                    },
                    {
                        "question": "다음 docker-compose.yml 파일에서의 depends_on 옵션의 역할은 무엇인가?\n\nversion: '3.8'\nservices:\n  web:\n    image: nginx:latest\n    depends_on:\n      - cache-redis\n      - db-postgres\n...",
                        "choices": [
                            "WEB 서비스가 시작되기 전에 cache-redis와 db-postgres 서비스가 먼저 시작되도록 보장한다.",
                            "WEB 서비스가 시작되기 전에 cache-redis와 db-postgres 서비스가 먼저 종료되도록 보장한다.",
                            "cache-redis와 db-postgres 서비스가 시작되기 전에 WEB 서비스가 먼저 시작되도록 보장한다.",
                            "WEB 서비스가 시작되기 전에 cache-redis와 db-postgres 서비스가 먼저 삭제되도록 보장한다."
                        ],
                        "answer": "WEB 서비스가 시작되기 전에 cache-redis와 db-postgres 서비스가 먼저 시작되도록 보장한다."
                    },
                    {
                        "question": "다음 중 다운로드된 도커 이미지를 확인하는 명령어는?",
                        "choices": [
                            "docker image",
                            "docker ps",
                            "docker ps -a",
                            "docker images"
                        ],
                        "answer": "docker images"
                    },
                    {
                        "question": "다음 프로그램의 결과로 알맞은 것은? \n\nclass Animal: def __init__(self, name, age): self.name = name\n       self.age = age\n      def say(self):\n        print(f\"안녕하세요. 제 이름은 {self.name}이고, 나이는 {self.age}살 입니다.\")\n\nclass Dog(Animal):\n        def __init__(self, name, age, breed):\n          super().__init__(name, age)\n          self.breed = breed\n        def say(self):\n          print(f\"안녕. 내 이름은 {self.name}이고, 나이는 {self.age}살!. 나는 {self.breed}!.\")\nwolf = Dog(\"늑대\", 3, \"허스키\")\nwolf.say()",
                        "choices": [
                            "안녕하세요. 제 이름은 늑대이고, 나이는 3살 입니다. 저는 허스키입니다.",
                            "안녕. 내 이름은 늑대이고, 나이는 3살!. 나는 허스키!.",
                            "안녕하세요. 제 이름은 늑대이고, 나이는 3살 입니다. 나는 허스키!.",
                            "안녕. 내 이름은 늑대이고, 나이는 3살!. 저는 허스키입니다."
                        ],
                        "answer": "안녕. 내 이름은 늑대이고, 나이는 3살!. 나는 허스키!."
                    }
                ]
        default_user_data = []
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                state_data = json.load(file)
                quiz_data = state_data.get("quizzes",[])#딕셔너리 형태로 받아옴
                user_data = state_data.get("users",[])

                quizzes = []# json파일과 같이 리스트안 딕셔너리로 만들기 위해 리스트로 설정
                for quiz_item in quiz_data:
                    try:
                         quiz = Quiz(
                             question=quiz_item["question"],
                             choices=quiz_item["choices"],
                             answer=quiz_item["answer"]
                         )
                         quizzes.append(quiz)
                    except KeyError as e:
                        print(f"\n 퀴즈 데이터 형식 오류: {e}. 해당 퀴즈 항목을 건너뜁니다.")

                users = []
                for user_item in user_data:
                    try:
                         user= User(
                             username=user_item["username"],
                             point=user_item["point"],
                             best_score=user_item["best_score"]
                            )
                         users.append(user)
                    except KeyError as e:
                        print(f"\n 유저 데이터 형식 오류: {e}. 해당 유저 항목을 건너뜁니다.")

                if not quizzes:
                    quizzes=[Quiz(**quiz) for quiz in default_quiz_data]
                return quizzes, users
        except (FileNotFoundError, json.JSONDecodeError, AttributeError, ValueError, KeyError):
    # 파일이 없거나 훼손되었으면 기본 퀴즈 데이터와 빈 유저 리스트를 반환
         quizzes = [Quiz(**quiz) for quiz in default_quiz_data]
         users = [User(**user) for user in default_user_data]
         print("\n 파일이 존재하지 않거나 손상되었습니다. 기본 퀴즈 데이터를 사용하겠습니다.")
         return quizzes, users
         
                

                    
                    

    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                data = {
                    "quizzes" :  [
                       { "question": new_quiz.question,
                        "choices" : new_quiz.choices,
                        "answer" : new_quiz.answer
                    }
                    for new_quiz in self.quizzes
                    ],
                    "users" : [
                        new_user.to_dict() for new_user in self.users]
                }
                json.dump(data,file,ensure_ascii=False, indent=4)
        except(PermissionError, OSError) as e:
            print(f"\n 파일 저장 중 문제가 발생했습니다 : {e}")


    def find_user(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None
    #GUI로 변경할꺼기 때문에 백그라운드와 포그라운드 나눔
    def register_user(self, username: str):
        if self.find_user(username) is not None:
            return False
        new_user = User(username=username)
        self.users.append(new_user)
        self.save_data()
        return True

        
    def add_quiz(self, question: str, choices: list, answer: str):
        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_data()


#self.가 없다: 이 함수 안에서만 잠깐 쓰고 버릴 데이터 (예: 입력받은 question, 방금 만든 new_quiz)

#self.가 있다: 이 프로그램이 끝날 때까지 객체가 계속 들고 다녀야 할 내 데이터나 내 기능 
#(예: 전체 퀴즈 목록 self.quizzes, 저장하는 기능 self.save_data())


    def run(self):
        print("\n" + "=" * 40)
        print("1. 퀴즈 풀기\n"
        "2. 사용자 등록\n"
        "3. 사용자 목록\n"
        "4. 점수 확인\n"
        "5. 종료 화면\n"
        "6. 퀴즈 추가\n"
        "7. 퀴즈 목록\n")
        print("=" * 40)
        try:
            while True:
                input_menu = input("메뉴를 선택하세요: ").strip()

                if input_menu == "1":
                    self.start_quiz_flow()
                elif input_menu == "2":
                    self.register_user_flow()
                elif input_menu == "3":
                    self.show_users_flow()
                elif input_menu == "4":
                    self.check_score_flow()
                elif input_menu == "5":
                    print("\n프로그램을 종료합니다.")
                    break
                elif input_menu == "6":
                    self.add_quiz_flow()
                elif input_menu == "7":
                    self.quiz_list()
                else:
                    print("\n잘못된 입력입니다. 1~7번 사이의 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n사용자에 의해 프로그램이 강제 종료되었습니다.")
        except EOFError:
            print("\n입력 스트림이 종료되었습니다. 프로그램을 종료합니다.")
        finally:
            self.save_data()
            print("\n프로그램을 안전하게 정리하고 종료하겠습니다.")



    def start_quiz_flow(self):
        name = input ("\n 퀴즈를 풀 사용자 이름을 입력해주세요 : ").strip()
        current_user = self.find_user(name)

        if not current_user:
            print(f"[{name}] 님은 등록되지 않은 사용자 압니다. 먼저 사용자 등록을 해주세요!") 
            return
        print(f"\n[{name}] 님 , 퀴즈를 시작합니다!")

        try:
            score_gain = 0

            for idx, quiz_items in enumerate(self.quizzes, 1):
                print(f"\n문제 {idx} 번 : {quiz_items.question}")
                
                for i, choice in enumerate(quiz_items.choices, 1):
                    print(f"{i}번 선지 : {choice}")

                while True:
                    user_input = input("\n 정답을 입력하세요 : ").strip()
                    if user_input.isdigit() and 1<= int(user_input) <=4:
                        break
                    else:
                        print("잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요 : ")

                user_choice = []
                user_choice = quiz_items.choices[int(user_input) - 1]
                if quiz_items.check_answer(user_choice):
                    print("정답입니다! +1점")
                    score_gain +=1
                    current_user.point +=1
                else:
                    print(f"틀렸습니다. 정답은 {quiz_items.get_answer_number()}번의 {quiz_items.answer}입니다.")

                if score_gain > current_user.best_score:
                                    current_user.best_score = score_gain
        except KeyboardInterrupt:
            print("\n사용자에 의해 프로그램이 강제 종료되었습니다.")
        except EOFError:
            print("\n입력 스트림이 종료되었습니다. 프로그램을 종료합니다.")
        finally:
            self.save_data()
            print("\n프로그램을 안전하게 정리하고 종료하겠습니다.")
                
            self.save_data()
            print("=" * 40)
            print(f"현재 희득 중인 포인트: {score_gain} 점 , 최고 점수: {current_user.best_score} 점 ")
            print("=" * 40)
                
           
        print("=" * 40)
        print("\n퀴즈가 종료되었습니다!")
        print(f"이번 라운드 획득 포인트 : {score_gain}점,  최고 점수: {current_user.best_score} 점")
        print(f"지금까지 희득한 포인트 : {current_user.point}")
        print("=" * 40)
   
    def check_score_flow(self): 
        name = input("\n점수를 확인할 사용자를 입력해주세요: ").strip()
        user = self.find_user(name)
        if user:
            print(f"[{user.username}]님의 현재까지 쌓인 포인트 : {user.point} , 최고 점수: {user.best_score}점 입니다.")
        else:
            print(f"[{name}]님은 등록되지 않은 사용자입니다. 먼저 사용자 등록을 해주세요!")
            return
        
    def quiz_list(self): 
        print("\n---[ 퀴즈 목록 ]---")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.\n")
            return
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx}. 문제 {quiz.question} \n정답 : 비밀입니다!")


    def register_user_flow(self): 
           new_name = input("\n등록할 사용자 이름을 입력해주세요 : ").strip()
   
           if not new_name:
               print("이름은 빈 칸일 수 없습니다.")
               return
   
           if self.register_user(new_name) is False :
               print(f"\n[{new_name}]님은 이미 등록된 사용자입니다.")
   
           else:
               print(f"\n[{new_name}]님이 새로 등록되었습니다!")
 
    def show_users_flow(self):
        print("\n ---[사용자 목록]---")
        if not self.users:
            print("\n 등록된 사용자가 없습니다.")
            return
        for idx, user in enumerate(self.users,1):
            print(f"{idx}. {user.username} (최고 점수 :  {user.best_score})점")

    def add_quiz_flow(self):
        question = input("\n추가할 문제를 입력하세요 : ").strip()
        if not question:
            print("문제는 빈 칸일 수 없습니다")
            return

        choices = []
        for i in range(4):
            choice=input(f"{i+1}번 선지를 입력하세요 : ").strip()
            choices.append(choice)
        answer = input("\n정답을 입력하세요 : ").strip()

        if answer not in choices:
            print("\n정답은 반드시 선지 중 하나여야 합니다!")
            print("퀴즈 추가가 중단되었습니다.")
            return
        
        self.add_quiz(question, choices, answer)
        print(f"\n퀴즈가 추가되었습니다! 문제: {question}, 정답: {answer}")

   
            
if __name__ == "__main__":
    quizGame = QuizGame()
    quizGame.run()


