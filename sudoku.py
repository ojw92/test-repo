import streamlit as st
import numpy as np
import time

# Function to generate a new Sudoku puzzle
def generate_puzzle():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return np.random.permutation(s)

    r_base = range(base)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    for i in range(side):
        for j in range(side):
            if np.random.random() < 0.8:
                board[i][j] = 0

    return board

# Function to check if the Sudoku is solved
def is_solved(board):
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num:
                return False

        for x in range(9):
            if board[x][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False

        return True

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
            if not is_valid(board, i, j, board[i][j]):
                return False

    return True

# Function to draw the Sudoku board
def draw_board(board, mode):
    edited_board = board.copy()
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            with cols[j]:
                if board[i][j] == 0:
                    if mode == 'Guess':
                        edited_board[i][j] = st.number_input('', min_value=1, max_value=9, key=f'{i}-{j}')
                    elif mode == 'Candidates':
                        edited_board[i][j] = st.text_input('', key=f'{i}-{j}')
                    elif mode == 'Delete':
                        edited_board[i][j] = st.text_input('', key=f'{i}-{j}')
                else:
                    st.text(board[i][j])
    return edited_board

# Main function to run the Streamlit app
def main():
    st.title("Sudoku Game")
    st.sidebar.title("Game Controls")

    start_game = st.sidebar.button("Start New Game")
    mode = st.sidebar.radio("Mode", ['Guess', 'Candidates', 'Delete'])

    if start_game:
        st.session_state['board'] = generate_puzzle()
        st.session_state['start_time'] = time.time()

    if 'board' not in st.session_state:
        st.session_state['board'] = generate_puzzle()
        st.session_state['start_time'] = time.time()

    if is_solved(st.session_state['board']):
        st.success("Congratulations! You solved the puzzle.")
        st.balloons()

    current_time = time.time()
    elapsed_time = current_time - st.session_state['start_time']
    st.sidebar.write(f'Time Elapsed: {int(elapsed_time // 60)}:{int(elapsed_time % 60):02d}')

    st.write("Sudoku Board:")
    st.session_state['board'] = draw_board(st.session_state['board'], mode)

if __name__ == "__main__":
    main()
