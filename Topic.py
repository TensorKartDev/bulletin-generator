class Topic:
    def __init__(self, title, path, most_recent_file, most_recent_time):
        self.title = title  # Title or name of the topic
        self.path = path    # File path to the topic's content (e.g., a PDF file)
        self.most_recent_file = most_recent_file
        self.most_recent_time = most_recent_time
        print(self.most_recent_file)
        if self.most_recent_file == None:
            self.next_file_index = 0 + 1
        else:
            self.next_file_index = int(self.most_recent_file.split(".")[0]) + 1

    def __repr__(self):
        return f"Topic(title={self.title}, path={self.path}, most_recent_file={self.most_recent_file}, most_recent_time= {self.most_recent_time})"
