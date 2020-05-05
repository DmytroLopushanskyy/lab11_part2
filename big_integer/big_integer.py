"""
BigInteger class realisation.
"""
from big_integer.node import TwoWayNode


class BigInteger:
    """
    Class for representing big integers.
    """
    def __init__(self, init_value="0"):
        """
        BigInteger initialisation.
        :param init_value: str
        """
        self.is_positive = True
        init_value = self.validate_str(init_value)
        self.length = len(init_value)

        first_node = TwoWayNode(int(init_value[0]))
        self._head = first_node
        self._tail = first_node
        for char in init_value[1:]:
            new_node = TwoWayNode(int(char), None, self._head)
            self._head.previous = new_node
            self._head = new_node

    def validate_str(self, val):
        """
        Validate string to only contain digits or - sign.
        :return: str
        """
        if val.startswith("-"):
            self.is_positive = False
        while val.startswith("0"):
            val = val[1:]
        validated = [ch for ch in val if ch.isdigit()]
        if not validated:
            validated = "0"
        return validated

    def __add__(self, other):
        """
        Add two big integers.
        :param other: BigInteger
        :return: BigInteger
        """
        if self.is_positive != other.is_positive:
            if self.is_positive:
                return self - abs(other)
            return other - abs(self)

        new_integer = ""
        if self.length >= other.length:
            smaller_integer = other
            bigger_integer = self
        else:
            smaller_integer = self
            bigger_integer = other

        next_el_1 = smaller_integer._head
        next_el_2 = bigger_integer._head
        add_one = False
        while next_el_2 is not None:
            if next_el_1 is None:
                next_el_1 = TwoWayNode(0)
            res = next_el_1.data + next_el_2.data + add_one
            if res > 9:
                add_one = True
                new_integer = str(res % 10) + new_integer
            else:
                add_one = False
                new_integer = str(res) + new_integer
            next_el_1 = next_el_1.next_el
            next_el_2 = next_el_2.next_el

        if add_one:
            new_integer = "1" + new_integer

        final_integer = BigInteger(new_integer)
        final_integer.is_positive = self.is_positive
        return final_integer

    def __sub__(self, other):
        """
        Subtract two big integers.
        :param other: BigInteger
        :return: BigInteger
        """
        if self.is_positive and not other.is_positive:  # (+self) - (-other)
            return self + abs(other)
        if not self.is_positive and not other.is_positive:  # (-self) - (-other)
            return abs(other) - abs(self)
        if not self.is_positive and other.is_positive:  # (-self) - (+other)
            result = abs(self) + other
            result.is_positive = False
            return result
        # else for (+self) - (+other)
        if self < other:
            result = other - self
            result.is_positive = False
            return result
        # now we have to subtract two positive integers. First one is bigger.

        new_integer = ""
        next_el_1 = other._head
        next_el_2 = self._head
        sub_one = False
        while next_el_2 is not None:
            if next_el_1 is None:
                next_el_1 = TwoWayNode(0)
            res = next_el_2.data - next_el_1.data - sub_one
            if res < 0:
                sub_one = True
                new_integer = str(res % 10) + new_integer
            else:
                sub_one = False
                new_integer = str(res) + new_integer
            next_el_1 = next_el_1.next_el
            next_el_2 = next_el_2.next_el

        return BigInteger(new_integer)

    def __mul__(self, other):
        """
        Multiply two big integers.
        :param other: BigInteger
        :return: BigInteger
        """
        nums_to_add = []
        next_el = other._head
        i = 0
        while next_el is not None:
            partial_mul = self.multiply_by_digit(int(next_el.data)).to_string()
            partial_mul += "0" * i
            nums_to_add.append(BigInteger(partial_mul))
            next_el = next_el.next_el
            i += 1

        result = BigInteger("0")
        for partial in nums_to_add:
            result = result + partial

        if self.is_positive != other.is_positive:
            result.is_positive = False

        return result

    def __floordiv__(self, other):
        """
        Divide by other and get the result without remainder.
        :param other: BigInteger
        :return: BigInteger
        """
        if other == BigInteger("0"):
            raise ZeroDivisionError
        result = BigInteger("-1")
        diff = abs(self)
        while diff.is_positive:
            result = result + BigInteger("1")
            diff = diff - other

        if not self.is_positive:
            result = result + BigInteger("1")
            result.is_positive = False
            return result
        return result

    def multiply_by_digit(self, digit):
        """
        Multiply by digit.
        :param digit: int
        :return: BigInteger
        """
        result = ""
        next_el = self._head
        digit_to_add = 0
        while next_el is not None:
            num, remainder = divmod(digit * next_el.data, 10)
            result = str((remainder + digit_to_add) % 10) + result
            digit_to_add = num + (remainder + digit_to_add) // 10
            next_el = next_el.next_el
        if digit_to_add:
            result = str(digit_to_add) + result
        return BigInteger(result)

    def __mod__(self, other):
        """
        Get remainder of dividing self by other.
        :param other: BigInteger
        :return: BigInteger
        """
        return self - (other * (self // other))

    def __pow__(self, power, modulo=None):
        """
        Raise to self to power.
        :param power: BigInteger
        :return: BigInteger
        """
        if power == BigInteger("0"):
            return BigInteger("1")
        i = BigInteger("1")
        result = self
        while i != power:
            result = result * self
            i = i + BigInteger("1")

        if not self.is_positive and power % 2 != 0:
            result.is_positive = False

        return result

    # comparison operators
    def __le__(self, other):
        """
        Less equal than operator.
        :param other: BigInteger
        :return: bool
        """
        if self.is_positive != other.is_positive:
            return not bool(self.is_positive)
        if self.length < other.length:
            return bool(self.is_positive)
        if self.length > other.length:
            return not bool(self.is_positive)

        next_el_1 = self._tail
        next_el_2 = other._tail
        while next_el_1 is not None:
            if next_el_1.data < next_el_2.data:
                return bool(self.is_positive)
            if next_el_1.data > next_el_2.data:
                return not bool(self.is_positive)
            next_el_1 = next_el_1.previous
            next_el_2 = next_el_2.previous
        return True  # are equal

    def __lt__(self, other):
        """
        Less than operator.
        :param other: BigInteger
        :return: bool
        """
        if self.is_positive != other.is_positive:
            return not bool(self.is_positive)
        if self.length < other.length:
            return bool(self.is_positive)
        if self.length > other.length:
            return not bool(self.is_positive)

        next_el_1 = self._tail
        next_el_2 = other._tail
        while next_el_1 is not None:
            if next_el_1.data < next_el_2.data:
                return bool(self.is_positive)
            if next_el_1.data > next_el_2.data:
                return not bool(self.is_positive)
            next_el_1 = next_el_1.previous
            next_el_2 = next_el_2.previous
        return False

    def __eq__(self, other):
        """
        Check if self equals other.
        :param other: BigInteger
        :return: bool
        """
        if self.length != other.length:
            return False
        if self.is_positive != other.is_positive:
            return False

        next_el_1 = self._tail
        next_el_2 = other._tail
        while next_el_1 is not None:
            if next_el_1.data != next_el_2.data:
                return False
            next_el_1 = next_el_1.previous
            next_el_2 = next_el_2.previous
        return True

    def __ge__(self, other):
        """
        Bigger equal than operator.
        :param other: BigInteger
        :return: bool
        """
        return not self < other

    def __gt__(self, other):
        """
        Bigger than operator.
        :param other: BigInteger
        :return: bool
        """
        return not self <= other

    def __ne__(self, other):
        """
        Not equals operator.
        :param other: BigInteger
        :return: bool
        """
        return not self == other

    def __bool__(self):
        """
        Bool representation.
        :return: bool
        """
        if self != BigInteger("0"):
            return True
        return False

    def __abs__(self):
        """
        Get absolute value
        :return: BigInteger
        """
        new_integer = BigInteger(self.to_string())
        new_integer.is_positive = True
        return new_integer

    # bitwise operators
    def to_binary(self):
        """
        Convert BigInteger to binary.
        :return: BigDigit
        """
        result = ""
        remainder = self
        while remainder != BigInteger("1"):
            result = (remainder % BigInteger("2")).to_string() + result
            remainder = remainder // BigInteger("2")
        result = (remainder % BigInteger("2")).to_string() + result
        return BigInteger(result)

    def from_bin_to_dec(self):
        """
        Convert from binary to decimal.
        :return: BigDigit.
        """
        next_el = self._head
        result = BigInteger("0")
        i = BigInteger("0")
        while next_el is not None:
            result = result + BigInteger(str(next_el)) * BigInteger("2") ** i
            i = i + BigInteger("1")
            next_el = next_el.next_el
        return result

    def __lshift__(self, other):
        """
        Shift to left
        :param other: BigInteger
        :return: BigInteger
        """
        shifted = self.to_binary().to_string()
        i = other
        while i != BigInteger("0"):
            i = i - BigInteger("1")
            shifted += "0"
        return BigInteger(shifted).from_bin_to_dec()

    def __rshift__(self, other):
        """
        Shift to right
        :param other: BigInteger
        :return: BigInteger
        """
        shifted = self.to_binary().to_string()
        i = other
        while i != BigInteger("0"):
            i = i - BigInteger("1")
            shifted = shifted[:-1]
        return BigInteger(shifted).from_bin_to_dec()

    def __and__(self, other):
        """
        Bitwise and.
        :param other: BigInteger
        :return: BigInteger
        """
        return self.bitwise_helper(other, "add")

    def __xor__(self, other):
        """
        Bitwise xor.
        :param other: BigInteger
        :return: BigInteger
        """
        return self.bitwise_helper(other, "xor")

    def __or__(self, other):
        """
        Bitwise or.
        :param other: BigInteger
        :return: BigInteger
        """
        return self.bitwise_helper(other, "or")

    def bitwise_helper(self, other, action):
        """
        Bitwise operations helper.
        :param other: BigInteger
        :param action: str
        :return: BigInteger
        """
        self_bin = self.to_binary()
        other_bin = other.to_binary()

        if self_bin.length >= other_bin.length:
            bigger = self_bin
            smaller = other_bin
        else:
            bigger = other_bin
            smaller = self_bin

        next_el_1 = bigger._head
        next_el_2 = smaller._head
        result = ""
        while next_el_1 is not None:
            if next_el_2 is None:
                next_el_2 = TwoWayNode(0)

            if action == "add":
                calc = next_el_1.data & next_el_2.data
            elif action == "xor":
                calc = next_el_1.data ^ next_el_2.data
            else:  # or
                calc = next_el_1.data | next_el_2.data
            result = str(calc) + result
            next_el_1 = next_el_1.next_el
            next_el_2 = next_el_2.next_el

        return BigInteger(result).from_bin_to_dec()

    def to_string(self):
        """
        Returns BigInteger as string.
        :return: str
        """
        output = ""
        next_el = self._head
        while next_el is not None:
            output = str(next_el) + output
            next_el = next_el.next_el

        if not self.is_positive:
            return "-" + output
        return output

    def __str__(self):
        """
        String representation.
        :return: str
        """
        return self.to_string()
