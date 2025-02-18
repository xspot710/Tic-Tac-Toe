from PIL import Image, ImageDraw, ImageFont


class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'O'

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            if self.current_player == 'X':
                self.current_player = 'O'
            else:
                self.current_player = 'X'

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        if ' ' not in self.board:
            return 'Draw'
        return None

    def display(self):
        for i in range(0, 9, 3):
            print(self.board[i] + '|' + self.board[i+1] + '|' + self.board[i+2])
            if i < 6:
                print('-+-+-')

    def available_moves(self):
        if self.check_winner():
            return []
        return [i for i, x in enumerate(self.board) if x == ' ']


    def undo_move(self, position):
        self.board[position] = ' '
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'


    def display_to_image(self, file_name):
        img = Image.new('RGB', (300, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # 绘制棋盘
        for i in range(1, 3):
            d.line([i * 100, 0, i * 100, 300], fill=(0, 0, 0), width=2)
            d.line([0, i * 100, 300, i * 100], fill=(0, 0, 0), width=2)

        # 绘制棋子
        for i, cell in enumerate(self.board):
            x = (i % 3) * 100
            y = (i // 3) * 100
            if cell == 'O':
                # 画蓝色圆圈
                d.ellipse([x + 10, y + 10, x + 90, y + 90], outline="blue", width=5)
            elif cell == 'X':
                # 画红色叉号
                d.line([x + 10, y + 10, x + 90, y + 90], fill="red", width=5)
                d.line([x + 90, y + 10, x + 10, y + 90], fill="red", width=5)

        # 保存图像
        img.save(f'images/{file_name}.png')

    def display_to_image_title(self, file_name, title):
        # 创建原始棋盘图像
        board_img = Image.new('RGB', (300, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(board_img)

        # 绘制棋盘
        for i in range(1, 3):
            d.line([i * 100, 0, i * 100, 300], fill=(0, 0, 0), width=2)
            d.line([0, i * 100, 300, i * 100], fill=(0, 0, 0), width=2)

        # 绘制棋子
        for i, cell in enumerate(self.board):
            x = (i % 3) * 100
            y = (i // 3) * 100
            if cell == 'O':
                # 画蓝色圆圈
                d.ellipse([x + 10, y + 10, x + 90, y + 90], outline="blue", width=5)
            elif cell == 'X':
                # 画红色叉号
                d.line([x + 10, y + 10, x + 90, y + 90], fill="red", width=5)
                d.line([x + 90, y + 10, x + 10, y + 90], fill="red", width=5)

        # 创建更大的图像用于包含标题和棋盘
        total_height = board_img.height + 50 
        img_with_title = Image.new('RGB', (board_img.width, total_height), color=(255, 255, 255))
        
        d = ImageDraw.Draw(img_with_title)
  
        title_position = (board_img.width // 2 - len(title) * 3, 20) 
        d.text(title_position, title, fill=(0, 0, 0))

        img_with_title.paste(board_img, (0, 50))

        # 保存图像
        img_with_title.save(f'images/{file_name}.png')