import re
import os

def fix_profile_urls():
    fixed_count = 0
    
    # Проверяем все HTML файлы
    for root, dirs, files in os.walk('.'):
        if 'venv' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Ищем все теги с 'profile'
                    if 'profile' in content:
                        # Заменяем {% url 'profile' %} на /users/profile/
                        new_content = re.sub(
                            r"{%\s*url\s+['\"]profile['\"]\s*%}",
                            "/users/profile/",
                            content
                        )
                        
                        if new_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            fixed_count += 1
                            print(f"Исправлен: {filepath}")
                            
                except Exception as e:
                    print(f"Ошибка в {filepath}: {e}")
    
    return fixed_count

if __name__ == "__main__":
    print("Исправление тегов с 'profile'...")
    fixed = fix_profile_urls()
    print(f"✅ Исправлено файлов: {fixed}")