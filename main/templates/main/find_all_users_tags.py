import os
import re

def find_users_tags():
    found_files = []
    
    # Ищем во всех файлах проекта
    for root, dirs, files in os.walk('.'):
        # Пропускаем системные папки
        skip_dirs = ['venv', '__pycache__', '.git', '.idea', 'node_modules']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            # Проверяем все текстовые файлы
            if file.endswith(('.html', '.htm', '.txt', '.js', '.py')):
                filepath = os.path.join(root, file)
                
                try:
                    # Пробуем разные кодировки
                    for encoding in ['utf-8', 'cp1251', 'latin-1']:
                        try:
                            with open(filepath, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        continue
                    
                    # Ищем теги с users:
                    if re.search(r'users:', content):
                        # Находим конкретные вхождения с контекстом
                        lines = content.split('\n')
                        matches = []
                        for i, line in enumerate(lines):
                            if 'users:' in line:
                                # Показываем 3 строки контекста
                                start = max(0, i-1)
                                end = min(len(lines), i+2)
                                context = '\n'.join(f'{j+1}: {lines[j]}' for j in range(start, end))
                                matches.append((i+1, context))
                        
                        found_files.append({
                            'path': filepath,
                            'matches': matches
                        })
                        
                except Exception:
                    pass
    
    return found_files

if __name__ == "__main__":
    print("🔍 Поиск ВСЕХ тегов с 'users:' в проекте...")
    results = find_users_tags()
    
    if results:
        print(f"\n⚠️  Найдено {len(results)} файлов с тегами 'users:':")
        for result in results:
            print(f"\n📁 ФАЙЛ: {result['path']}")
            print("─" * 80)
            for line_num, context in result['matches']:
                print(f"Строка {line_num}:")
                print(context)
                print("-" * 40)
                
            # Автоматическое исправление для HTML файлов
            if result['path'].endswith('.html'):
                fix = input(f"\nИсправить {result['path']}? (y/n): ")
                if fix.lower() == 'y':
                    try:
                        with open(result['path'], 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Заменяем все {% url 'users:xxx' %} на {% url 'xxx' %}
                        new_content = re.sub(
                            r"{%\s*url\s+['\"]users:([^'\"]+)['\"]\s*%}",
                            r"{% url '\1' %}",
                            content
                        )
                        
                        with open(result['path'], 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print("✅ Исправлено!")
                    except Exception as e:
                        print(f"❌ Ошибка: {e}")
    else:
        print("✅ Тегов с 'users:' не найдено!")