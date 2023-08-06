class Common:
    @staticmethod
    def limit(data, limit):
        if not limit or len(data) <= limit:
            return data
        else:
            return data[0:limit]
