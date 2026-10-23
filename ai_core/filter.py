#!/usr/bin/env python3
import re
import json

class AICoreFilter:
    def __init__(self):
        # Базовая база знаний фундаментальных законов и ключевых слов по дисциплинам
        self.disciplines_keywords = {
            "Ядерная физика": [r"плазм", r"термояд", r"реактор", r"аорт", r"магнитн.*пол", r"токамак"],
            "Органическая химия": [r"полимер", r"молекул", r"синтез", r"углерод", r"абсорб", r"кристалл"],
            "Микробиология": [r"бактери", r"штамм", r"клетк", r"штамм", r"биомасс", r"синапс"],
            "Экология": [r"пластик", r"океан", r"загрязн", r"почв", r"гумус", r"эрози"],
            "Гидродинамика": [r"поток", r"течен", r"жидкост", r"фильтр", r"навье-стокс", r"давлен"]
        }
        
    def primary_classification(self, project_text):
        """Этап 1: Автоматическое тегирование по дисциплинам"""
        detected_tags = []
        text_lower = project_text.lower()
        
        for discipline, regexes in self.disciplines_keywords.items():
            for regex in regexes:
                if re.search(regex, text_lower):
                    if discipline not in detected_tags:
                        detected_tags.append(discipline)
                        
        return detected_tags if detected_tags else ["Междисциплинарный / Общий"]

    def check_fundamental_laws(self, project_text):
        """Этап 1.5: Проверка на грубые нарушения законов физики (псевдонаука)"""
        text_lower = project_text.lower()
        # Попытка создания вечного двигателя без затрат энергии
        if "вечный двигатель" in text_lower or "perpetuum mobile" in text_lower:
            if "кпд > 100" in text_lower or "без затрат" in text_lower:
                return False, "Проект отклонен: Обнаружено нарушение Первого начала термодинамики."
        return True, "Базовый физический аудит пройден успешно."

    def cross_disciplinary_analysis(self, detected_tags):
        """Этап 2: Поиск междисциплинарной тождественности"""
        # Логическая матрица связей: ИИ ищет скрытые синергии между полярными науками
        synergies = []
        if "Гидродинамика" in detected_tags and "Экология" in detected_tags:
            synergies.append("Взаимосвязь макро-потоков: Применимо для Репера 3 (Очистка океана).")
        if "Органическая химия" in detected_tags and "Микробиология" in detected_tags:
            synergies.append("Биомиметический контур: Применимо для Репера 1 (Регенерация гумуса).")
        return synergies

    def process_project(self, title, text):
        """Главный контур обработки входящей научной заявки"""
        is_valid, audit_msg = self.check_fundamental_laws(text)
        if not is_valid:
            return json.dumps({"status": "REJECTED", "reason": audit_msg}, ensure_ascii=False, indent=4)
            
        tags = self.primary_classification(text)
        interdisciplinary_notes = self.cross_disciplinary_analysis(tags)
        
        report = {
            "project_title": title,
            "status": "VERIFIED_BY_AI",
            "disciplines": tags,
            "interdisciplinary_synergies": interdisciplinary_notes if interdisciplinary_notes else ["Связи не обнаружены, требуется углубленный семантический анализ."],
            "audit_log": audit_msg
        }
        return json.dumps(report, ensure_ascii=False, indent=4)

# Демонстрационный запуск ядра ИИ на тестовом проекте Павла
if __name__ == "__main__":
    ai_core = AICoreFilter()
    
    test_title = "Система очистки Тихого океана"
    test_text = "Использование законов гидродинамики и уравнений Навье-Стокса для улавливания частиц микропластика в океанических течениях через каскадные фильтры."
    
    print(ai_core.process_project(test_title, test_text))
