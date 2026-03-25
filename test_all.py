"""모든 모듈 테스트"""

import unittest
from calculator import Calculator
from data_structures import Stack, Queue, LinkedList, BinarySearchTree, HashMap
from sorting import (
    bubble_sort, selection_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort,
    counting_sort, radix_sort,
)
from utils import (
    validate_email, validate_phone, validate_password_strength,
    slugify, truncate, flatten, chunk_list, deep_merge,
    format_bytes, format_number, hash_string, generate_password,
)
from matrix import Matrix
from game import NumberGuessingGame, RockPaperScissors, DiceGame
from patterns import (
    DatabaseConnection, EventEmitter, Sorter,
    AnimalFactory, PizzaBuilder, BasicCoffee,
    MilkDecorator, SyrupDecorator, StateMachine,
)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)
        self.assertEqual(self.calc.subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)
        self.assertEqual(self.calc.multiply(-3, 7), -21)
        self.assertEqual(self.calc.multiply(0, 100), 0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333, places=3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 10), 1024)
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_modulo(self):
        self.assertEqual(self.calc.modulo(17, 5), 2)
        with self.assertRaises(ZeroDivisionError):
            self.calc.modulo(10, 0)

    def test_history(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        self.assertEqual(len(self.calc.get_history()), 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.size(), 1)

    def test_peek(self):
        s = Stack()
        s.push(42)
        self.assertEqual(s.peek(), 42)
        self.assertEqual(s.size(), 1)

    def test_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_pop_empty(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        q.enqueue("c")
        self.assertEqual(q.dequeue(), "a")
        self.assertEqual(q.dequeue(), "b")
        self.assertEqual(q.size(), 1)

    def test_front(self):
        q = Queue()
        q.enqueue(10)
        self.assertEqual(q.front(), 10)

    def test_dequeue_empty(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()


class TestLinkedList(unittest.TestCase):
    def test_append(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        self.assertEqual(ll.to_list(), [1, 2, 3])

    def test_prepend(self):
        ll = LinkedList()
        ll.append(2)
        ll.prepend(1)
        self.assertEqual(ll.to_list(), [1, 2])

    def test_delete(self):
        ll = LinkedList()
        for x in [1, 2, 3, 4]:
            ll.append(x)
        ll.delete(3)
        self.assertEqual(ll.to_list(), [1, 2, 4])
        self.assertEqual(ll.size(), 3)

    def test_find(self):
        ll = LinkedList()
        for x in [10, 20, 30]:
            ll.append(x)
        self.assertEqual(ll.find(20), 1)
        self.assertEqual(ll.find(99), -1)


class TestBST(unittest.TestCase):
    def test_insert_search(self):
        bst = BinarySearchTree()
        for x in [50, 30, 70, 20, 40]:
            bst.insert(x)
        self.assertTrue(bst.search(30))
        self.assertTrue(bst.search(70))
        self.assertFalse(bst.search(99))

    def test_inorder(self):
        bst = BinarySearchTree()
        for x in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(x)
        self.assertEqual(bst.inorder(), [20, 30, 40, 50, 60, 70, 80])

    def test_height(self):
        bst = BinarySearchTree()
        bst.insert(50)
        self.assertEqual(bst.height(), 1)
        bst.insert(30)
        bst.insert(70)
        self.assertEqual(bst.height(), 2)


class TestHashMap(unittest.TestCase):
    def test_put_get(self):
        hm = HashMap()
        hm.put("a", 1)
        hm.put("b", 2)
        self.assertEqual(hm.get("a"), 1)
        self.assertEqual(hm.get("b"), 2)
        self.assertIsNone(hm.get("c"))

    def test_overwrite(self):
        hm = HashMap()
        hm.put("key", "old")
        hm.put("key", "new")
        self.assertEqual(hm.get("key"), "new")

    def test_remove(self):
        hm = HashMap()
        hm.put("x", 10)
        self.assertTrue(hm.remove("x"))
        self.assertIsNone(hm.get("x"))
        self.assertFalse(hm.remove("x"))


class TestSorting(unittest.TestCase):
    def setUp(self):
        self.unsorted = [64, 34, 25, 12, 22, 11, 90]
        self.expected = sorted(self.unsorted)

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(self.unsorted), self.expected)

    def test_selection_sort(self):
        self.assertEqual(selection_sort(self.unsorted), self.expected)

    def test_insertion_sort(self):
        self.assertEqual(insertion_sort(self.unsorted), self.expected)

    def test_merge_sort(self):
        self.assertEqual(merge_sort(self.unsorted), self.expected)

    def test_quick_sort(self):
        self.assertEqual(quick_sort(self.unsorted), self.expected)

    def test_heap_sort(self):
        self.assertEqual(heap_sort(self.unsorted), self.expected)

    def test_counting_sort(self):
        self.assertEqual(counting_sort(self.unsorted), self.expected)

    def test_radix_sort(self):
        self.assertEqual(radix_sort(self.unsorted), self.expected)

    def test_empty(self):
        for func in [bubble_sort, merge_sort, quick_sort]:
            self.assertEqual(func([]), [])

    def test_single(self):
        for func in [bubble_sort, merge_sort, quick_sort]:
            self.assertEqual(func([42]), [42])


class TestUtils(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name+tag@domain.co.kr"))
        self.assertFalse(validate_email("not-email"))
        self.assertFalse(validate_email("@domain.com"))

    def test_validate_phone(self):
        self.assertTrue(validate_phone("010-1234-5678"))
        self.assertTrue(validate_phone("02-123-4567"))
        self.assertFalse(validate_phone("1234567890"))

    def test_password_strength(self):
        weak = validate_password_strength("abc")
        self.assertEqual(weak["strength"], "약함")
        strong = validate_password_strength("MyP@ssw0rd!")
        self.assertIn(strong["strength"], ["강함", "매우 강함"])

    def test_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")

    def test_truncate(self):
        self.assertEqual(truncate("short", 100), "short")
        self.assertEqual(truncate("a very long string", 10), "a very...")

    def test_flatten(self):
        self.assertEqual(flatten([1, [2, [3, [4]]]]), [1, 2, 3, 4])
        self.assertEqual(flatten([]), [])

    def test_chunk_list(self):
        self.assertEqual(chunk_list([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_deep_merge(self):
        d1 = {"a": 1, "b": {"x": 10}}
        d2 = {"b": {"y": 20}, "c": 3}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], {"x": 10, "y": 20})
        self.assertEqual(result["c"], 3)

    def test_format_bytes(self):
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertIn("MB", format_bytes(1048576))

    def test_format_number(self):
        self.assertEqual(format_number(1500), "1.5K")
        self.assertEqual(format_number(2500000), "2.5M")

    def test_hash_string(self):
        h1 = hash_string("hello", "sha256")
        h2 = hash_string("hello", "sha256")
        self.assertEqual(h1, h2)
        self.assertNotEqual(hash_string("hello"), hash_string("world"))

    def test_generate_password(self):
        pw = generate_password(20)
        self.assertEqual(len(pw), 20)
        self.assertTrue(any(c.isupper() for c in pw))
        self.assertTrue(any(c.islower() for c in pw))
        self.assertTrue(any(c.isdigit() for c in pw))


class TestMatrix(unittest.TestCase):
    def test_add(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        result = a + b
        self.assertEqual(result.data, [[6, 8], [10, 12]])

    def test_subtract(self):
        a = Matrix([[5, 6], [7, 8]])
        b = Matrix([[1, 2], [3, 4]])
        result = a - b
        self.assertEqual(result.data, [[4, 4], [4, 4]])

    def test_multiply_scalar(self):
        a = Matrix([[1, 2], [3, 4]])
        result = a * 2
        self.assertEqual(result.data, [[2, 4], [6, 8]])

    def test_multiply_matrix(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        result = a * b
        self.assertEqual(result.data, [[19, 22], [43, 50]])

    def test_transpose(self):
        a = Matrix([[1, 2, 3], [4, 5, 6]])
        t = a.transpose()
        self.assertEqual(t.rows, 3)
        self.assertEqual(t.cols, 2)
        self.assertEqual(t.data, [[1, 4], [2, 5], [3, 6]])

    def test_determinant(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.determinant(), -2)

    def test_identity(self):
        i = Matrix.identity(3)
        self.assertEqual(i.data, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_trace(self):
        m = Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 9]])
        self.assertEqual(m.trace(), 15)


class TestGames(unittest.TestCase):
    def test_number_guessing(self):
        game = NumberGuessingGame(1, 100)
        result = game.guess(game.secret)
        self.assertEqual(result, "correct")

    def test_rps(self):
        rps = RockPaperScissors()
        result = rps.play("가위")
        self.assertIn(result["result"], ["win", "lose", "draw"])
        self.assertEqual(result["player"], "가위")

    def test_dice(self):
        dice = DiceGame(2)
        roll = dice.roll()
        self.assertEqual(len(roll), 2)
        self.assertTrue(all(1 <= d <= 6 for d in roll))


class TestPatterns(unittest.TestCase):
    def test_singleton(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        self.assertIs(db1, db2)

    def test_observer(self):
        results = []
        emitter = EventEmitter()
        emitter.on("test", lambda x: results.append(x))
        emitter.emit("test", 42)
        self.assertEqual(results, [42])

    def test_factory(self):
        dog = AnimalFactory.create("dog")
        self.assertEqual(dog.speak(), "멍멍!")
        cat = AnimalFactory.create("cat")
        self.assertEqual(cat.speak(), "야옹~")

    def test_builder(self):
        pizza = PizzaBuilder().size("L").crust("씬").topping("치즈").build()
        self.assertEqual(pizza.size, "L")
        self.assertEqual(pizza.crust, "씬")
        self.assertIn("치즈", pizza.toppings)

    def test_decorator(self):
        coffee = BasicCoffee()
        self.assertEqual(coffee.cost(), 3000)
        coffee = MilkDecorator(coffee)
        self.assertEqual(coffee.cost(), 3500)
        coffee = SyrupDecorator(coffee)
        self.assertEqual(coffee.cost(), 3800)

    def test_state_machine(self):
        sm = StateMachine()
        self.assertEqual(sm.current_state(), "IdleState")
        sm.step()
        self.assertEqual(sm.current_state(), "RunningState")
        sm.step()
        self.assertEqual(sm.current_state(), "CompletedState")


if __name__ == "__main__":
    unittest.main(verbosity=2)
