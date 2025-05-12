from insight import Insight
import json
from datetime import datetime


class InsightManager:
    def __init__(self):
        self.insights = []

    def add_insight(self, insight):
        if not isinstance(insight, Insight):
            raise ValueError("ההכנסה חייבת להיות של תובנה")
        self.insights.append(insight)
    
    def update_insight(self, insight_id, **kwargs):
        if isinstance(insight_id, Insight):
            for i, ins in enumerate(self.insights):
                if insight_id.id == ins.id:
                    self.insights[i] = insight_id  # כאן שמים את האובייקט המלא!
                    print(f"Insight {insight_id.id} fully updated")
                    return
            print(f"Didnt found {insight_id.id} insight for fullu update")    

        else:
            # כאן מניחים ש־insight_id הוא מזהה id
            for ins in self.insights:
                if insight_id == ins.id:
                    for key, value in kwargs.items():
                        if hasattr(ins, key):
                            setattr(ins, key, value)
                    print(f"Insight {ins.id} partial updated") 
                    return
            print(f"Didnt found {insight_id} insight for partial update")  

                       
    def remove_insight(self, id):
        for ins in self.insights:
            if id == ins.id: 
                self.insights.remove(ins)
                print(f"Removed insight: {ins.id}")
                return 
        print(f"No insight found with id: {id}")

    def list_insights(self, limit=None):
        print(f"DEBUG: מספר התובנות במנהל: {len(self.insights)}") 
        for i, ins in enumerate(self.insights):
            if limit and i >= limit:
                print("...המשך קיים אך לא מוצג")
                break
            print(f"\n📌 {ins.id} {ins.title} ({ins.date})")
            print(f"🔖 {', '.join(ins.tags) if ins.tags else 'empty tags'}")
            print(f"✏️ {ins.subtitle}")


    def search_by_title(self, keyword):  
        return [ins for ins in self.insights if keyword.lower() in ins.title.lower()]

    def search_by_content(self, keyword):
        return [ins for ins in self.insights if keyword.lower() in ins.content.lower()]

    def search_by_tag(self, tag):
        return [ins for ins in self.insights if ins.tags and tag in ins.tags]

    def sort_by_date(self):
        return sorted(self.insights, key=lambda x: x.date)

    def search_by_date_range(self, start_date, end_date):
        def parse(d): return datetime.strptime(d, "%Y-%m-%d")
        start = parse(start_date)
        end = parse(end_date)
        return [ins for ins in self.insights if start <= parse(ins.date) <= end]

    def save(self, filename="insights.json"):
        data = [insight.to_dict() for insight in self.insights]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
 

    def load(self, filename="insights.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.insights = [Insight.from_dict(item) for item in data]
        except FileNotFoundError:
            print("⚠️ קובץ לא נמצא, מתחילים עם רשימה ריקה.")
            self.insights = []

    def get_insight_by_id(self, id):
        for ins in self.insights:
            if ins.id == id:
                return ins
        return None    
    
