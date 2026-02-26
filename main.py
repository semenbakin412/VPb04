import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


class Task:
    ALLOWED_PRIORITIES = ("Low", "Medium", "High")

    def __init__(
        self,
        title: str,
        description: str,
        priority: str = "Medium",
        due_date: Optional[datetime] = None,
    ) -> None:
        if priority not in self.ALLOWED_PRIORITIES:
            raise ValueError(f"Недопустимый приоритет: {priority}")

        self._id: str = str(uuid.uuid4())
        self._title: str = title
        self._description: str = description
        self._is_done: bool = False
        self._priority: str = priority
        self._due_date: Optional[datetime] = due_date
        self._created_at: datetime = datetime.now()
        self._completed_at: Optional[datetime] = None

    # --- Свойства для доступа к приватным атрибутам ---
    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @property
    def is_done(self) -> bool:
        return self._is_done

    @property
    def priority(self) -> str:
        return self._priority

    @property
    def due_date(self) -> Optional[datetime]:
        return self._due_date

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def completed_at(self) -> Optional[datetime]:
        return self._completed_at

    # --- Методы ---
    def mark_as_done(self) -> None:
        self._is_done = True
        self._completed_at = datetime.now()

    def change_description(self, new_description: str) -> None:
        self._description = new_description

    def set_priority(self, new_priority: str) -> None:
        if new_priority not in self.ALLOWED_PRIORITIES:
            raise ValueError(
                f"Недопустимый приоритет: {new_priority}. Допустимые: {self.ALLOWED_PRIORITIES}"
            )
        self._priority = new_priority

    def update_due_date(self, new_due_date: Optional[datetime]) -> None:
        self._due_date = new_due_date

    def reopen(self) -> None:
        self._is_done = False
        self._completed_at = None

    def __repr__(self) -> str:
        status = "[x]" if self.is_done else "[ ]"
        due_str = self.due_date.strftime("%Y-%m-%d %H:%M") if self.due_date else "—"
        return (
            f"Task(id={self.id}, title={self.title!r}, status={status}, "
            f"priority={self.priority}, due={due_str})"
        )


class Project:
    def __init__(self, title: str, description: str = "") -> None:
        self._id: str = str(uuid.uuid4())
        self._title: str = title
        self._description: str = description
        self._created_at: datetime = datetime.now()
        self._tasks: List[Task] = []

    # --- Свойства ---
    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def tasks(self) -> List[Task]:
        return list(self._tasks)

    # --- Методы ---
    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return
        print("Задача не найдена")

    def get_tasks_by_status(self, is_done: bool) -> List[Task]:
        return [task for task in self._tasks if task.is_done == is_done]

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def __repr__(self) -> str:
        return f"Project(id={self.id}, title={self.title!r}, tasks={len(self._tasks)})"


class User:
    def __init__(self, username: str, full_name: str, email: str) -> None:
        self._id: str = str(uuid.uuid4())
        self._username: str = username
        self._full_name: str = full_name
        self._email: str = email
        self._created_at: datetime = datetime.now()
        self._projects: List[Project] = []

    # --- Свойства ---
    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def projects(self) -> List[Project]:
        return list(self._projects)

    # --- Методы ---
    def create_project(self, title: str, description: str = "") -> Project:
        project = Project(title=title, description=description)
        self._projects.append(project)
        return project

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        for project in self._projects:
            if project.id == project_id:
                return project
        return None

    def get_all_tasks(self) -> List[Task]:
        tasks: List[Task] = []
        for project in self._projects:
            tasks.extend(project.tasks)
        return tasks

    def get_overdue_tasks(self) -> List[Task]:
        now = datetime.now()
        overdue: List[Task] = []
        for task in self.get_all_tasks():
            if task.due_date is not None and not task.is_done and task.due_date < now:
                overdue.append(task)
        return overdue

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        return [task for task in self.get_all_tasks() if task.priority == priority]

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, username={self.username!r}, "
            f"projects={len(self._projects)})"
        )


# ---------------- CLI-приложение ----------------


def print_main_menu() -> None:
    print("\n--- Меню ---")
    print("1. Создать проект")
    print("2. Показать проекты")
    print("3. Создать задачу в проекте")
    print("4. Показать задачи проекта")
    print("5. Отметить задачу как выполненную")
    print("6. Показать все задачи пользователя")
    print("7. Показать просроченные задачи")
    print("8. Показать задачи по приоритету")
    print("0. Выход")


def choose_project(user: User) -> Optional[Project]:
    if not user.projects:
        print("У пользователя нет проектов.")
        return None

    print("\nСписок проектов:")
    for idx, project in enumerate(user.projects, start=1):
        print(f"{idx}. {project.title} (id={project.id})")

    choice = input("Выберите номер проекта: ").strip()
    if not choice.isdigit():
        print("Некорректный ввод.")
        return None

    index = int(choice) - 1
    if index < 0 or index >= len(user.projects):
        print("Проект с таким номером не найден.")
        return None

    return user.projects[index]


