

from typing import Union
from pydantic import BaseModel, Field
import inspect


class DB_value_model(BaseModel):
    ref_count: int = 1
    value: Union[str, int, float]
    transtaction_operation: str = Field(default="")


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
        self.transaction_stack = []
        self.current_transaction = None

    @MethodRegistry.register(tip="начинает новую транзакцию")
    def BEGIN(self):
        if self.current_transaction:
            self.transaction_stack.append(self.current_transaction)

        self.current_transaction = {"keys": {}, "values": {}}
        return "Транзакция начата"

    @MethodRegistry.register(tip="фиксирует текущую транзакцию")
    def COMMIT(self):
        if not self.current_transaction:
            return "Нечего фиксировать. Начните новую транзакцию."

        if not self.current_transaction['keys']:
            return "Нельзя фиксировать пустую транзакцию."

        # Применяем изменения из текущей транзакции
        for key, value_hashcode in self.current_transaction["keys"].items():
            self.keys[key] = value_hashcode
        for hashref, db_value in self.current_transaction["values"].items():
            if hashref in self.values:
                self.values[hashref].ref_count += db_value.ref_count
            else:
                self.values[hashref] = db_value

        # Очищаем текущую транзакцию
        self.transaction_stack.pop()
        self.current_transaction = None if not self.transaction_stack else self.transaction_stack[-1]
        return "Transaction committed."

    @MethodRegistry.register(tip="откатывает текущую транзакцию")
    def ROLLBACK(self):
        if not self.current_transaction:
            return "Нет активных транзакций для отмены."

        msg = 'Транзакция отменена.'
        self.current_transaction = None
        if self.transaction_stack:
            self.current_transaction = self.transaction_stack.pop()
            return f"{msg} Возврат к предыдущей транзакции."

        return msg

    @MethodRegistry.register(tip="сохраняет аргумент в базе данных")
    def SET(self, key, value):

        is_delayed = self.current_transaction is not None

        keys: dict = self.current_transaction['keys'] if is_delayed else self.keys
        values: dict = self.current_transaction['values'] if is_delayed else self.values

        value_hashcode = hash(value)
        if old_value_ref := keys.get(key):
            if value_hashcode != old_value_ref:
                self._recalc_values_db(old_value_ref)

                keys[key] = value_hashcode
                values[value_hashcode] = DB_value_model(**{'value': value})
        else:
            keys[key] = value_hashcode
            if value_hashcode in values:
                values[value_hashcode].ref_count += 1
            else:
                model_data = {'value': value}
                if is_delayed:
                    model_data["transtaction_operation"] = "SET"
                values[value_hashcode] = DB_value_model(**model_data)

        return 'OK 👌'

    @MethodRegistry.register(tip="возвращает, ранее сохраненную переменную. Если такой переменной не было сохранено, возвращает NULL")
    def GET(self, key):
        if (ct := self.current_transaction) and (v := ct['keys'].get(key)):
            return v.value
        if hashref := self.keys.get(key):
            v: DB_value_model = self.values[hashref]
            return v.value
        return 'NULL'

    @MethodRegistry.register(tip="удаляет, ранее установленную переменную. Если значение не было установлено, не делает ничего")
    def UNSET(self, key):
        is_delayed = self.current_transaction is not None

        keys: dict = self.current_transaction['keys'] if is_delayed else self.keys

        if hashref := keys.get(key):
            del keys[key]
            self._recalc_values_db(hashref)
            return 'Удалено из транзакции' if is_delayed else 'Удалено из базы'

        if is_delayed and (hashref := self.keys.get(key)):
            self.current_transaction['values'][hashref] = self.values[hashref]
            self.current_transaction['values']['transtaction_operation'] = "UNSET"

        return 'Не найдено'

    @MethodRegistry.register(tip="показывает сколько раз данные значение встречается в базе данных")
    def COUNTS(self, value):
        value_hashcode = hash(value)
        if v := self.values.get(value_hashcode):
            v: DB_value_model
            ref_count = v.ref_count
            if self.current_transaction:
                transaction_values = self.current_transaction['keys'].values()
                for tv in transaction_values:
                    if tv == value_hashcode:
                        ref_count += 1
                if (ct := self.current_transaction) and (v := ct['values'].get(value_hashcode)):
                    ref_count -= v.ref_count
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
        values: dict = self.current_transaction.get(
            'values') if self.current_transaction else self.values

        v: DB_value_model = values[hashref]
        v.ref_count -= 1
        if v.ref_count == 0 and not self.current_transaction:
            del values[hashref]

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
            'HELP', 'INCORRECT METHOD 2 14', 'GeT A', 'SET A 10',
            'GET a', 'GET A', 'Counts 10', 'SET B 20', 'SET C 10', 'CoUNTs 10',
            'Find 10', 'Unset A', 'Find 10', 'BEGIN', 'COMMIT', 'ROLLBACK', 'ROLLBACK', 'COMMIT', 'BEGIN'
            'BEGIN', 'SET A 44', 'COMMIT', 'GET A', 'BEGIN', 'SET A 22', 'ROLLBACK', 'GET A',
            'CoUNTs 10', 'FIND 10', 'CoUNTs 44', 'FIND 44', 'End'
        ]

        for test_command in test_commands[1:]:
            main(db, test_command)
        ...
    else:
        main(db)
