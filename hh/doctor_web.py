

from typing import Union
from pydantic import BaseModel, Field
import inspect


class DB_value_model(BaseModel):
    ref_count: int = 1
    value: Union[str, int, float]


class MethodRegistry:
    _registry = {}

    @staticmethod
    def register(tip):
        """Статический метод-декоратор для регистрации методов"""
        def decorator(func):
            MethodRegistry._registry[func.__name__] = {
                "func": func, "tip": tip}
            return func
        return decorator

    @property
    def registry(self):
        """Метод для получения содержимого словаря"""
        return MethodRegistry._registry


class DB(MethodRegistry):

    def __init__(self):
        super().__init__()
        self.keys = dict()
        self.values = dict()

    @MethodRegistry.register(tip="сохраняет аргумент в базе данных")
    def SET(self, key, value):

        value_hashcode = hash(value)
        if old_value_ref := self.keys.get(key):
            if value_hashcode != old_value_ref:
                self._recalc_values_db(old_value_ref)

                self.keys[key] = value_hashcode
                self.values[value_hashcode] = DB_value_model(
                    **{'value': value})
        else:
            self.keys[key] = value_hashcode
            if value_hashcode in self.values:
                self.values[value_hashcode].ref_count += 1
            else:
                self.values[value_hashcode] = DB_value_model(
                    **{'value': value})

        return 'OK'

    @MethodRegistry.register(tip="возвращает, ранее сохраненную переменную. Если такой переменной не было сохранено, возвращает NULL")
    def GET(self, key):
        if hashref := self.keys.get(key):
            v: DB_value_model = self.values[hashref]
            return v.value
        return 'NULL'

    @MethodRegistry.register(tip="удаляет, ранее установленную переменную. Если значение не было установлено, не делает ничего")
    def UNSET(self, key):
        if hashref := self.keys.get(key):
            del self.keys[key]
            self._recalc_values_db(hashref)

            return 'deleted'
        return 'not found'

    @MethodRegistry.register(tip="показывает сколько раз данные значение встречается в базе данных")
    def COUNTS(self, value):
        value_hashcode = hash(value)
        if v := self.values.get(value_hashcode):
            v: DB_value_model
            return v.ref_count
        return 0

    @MethodRegistry.register(tip="выводит найденные установленные переменные для данного значения")
    def FIND(self, value: str):
        value_hashcode = hash(value)
        if not (count_vars := self.values.get(value_hashcode)):
            return f"{value} отсутствует в базе данных"

        count_vars: DB_value_model = count_vars.ref_count

        variables = list()
        for k, v in self.keys.items():
            if v == value_hashcode:
                variables.append(k)
                count_vars -= 1

                if count_vars == 0:
                    break

        return variables

    @MethodRegistry.register(tip="закрывает приложение")
    def END(self):
        raise EOFError

    @MethodRegistry.register(tip="Вывод доступных комманд")
    def HELP(self):
        print('Список доступных команд:')
        for k, v in self.registry.items():
            print(f"{k}\t- {v['tip']}")

        return "\n"

    def _recalc_values_db(self, hashref: str):
        v: DB_value_model = self.values[hashref]
        v.ref_count -= 1
        if v.ref_count == 0:
            del self.values[hashref]

        return 1

    def get_command_info(self, command: str):
        return self.registry.get(command, None)


def main(db: DB, debug_str: str = None):
    while True:
        try:
            user_input = debug_str if debug_str else input("> ").strip()
            processing_command(db, user_input)
            if debug_str:
                break
        except EOFError:
            print('bye.')
            break
        except ValueError:
            msg = 'Неверный формат команды. Введите help, чтобы узнать доступные комапды.'
            print(msg)
            if debug_str:
                break

    return 1


def processing_command(db: DB, user_input: str):
    args = user_input.split()
    command = str(args[0]).upper()
    if not (command_info := db.get_command_info(command)):
        raise ValueError(f"Неизвестная команда: {command}")

    func = command_info['func']
    requied_args = inspect.getfullargspec(func).args[1:]

    len_args = len(args[1:])
    len_requied_args = len(requied_args)

    if len(args[1:]) != len(requied_args):
        print(
            f"Неверное количество аргументов. Ожидалось {len_requied_args}, получено {len_args}")
        return

    dict_args = {'self': db}
    for i in range(len_requied_args):
        dict_args[requied_args[i]] = args[i+1]

    res = func(**dict_args)
    print(f'{user_input}: {res}')

    return 1


if __name__ == '__main__':
    db = DB()

    is_debug = True
    if is_debug:
        test_commands = [
            'HELP', 'INCORRECT METHOD 2 14', 'GET A', 'SET A 10',
            'GET a', 'GET A', 'Counts 10', 'SET B 20', 'SET C 10', 'Counts 10',
            'Find 10', 'Unset A', 'Find 10', 'End'
        ]

        for test_command in test_commands[1:]:
            main(db, test_command)
        ...
    else:
        main(db)
