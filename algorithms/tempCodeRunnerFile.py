def _hash_state(state: State):
        hash_value = 1 << 31
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                hash_value = hash_value << 2 | (2+state.board[coor_y][coor_x])
        hash_value = hash_value << 2 | (2+state.player)
        return hash_value