"""
Test module for big_integer
"""
from big_integer.big_integer import BigInteger


def test():
    """
    Main testing function.
    :return: None
    """
    integer_1 = BigInteger("123456")
    integer_2 = BigInteger("9547")
    integer_3 = BigInteger("9547")
    integer_4 = BigInteger("100")
    integer_5 = BigInteger("2")
    integer_6 = BigInteger("10")
    integer_7 = BigInteger("11110001001000000")
    integer_8 = BigInteger("-294363")

    print("integer_1", integer_1.to_string())
    print("integer_2", integer_2.to_string())
    print("integer_3", integer_3.to_string())
    print("integer_1 is less than integer_2", integer_1 < integer_2)
    print("integer_2 is less than integer_1", integer_2 < integer_1)
    print("integer_2 is less than integer_3", integer_2 < integer_3)
    print("integer_2 is less equals than integer_3", integer_2 <= integer_3)

    print("integer_2 equals integer_3", integer_2 == integer_3)
    print("integer_2 equals integer_1", integer_2 == integer_1)
    print("-" * 40)
    print("big integer 0 as bool", bool(BigInteger("0")))
    print("integer_2 as bool", bool(integer_2))
    print("-" * 40)

    print("integer_1 + integer_2", (integer_1 + integer_2).to_string())
    print("integer_1 - integer_2", (integer_1 - integer_2).to_string())
    print("integer_2 - integer_1", (integer_2 - integer_1).to_string())
    print(integer_1.multiply_by_digit(2).to_string())
    print(integer_1.multiply_by_digit(2).to_string())
    print("integer_1 * integer_3", (integer_1 * integer_3).to_string())
    print("-" * 40)
    print("integer_1 // integer_4", (integer_1 // integer_4).to_string())
    print("-294363 // 100 =", (integer_8 // integer_4).to_string())
    print("integer_1 % integer_4", (integer_1 % integer_4).to_string())
    print("integer_5 ** integer_6", (integer_5 ** integer_6).to_string())
    print("-" * 50)
    print("integer_6 to binary", integer_6.to_binary().to_string())
    print("11110001001000000 to decimal",
          integer_7.from_bin_to_dec().to_string())
    print("integer_6 to binary SHIFTED BY 2",
          (integer_6 << integer_5).to_string())
    print("integer_6 to binary SHIFTED BY 2",
          (integer_6 >> integer_5).to_string())
    print(10 << 2)
    print(10 >> 2)
    print(9547 & 100)
    print("9547 & 100 = ", (integer_2 & integer_4).to_string())
    print(9547 | 100)
    print("9547 | 100 = ", (integer_2 | integer_4).to_string())
    print(9547 ^ 100)
    print("9547 ^ 100 = ", (integer_2 ^ integer_4).to_string())


if __name__ == '__main__':
    test()
