# Tic-Tac-Toe

Tic-Tac-Toe is a project that utilizes Q-Learning to train an agent to play Tic-Tac-Toe.  
The goal is to explore reinforcement learning techniques in turn-based games and implement model training, visualizing the learning process, and saving Q-tables.

## Project Structure

### Main Files

- **main.py**  
  - Runs Q-Learning to train the Tic-Tac-Toe agent.
  - Defines learning parameters such as `exploration rate (epsilon)`, `learning rate (alpha)`, and `discount factor (gamma)`.
  - Saves Q-table models at intervals during training.

- **TTT_training_video.ipynb**  
  - Uses `moviepy` to generate a video of the training process.
  - Reads Q-table models to simulate the game based on learned strategies.

### Related Directories

- **TTT_images/**  
  - Stores game images generated during the training process.

- **TTT_model/**  
  - Stores `.pkl` Q-Learning models from training to retain learning progress.

## Parameter Adjustments

The following parameters in `main.py` can be adjusted to influence the Q-Learning training behavior:

- `total_i`: Number of training iterations, affecting both training duration and effectiveness.  
- `er` (Exploration Rate): The probability of taking random actions, decreasing gradually from `1.0`.  
- `min_er`: The minimum exploration rate to ensure some level of randomness remains.  
- `alpha` (Learning Rate): Controls how quickly the Q-values are updated.  
- `gamma` (Discount Factor): Determines how future rewards influence current decisions.  
- `reward_cross` / `reward_circle`: Defines reward values for winning, losing, or drawing a game for both players.

To modify these, adjust the respective variables in `main.py` before running the training.

## Usage

### Train the Agent

Run the following command to start Q-Learning training:

```bash
python main.py
```

- The program will periodically save Q-tables in the `TTT_model/` directory.
- These saved models can be loaded later to continue training without starting from scratch.

### Generate Training Video

1. Open `TTT_training_video.ipynb`.
2. Ensure that `TTT_images/` contains game images generated during training.
3. Execute all cells in the notebook:
   - It will load the Q-tables from `TTT_model/`.
   - Simulate games using the trained model.
   - Generate an `.mp4` video to visualize the learning process.

## Project Purpose

This is a **side project** aimed at exploring reinforcement learning applications in turn-based games  
while also serving as an experimental platform for Q-Learning.  

The project was primarily developed by **Yen-Hsu.C**, with some AI-based suggestions from GPT-3.  
This is not an AI-generated project but rather a learning experience built through experimentation and implementation.

## License

This project is licensed under the **MIT License**.  
See the [`LICENSE`](./LICENSE) file for more details.