def choose_task(project: Project) -> Optional[Task]:
    if not project.tasks:
        print("В проекте нет задач.")
        return None

    print("\nСписок задач:")
    for idx, task in enumerate(project.tasks, start=1):
        status = "[x]" if task.is_done else "[ ]"
        print(f"{idx}. {task.title} (id={task.id}, статус={status})")

    choice = input("Выберите номер задачи: ").strip()
    if not choice.isdigit():
        print("Некорректный ввод.")
        return None

    index = int(choice) - 1
    if index < 0 or index >= len(project.tasks):
        print("Задача с таким номером не найдена.")
        return None

    return project.tasks[index]


def cli_app() -> None:
    print("Добро пожаловать в систему управления задачами!")
    username = input("Введите логин пользователя: ").strip()
    full_name = input("Введите полное имя пользователя: ").strip()
    email = input("Введите email пользователя: ").strip()

    user = User(username=username, full_name=full_name, email=email)
    print(f"\nПользователь создан: {user}")

    while True:
        print_main_menu()
        command = input("Выберите пункт меню: ").strip()

        if command == "1":
            title = input("Название проекта: ").strip()
            description = input("Описание проекта (можно оставить пустым): ").strip()
            project = user.create_project(title=title, description=description)
            print(f"Проект создан: {project}")

        elif command == "2":
            if not user.projects:
                print("У пользователя пока нет проектов.")
            else:
                print("\nПроекты пользователя:")
                for project in user.projects:
                    print(
                        f"- {project.title} (id={project.id}, задач: {len(project.tasks)})"
                    )

        elif command == "3":
            project = choose_project(user)
            if project is None:
                continue

            title = input("Название задачи: ").strip()
            description = input("Описание задачи: ").strip()
            priority = input(
                "Приоритет (Low, Medium, High, по умолчанию Medium): "
            ).strip()
            if not priority:
                priority = "Medium"

            due_input = input(
                "Срок выполнения (в формате YYYY-MM-DD HH:MM или пусто): "
            ).strip()
            due_date: Optional[datetime] = None
            if due_input:
                try:
                    due_date = datetime.strptime(due_input, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Некорректный формат даты, срок не будет установлен.")

            try:
                task = Task(
                    title=title,
                    description=description,
                    priority=priority,
                    due_date=due_date,
                )
            except ValueError as e:
                print(f"Ошибка при создании задачи: {e}")
                continue

            project.add_task(task)
            print(f"Задача создана: {task}")

        elif command == "4":
            project = choose_project(user)
            if project is None:
                continue

            if not project.tasks:
                print("В этом проекте пока нет задач.")
            else:
                print(f"\nЗадачи проекта {project.title}:")
                for task in project.tasks:
                    status = "[x]" if task.is_done else "[ ]"
                    due_str = (
                        task.due_date.strftime("%Y-%m-%d %H:%M")
                        if task.due_date
                        else "—"
                    )
                    print(
                        f"- {task.title} (id={task.id}, статус={status}, "
                        f"приоритет={task.priority}, срок={due_str})"
                    )

        elif command == "5":
            project = choose_project(user)
            if project is None:
                continue

            task = choose_task(project)
            if task is None:
                continue

            task.mark_as_done()
            print("Задача отмечена как выполненная.")

        elif command == "6":
            tasks = user.get_all_tasks()
            if not tasks:
                print("У пользователя нет задач.")
            else:
                print("\nВсе задачи пользователя:")
                for task in tasks:
                    status = "[x]" if task.is_done else "[ ]"
                    print(
                        f"- {task.title} (id={task.id}, статус={status}, проектов не хранится)"
                    )

        elif command == "7":
            overdue_tasks = user.get_overdue_tasks()
            if not overdue_tasks:
                print("Просроченных задач нет.")
            else:
                print("\nПросроченные задачи:")
                for task in overdue_tasks:
                    due_str = (
                        task.due_date.strftime("%Y-%m-%d %H:%M")
                        if task.due_date
                        else "—"
                    )
                    print(
                        f"- {task.title} (id={task.id}, приоритет={task.priority}, срок={due_str})"
                    )

        elif command == "8":
            priority = input("Введите приоритет (Low, Medium, High): ").strip()
            tasks = user.get_tasks_by_priority(priority)
            if not tasks:
                print("Задач с таким приоритетом нет.")
            else:
                print(f"\nЗадачи с приоритетом {priority}:")
                for task in tasks:
                    status = "[x]" if task.is_done else "[ ]"
                    print(f"- {task.title} (id={task.id}, статус={status})")

        elif command == "0":
            print("Выход из приложения. До свидания!")
            break

        else:
            print("Неизвестная команда, попробуйте снова.")


def demo_example() -> None:
    """Пример создания объектов и вызова их методов без CLI."""
    print("\n--- Демонстрационный пример ---")
    user = User(username="jdoe", full_name="John Doe", email="jdoe@example.com")
    project = user.create_project("Учёба", "Подготовка к экзаменам")
    task1 = Task("Прочитать главу 1", "Изучить основы", priority="High")
    task2 = Task("Сделать упражнения", "Закрепить материал", priority="Medium")

    project.add_task(task1)
    project.add_task(task2)

    print("Пользователь:", user)
    print("Проект:", project)
    print("Все задачи пользователя:", user.get_all_tasks())

    task1.mark_as_done()
    print("Задача 1 после выполнения:", task1)


if __name__ == "__main__":
    # Сначала запускаем демонстрационный пример,
    # затем — основное CLI-приложение.
    demo_example()
    cli_app()

