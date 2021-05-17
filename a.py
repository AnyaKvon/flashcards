from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String(100))
    answer = Column(String(50))
    status = Column(Integer, default=0)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# write your code here
def error(par):
    return par + ' is not an option'


def leitner(q):
    while True:
        print('''press "y" if your answer is correct:
press "n" if your answer is wrong:''')
        ans = input()
        if ans not in ['y', 'n']:
            error(ans)
        else:
            break
    if ans == 'y':
        if q.status != 2:
            q.status += 1
            session.commit()
        else:
            session.delete(q)
            session.commit()
    elif ans == 'n':
        if q.status != 0:
            q.status -= 1
            session.commit()


def add_question():

    while True:
        print('Question:')
        ques = input()
        if ques:
            break
    while True:
        print('Answer:')
        ans = input()
        if ans:
            new = Flashcard(question=ques, answer=ans)
            session.add(new)
            session.commit()
            break
    return True


def create_cards():
    while True:
        print('''1. Add a new flashcard
2. Exit''')
        ans = input()
        if ans == '1':
            add_question()
        elif ans == '2':
            break
        else:
            print(error(ans))
    return True


def update_flash(q):
    print('''press "d" to delete the flashcard:
press "e" to edit the flashcard:''')
    ans = input()
    if ans == 'd':
        session.delete(q)
        session.commit()
    elif ans == 'e':
        print(f'''current question: {q.question}
please write a new question: ''')
        q.question = input()
        session.commit()
        print(f'''current answer: {q.answer}
please write a new answer:''')
        q.answer = input()
        session.commit()
    else:
        error(ans)


def practice():
    result_list = session.query(Flashcard).all()
    if not result_list:
        print('There is no flashcard to practice!')
    else:
        for q in result_list:
            print(f'Question: {q.question}')
            print('''press "y" to see the answer:
press "n" to skip:
press "u" to update:''')
            ans = input()
            if ans == 'y':
                print(f'Answer: {q.answer}')
                leitner(q)
            elif ans == 'n':
                leitner(q)
                continue
            elif ans == 'u':
                update_flash(q)
            else:
                print(error(ans))


def menu():
    while True:
        print('''1. Add flashcards
2. Practice flashcards
3. Exit''')
        ans = input()
        if ans == '1':
            create_cards()
        elif ans == '2':
            practice()
        elif ans == '3':
            print('Bye!')
            break
        else:
            print(error(ans))

menu()