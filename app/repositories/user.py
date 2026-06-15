class UserRepository:

    def __init__(self):
        self.users = []
        self.next_id = 1


    def create(self, user_data: dict):
        user = {
            "id": self.next_id,
            **user_data
        }

        self.next_id += 1

        self.users.append(user)

        return user


    def get_all(self):
        return list(self.users)


    def get_by_id(self, user_id: int):
        for user in self.users:
            if user["id"] == user_id:
                return user

        return None


    def update(self, user_id: int, user_data: dict):
        user = self.get_by_id(user_id)

        if not user:
            return None

        user.update(user_data)

        return user


    def delete(self, user_id: int):
        user = self.get_by_id(user_id)

        if not user:
            return False

        self.users.remove(user)

        return True