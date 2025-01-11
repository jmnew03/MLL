import sys


class MLL:
    def __init__(self):
        self.data = [0]*256

    def toNumber(self, code):
        tokens = code.split(' ')
        result = 1
        for token in tokens:
            num = (self.data[token.count('계') + token.count('어') + token.count('엄') - 2] if (token.count('어') or token.count('계') or token.count('엄')) else 0) + token.count('.') - token.count(',')
            result *= num
        return result

    @staticmethod
    def type(code):
        if '내란' in code:
            return 'IF'
        if '윤' in code:
            return 'MOVE'
        if '탄핵!' in code:
            return 'END'
        if '선포' in code and '?' in code:
            return 'INPUT'
        if '선포' in code and '!' in code:
            return 'PRINT'
        if '선포' in code and '쩝' in code:
            return 'PRINTASCII'
        if '거' in code:
            return 'DEF'

    def compileLine(self, code):
        if code == '':
            return None
        TYPE = self.type(code)
        
        if TYPE == 'DEF':
            var, cmd = code.split('거')
            self.data[var.count('예')] = self.toNumber(cmd)
        elif TYPE == 'END':
            print(self.toNumber(code.split('탄핵!')[1]), end='')
            sys.exit()
        elif TYPE == 'INPUT':
            self.data[code.replace('선포?', '').count('어')] = int(input())
        elif TYPE == 'PRINT':
            print(self.toNumber(code[2:-1]), end='')
         # Add a newline after printing all values
        elif TYPE == 'PRINTASCII':
            value = self.toNumber(code[2:-1])
            print(chr(value) if value else '\n', end='')
        elif TYPE == 'IF':
            cond, cmd = code.replace('내란', '').split('?')
            if self.toNumber(cond) == 0:
                return cmd
        elif TYPE == 'MOVE':
            return self.toNumber(code.replace('윤', ''))

    def compile(self, code, check=True, errors=100000):
        jun = False
        recode = ''
        spliter = '\n' if '\n' in code else '~'
        code = code.rstrip().split(spliter)
        start_marker = code[0].strip()
        end_marker = code[-1].strip()
        if check and (
            start_marker != '존경하는 국민 여러분'
            or end_marker != '국민 여러분께 호소드립니다'
        ):
            raise SyntaxError('국민을 존경하는 마음을 가지십시오.')
        index = 0
        error = 0
        while index < len(code):
            errorline = index
            c = code[index].strip()
            res = self.compileLine(c)
            if jun:
                jun = False
                code[index] = recode                
            if isinstance(res, int):
                index = res-2
            if isinstance(res, str):
                recode = code[index]
                code[index] = res
                index -= 1
                jun = True

            index += 1
            error += 1
            if error == errors:
                raise RecursionError(str(errorline+1) + '번째 줄에서 무한 루프가 감지되었습니다.')

    def compilePath(self, path):
        with open(path) as file:
            code = ''.join(file.readlines())
            self.compile(code)