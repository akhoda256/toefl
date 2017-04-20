class AnswerHistory(object):
    def __init__(self):
        print('Create Answer History')
        self.questionNum = 0
        self.tpoNum = 0
        self.passageNum = 0
        self.answer = 0


class State(object):
    def __init__(self):
        print('create state object')
        self.currentQuestion = 0
        self.history = []
