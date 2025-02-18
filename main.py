from TTT.tictactoe import TicTacToe
from qlearning import QLearning
from tqdm import tqdm
import json
import pickle

qlearning_circle = QLearning()
qlearning_cross = QLearning()

# qlearning_circle.load_q_table('circle.pkl')
# qlearning_cross.load_q_table('cross.pkl')

# 關注的局面
interesting_states = [
    ([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], qlearning_circle),
    (['O', 'O', 'X', ' ', 'X', ' ', ' ', ' ', ' '], qlearning_circle),
    (['O', 'O', 'X', 'O', 'X', ' ', ' ', ' ', ' '], qlearning_cross)
]
# 用於儲存感興趣的 Q 值變化
q_values_interesting_states = {}
# 用於儲存第一步的落點變化
q_values_first_step = {}
# 儲存勝率的資料結構
win_rate_data = {}

total_games = 0
circle_wins = 0
cross_wins = 0

r1 = 1
r2 = 0.6
r3 = 0.45
r4 = 0.2
r5 = 0.1

total_i = 50000000
# 每m次迭代記錄一次勝率
m = int(total_i/1000)
# 每n次 記錄一次模型
n_m = int(total_i/25)

qlearning_circle.er = r1
qlearning_cross.er = r1
qlearning_circle.min_er = r2
qlearning_cross.min_er = r2
stage = 1

for i in tqdm(range(total_i)):
    game = TicTacToe()
    
    new_state_circle = None
    new_state_cross = None

    # 根據進行用不同的er來訓練
    progress = i / total_i
    # 檢查當前訓練階段並更新探索率

    if stage == 1 and progress >= 0.5:
        qlearning_circle.er = r2
        qlearning_cross.er = r2
        qlearning_circle.min_er = r3
        qlearning_cross.min_er = r3
        stage = 2
    elif stage == 2 and progress >= 0.75:
        qlearning_circle.er = r3
        qlearning_cross.er = r3
        qlearning_circle.min_er = r4
        qlearning_cross.min_er = r4
        stage = 3
    elif stage == 3 and progress >= 9.0:
        qlearning_circle.er = r4
        qlearning_cross.er = r4
        qlearning_circle.min_er = r5
        qlearning_cross.min_er = r5
        stage = 4


    while game.check_winner() is None:
        available_actions = game.available_moves()
        player = game.current_player
        reward = 0
        if player == 'O':
            old_state_circle = new_state_circle
            new_state_circle = game.board.copy()
            action_circle_new = qlearning_circle.choose_action(tuple(game.board), available_actions)
            game.make_move(action_circle_new)
            if old_state_circle is not None:
                qlearning_circle.learn(old_state_circle, action_circle_old, reward, new_state_circle, available_actions)
            action_circle_old = action_circle_new

        else:
            old_state_cross = new_state_cross
            new_state_cross = game.board.copy()
            action_cross_new = qlearning_cross.choose_action(tuple(game.board), available_actions)
            game.make_move(action_cross_new)
            if old_state_cross is not None:
                qlearning_cross.learn(old_state_cross, action_cross_old, reward, new_state_cross, available_actions)
            action_cross_old = action_cross_new
    
    winner = game.check_winner()
    total_games += 1
    if winner == 'X':
        reward_cross = 50
        reward_circle = -100
        cross_wins += 1
    elif winner == 'O':
        reward_cross = -100
        reward_circle = 50
        circle_wins += 1
    else:
        reward_cross = 10
        reward_circle = -10

    qlearning_circle.learn(new_state_circle, action_circle_new, reward_circle, game.board.copy(), [])
    qlearning_cross.learn(new_state_cross, action_cross_new, reward_cross, game.board.copy(), [])

    if i % m == 0:
        ind = str(int(i/m))
        win_rate_data[ind] = {'O': round(circle_wins/total_games, 4), 'X': round(cross_wins/total_games, 4)}
        
        total_games = 0
        circle_wins = 0
        cross_wins = 0
        
        # 檢查並記錄感興趣的局面的 Q 值
        for state, ql in interesting_states:
            if state[4] == ' ':
                q_values_first_step['S_' + ind]  = {str(i):ql.get_q_value(state, i) for i in range(9)}
            else:
                temp_dict = {}
                if state[3] == ' ':
                    name = 'O_' + ind
                    temp_dict['3'] = ql.get_q_value(state, 3)
                else:
                    name = 'X_' + ind
                temp_dict['5'] = ql.get_q_value(state, 5)
                temp_dict['6'] = ql.get_q_value(state, 6)
                temp_dict['7'] = ql.get_q_value(state, 7)
                temp_dict['8'] = ql.get_q_value(state, 8)
                q_values_interesting_states[name]  = temp_dict

    if i % n_m == 0:
        qlearning_circle.save_q_table(f'model/{str(i)}_circle.pkl')
        qlearning_cross.save_q_table(f'model/{str(i)}_cross.pkl')

# 訓練後儲存數據
with open('win_rate_data.json', 'w') as f:
    json.dump(win_rate_data, f)

with open('q_values_interesting_states.json', 'w') as f:
    json.dump(q_values_interesting_states, f)

with open('q_values_first_step.json', 'w') as f:
    json.dump(q_values_first_step, f)


qlearning_circle.save_q_table('circle.pkl')
qlearning_cross.save_q_table('cross.pkl')
print(qlearning_cross.er)