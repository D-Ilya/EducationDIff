class ColorPrint:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"

    @classmethod
    def print_err(cls, msg: str):
        print(cls.RED + msg + cls.END)

    @classmethod
    def print_ok(cls, msg):
        print(cls.GREEN + msg + cls.END)

    @classmethod
    def print_warn(cls, msg):
        print(cls.YELLOW + msg + cls.END)

    @classmethod
    def print_info(cls, msg):
        print(cls.BLUE + msg + cls.END)