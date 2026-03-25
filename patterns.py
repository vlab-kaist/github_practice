from abc import ABC, abstractmethod


# === Singleton ===
class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class DatabaseConnection(Singleton):
    def __init__(self, host="localhost", port=5432):
        if not hasattr(self, "_initialized"):
            self.host = host
            self.port = port
            self._initialized = True
            print(f"DB 연결: {host}:{port}")

    def query(self, sql):
        return f"[{self.host}] 실행: {sql}"


# === Observer ===
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event, callback):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event, *args, **kwargs):
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)


# === Strategy ===
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass


class BubbleSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data[:]
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class Sorter:
    def __init__(self, strategy=None):
        self._strategy = strategy or QuickSortStrategy()

    def set_strategy(self, strategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)


# === Factory ===
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

    @abstractmethod
    def name(self):
        pass


class Dog(Animal):
    def speak(self):
        return "멍멍!"

    def name(self):
        return "개"


class Cat(Animal):
    def speak(self):
        return "야옹~"

    def name(self):
        return "고양이"


class Duck(Animal):
    def speak(self):
        return "꽥꽥!"

    def name(self):
        return "오리"


class AnimalFactory:
    _animals = {
        "dog": Dog,
        "cat": Cat,
        "duck": Duck,
    }

    @classmethod
    def create(cls, animal_type):
        animal_class = cls._animals.get(animal_type.lower())
        if not animal_class:
            raise ValueError(f"알 수 없는 동물: {animal_type}")
        return animal_class()

    @classmethod
    def register(cls, name, animal_class):
        cls._animals[name.lower()] = animal_class


# === Builder ===
class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.toppings = []
        self.sauce = None
        self.cheese = None

    def __repr__(self):
        return (
            f"Pizza(size={self.size}, crust={self.crust}, "
            f"sauce={self.sauce}, cheese={self.cheese}, "
            f"toppings={self.toppings})"
        )


class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def size(self, size):
        self._pizza.size = size
        return self

    def crust(self, crust):
        self._pizza.crust = crust
        return self

    def sauce(self, sauce):
        self._pizza.sauce = sauce
        return self

    def cheese(self, cheese):
        self._pizza.cheese = cheese
        return self

    def topping(self, topping):
        self._pizza.toppings.append(topping)
        return self

    def build(self):
        pizza = self._pizza
        self._pizza = Pizza()
        return pizza


# === Decorator Pattern ===
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass


class BasicCoffee(Coffee):
    def cost(self):
        return 3000

    def description(self):
        return "아메리카노"


class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee


class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 500

    def description(self):
        return self._coffee.description() + " + 우유"


class SyrupDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 300

    def description(self):
        return self._coffee.description() + " + 시럽"


class WhipDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 700

    def description(self):
        return self._coffee.description() + " + 휘핑"


# === State Machine ===
class State(ABC):
    @abstractmethod
    def handle(self, context):
        pass


class IdleState(State):
    def handle(self, context):
        print("대기 중... 시작합니다.")
        context.state = RunningState()


class RunningState(State):
    def handle(self, context):
        print("실행 중... 완료!")
        context.state = CompletedState()


class CompletedState(State):
    def handle(self, context):
        print("완료됨. 리셋합니다.")
        context.state = IdleState()


class StateMachine:
    def __init__(self):
        self.state = IdleState()

    def step(self):
        self.state.handle(self)

    def current_state(self):
        return self.state.__class__.__name__


if __name__ == "__main__":
    print("=== Singleton ===")
    db1 = DatabaseConnection("prod-server", 5432)
    db2 = DatabaseConnection("other-server", 3306)
    print(f"  같은 인스턴스? {db1 is db2}")
    print(f"  {db1.query('SELECT * FROM users')}")

    print("\n=== Observer ===")
    emitter = EventEmitter()
    emitter.on("login", lambda user: print(f"  {user} 로그인!"))
    emitter.on("login", lambda user: print(f"  {user} 환영합니다!"))
    emitter.on("logout", lambda user: print(f"  {user} 로그아웃"))
    emitter.emit("login", "철수")
    emitter.emit("logout", "철수")

    print("\n=== Strategy ===")
    sorter = Sorter()
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"  Quick: {sorter.sort(data)}")
    sorter.set_strategy(BubbleSortStrategy())
    print(f"  Bubble: {sorter.sort(data)}")

    print("\n=== Factory ===")
    for animal_type in ["dog", "cat", "duck"]:
        animal = AnimalFactory.create(animal_type)
        print(f"  {animal.name()}: {animal.speak()}")

    print("\n=== Builder ===")
    pizza = (
        PizzaBuilder()
        .size("L")
        .crust("씬")
        .sauce("토마토")
        .cheese("모짜렐라")
        .topping("페퍼로니")
        .topping("올리브")
        .topping("버섯")
        .build()
    )
    print(f"  {pizza}")

    print("\n=== Decorator ===")
    coffee = BasicCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SyrupDecorator(coffee)
    coffee = WhipDecorator(coffee)
    print(f"  {coffee.description()}: {coffee.cost():,}원")

    print("\n=== State Machine ===")
    sm = StateMachine()
    for _ in range(6):
        print(f"  상태: {sm.current_state()}", end=" -> ")
        sm.step()
