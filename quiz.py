import json

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
        

class Quizgame:
    def __init__(self, data_file: str ="state.json"):
        self.data_file = data_file
        self.quizzes = []
        self.users = []

    def run(self):
        while True:
            input_menu = input("메뉴를 선택하세요: ").strip()

            if input_menu == "1":
                self.start_quiz()
            elif input_menu == "2":
                self.register_user()
            elif input_menu == "3":
                self.show_users()
            elif input_menu == "4":
                self.check_score()
            elif input_menu == "5":
                print("\n프로그램을 종료합니다.")
                break
            elif input_menu == "6":
                self.add_quiz()
            elif input_menu == "7":
                self.quiz_list()
            else:
                print("\n잘못된 입력입니다. 1~7번 사이의 숫자를 입력해주세요.")
            
            
        


