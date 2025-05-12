from datetime import datetime
import json

class Insight:
    counter = 1
    def __init__(self, title, subtitle, content, tags=None, date=None, id=None, connections=None):

        self.id = id if id is not None else Insight.counter 
        Insight.counter = max(Insight.counter, self.id + 1) 

        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.tags = list(tags) if tags else []
        self.connections = list(connections) if connections else []

    def __str__(self):
         return f"{self.id} - {self.title} – {self.subtitle}\n{self.content}\n({self.date}\n{self.connections})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
        'id': self.id,
        'title': self.title,
        'subtitle': self.subtitle,
        'content': self.content,
        'tags': self.tags,
        'date': self.date,
        'connections': self.connections    
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            subtitle=data.get("subtitle"),
            content=data.get("content"),
            tags=data.get("tags"),
            date=data.get("date"),
            connections=data.get("connections")  
        )
   