#!/usr/bin/env python3
import re
import json

class AICoreFilter:
    def __init__(self):
        # Расширенная база знаний фундаментальных законов и паттернов по дисциплинам
        self.disciplines_keywords = {
            "Ядерная физика": [r"плазм", r"термояд", r"реактор", r"аорт", r"магнитн.*пол", r"токамак"],
            "Органическая химия": [r"полимер", r"молекул", r"синтез", r"углерод", r"абсорб", r"кристалл"],
            "Микробиология": [r"бактери", r"штамм", r"клетк", r"биомасс", r"синапс"],
            "Экология": [r"пластик", r"океан", r"загрязн", r"почв", r"гумус", r"эрози"],
            "Гидродинамика": [r"поток", r"течен", r"жидкост", r"фильтр", r"навье-стокс", r"давлен"],
            "Квантовая физика": [r"квант", r"суперпозиц", r"запутан", r"кубит", r"полупроводник", r"фотон"],
            "Космическая механика": [r"орбит", r"гравитац", r"ионн.*двигател", r"терраформ", r"ракета", r"траектори"],
            "Геоинженерия": [r"климат", r"атмосфер", r"альбедо", r"аэрозол", r"опреснен", r"улавливан.*co2"]
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
        """Этап 2: Поиск междисциплинарной тождественности и синергии"""
        synergies = []
        
        # Контур 1: Очистка Океана (Репер 3)
        if "Гидродинамика" in detected_tags and "Экология" in detected_tags:
            synergies.append("Взаимосвязь макро-потоков: Применимо для Репера 3 (Очистка океана от микропластика).")
            
        # Контур 2: Регенерация Почв (Репер 1)
        if "Органическая химия" in detected_tags and "Микробиология" in detected_tags:
            synergies.append("Биомиметический контур: Применимо для Репера 1 (Регенерация гумусового слоя).")
            
        # Контур 3: Космическая энергетика и новые материалы (Вектор Экспансии)
        if "Квантовая физика" in detected_tags and "Космическая механика" in detected_tags:
            synergies.append("Контур Экспансии: Разработка квантовых датчиков ориентации и ионных двигателей нового поколения.")
            
        # Контур 4: Управление планетарным климатом (Вектор Стабилизации)
        if "Геоинженерия" in detected_tags and "Ядерная физика" in detected_tags:
            synergies.append("Контур Стабилизации: Использование энергии ТЯС для глобальных комплексов прямого улавливания углерода (CO2).")
            
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

# Запуск тестов на междисциплинарных моделях
if __name__ == "__main__":
    ai_core = AICoreFilter()
    
    # Тест 1: Экологический проект
    test_title_1 = "Система очистки Тихого океана"
    test_text_1 = "Использование законов гидродинамики и уравнений Навье-Стокса для улавливания частиц микропластика в океанических течениях через каскадные фильтры."
    print("--- ТЕСТ 1 ---")
    print(ai_core.process_project(test_title_1, test_text_1))
    
    # Тест 2: Космический проект нового поколения
    test_title_2 = "Ионный двигатель на квантовых кубитах"
    test_text_2 = "Расчет оптимальной траектории и коррекции орбиты космических аппаратов с использованием ионного двигателя, стабилизируемого квантовыми матрицами суперпозиции."
    print("\n--- ТЕСТ 2 ---")
    print(ai_core.process_project(test_title_2, test_text_2))
