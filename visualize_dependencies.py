import os
import subprocess
import argparse

def get_commit_files(repo_path, branch_name):
    """Получить список файлов из всех коммитов в заданной ветке."""
    os.chdir(repo_path)

    # Получаем список коммитов и связанных с ними файлов
    commit_files = subprocess.check_output(
        ["git", "log", "--name-only", "--pretty=format:%H", branch_name],
        encoding='utf-8'
    ).strip().split('\n\n')
    print(commit_files)
    files_dict = {}
    current_commit = None

    for line in commit_files:
        line = line.strip().split('\n')

        files_dict[line[0]] = line[1:]  # Инициализация списка для файлов этого коммита

    print("Список файлов из коммитов:", files_dict)  # Отладочное сообщение
    return files_dict


def generate_plantuml_graph(files_dict):
    """Генерирует строку PlantUML для визуализации графа зависимостей."""
    plantuml_graph = "@startuml\n"

    for commit, files in files_dict.items():
        for file in files:
            plantuml_graph += f'"{commit}" --> "{file}"\n'

    plantuml_graph += "@enduml"
    return plantuml_graph

def save_plantuml_graph(plantuml_graph, output_path):
    """Сохраняет граф PlantUML в файл."""
    with open('graph.puml', 'w') as f:
        f.write(plantuml_graph)

    # Генерация изображения из PlantUML
    subprocess.run(["java", "-jar", "d:/dz2/plantuml.jar", 'graph.puml'], check=True)

    # Перемещение файла PNG в указанный выходной путь
    os.rename('graph.png', output_path)

def main():
    parser = argparse.ArgumentParser(description='Visualize Git repository dependency graph.')
    parser.add_argument('path_to_plantuml', type=str, help='Path to PlantUML JAR file.')
    parser.add_argument('path_to_repo', type=str, help='Path to the Git repository.')
    parser.add_argument('output_file', type=str, help='Output file path for the dependency graph image.')
    parser.add_argument('branch_name', type=str, help='Branch name in the repository.')
    args = parser.parse_args()

    # Получение файлов из коммитов ветки
    files_dict = get_commit_files(args.path_to_repo, args.branch_name)

    # Генерация графа PlantUML
    plantuml_graph = generate_plantuml_graph(files_dict)

    print("Содержимое graph.puml:")
    print(plantuml_graph)

    # Сохранение и генерация графа
    save_plantuml_graph(plantuml_graph, args.output_file)

    print("Граф зависимостей успешно сгенерирован и сохранен в:", args.output_file)

if __name__ == "__main__":
    main()
