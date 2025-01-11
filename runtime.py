import sys

class MLL:
    def __init__(self):
        self.data = [0]*64

    def toNumber(self, code):
        tokens = code.split(' ')
        result = 1
        for token in tokens:
            if token.isdigit():
                num = int(token)  # Convert the token to an integer
            elif token.startswith('어') or token.startswith('엄'):
                # Determine the base value based on '어' and '엄'
                index = token.count('어')  # Count '어' occurrences before '엄'
                base_value = 0  # Default to 0 for assignment
                if '.' in token or ',' in token:
                    adjustment = token.count('.') - token.count(',')
                    base_value += adjustment  # Adjust the base value
                num = base_value
            else:
                raise SyntaxError(f"Invalid token: {token}")
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
        if '선포' in code and '!!' in code:
            return 'PRINT'
        if '선포!' in code and '쩝' in code:
            return 'PRINTASCII'
        if '엄' in code:
            return 'DEF'
        if code.startswith('어'):
            return 'SET'
        if code.startswith('계'):
            return 'USE'

    def compileLine(self, code):
        if code == '':
            return None
        TYPE = self.type(code)
        
        if TYPE == 'DEF':
            var, value = code.split('엄')
            var = var.strip()  # Remove whitespace
            value = value.strip()

            # Calculate the index based on '계' and '어'
            index = var.count('어')
            self.data[index] = self.toNumber(value)  # Assign the value to data[index]
        elif TYPE == 'END':
            print(self.toNumber(code.split('탄핵!')[1]), end='')
            sys.exit()
        elif TYPE == 'INPUT':
            self.data[code.replace('선포?', '').count('어')] = int(input())
        elif TYPE == 'PRINT':
        # If '선포!' with no arguments, print all non-zero elements in self.data
            if code.strip() == '선포!!':
                for value in self.data:
                    if value != 0:
                        print(value, end=' ')
                print()  # Add a newline after printing all values
            else:
                # Handle other print cases
                print(self.toNumber(code[1:-1]), end='')
        elif TYPE == 'PRINTASCII':
            # Handle '선포!쩝' to print ASCII characters
            if code.strip() == '선포!쩝':
                for value in self.data:
                    if value != 0:
                        print(chr(value), end='')  # Print non-zero values as ASCII characters
                print()  # Add a newline after printing all characters
            else:
                # Handle cases where specific ASCII values are passed
                value = self.toNumber(code.replace('선포!쩝', '').strip())
                if value:
                    print(chr(value), end='')
        elif TYPE == 'IF':
            cond, cmd = code.replace('내란', '').split('?')
            if self.toNumber(cond) == 0:
                return cmd
        elif TYPE == 'MOVE':
            return self.toNumber(code.replace('윤', ''))

    def compile(self, code, check=True, errors=100000):
        yoon = False
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
            if yoon:
                jun = False
                code[index] = recode                
            if isinstance(res, int):
                index = res-2
            if isinstance(res, str):
                recode = code[index]
                code[index] = res
                index -= 1
                yoon = True

            index += 1
            error += 1
            if error == errors:
                raise RecursionError(str(errorline+1) + '번째 줄에서 무한 루프가 감지되었습니다.')

    def compilePath(self, path):
        with open(path) as file:
            code = ''.join(file.readlines())
            self.compile(code)