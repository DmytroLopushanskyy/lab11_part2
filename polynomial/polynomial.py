"""
Implementation of the Polynomial ADT using a sorted linked list.
"""


class Polynomial:
    """
    Create a new polynomial object.
    """
    def __init__(self, degree=None, coefficient=None):
        """
        Polynomial initialisation.
        :param degree: float
        :param coefficient: float
        """
        if degree is None:
            self._poly_head = None
        else:
            self._poly_head = _PolyTermNode(degree, coefficient)
        self._poly_tail = self._poly_head

    def degree(self):
        """
        Return the degree of the polynomial.
        :return:
        """
        if self._poly_head is None:
            return -1
        return self._poly_head.degree

    def __getitem__(self, degree):
        """
        Return the coefficient for the term of the given degree.
        :param degree: float
        :return: float
        """
        assert self.degree() >= 0, "Operation not permitted on an empty polynomial."
        cur_node = self._poly_head
        while cur_node is not None and cur_node.degree >= degree:
            if cur_node.degree == degree:
                break
            cur_node = cur_node.next

        if cur_node is None or cur_node.degree != degree:
            return 0.0

        return cur_node.coefficient

    def evaluate(self, scalar):
        """
        Evaluate the polynomial at the given scalar value.
        :param scalar:
        :return:
        """
        assert self.degree() >= 0, "Only non -empty polynomials can be evaluated."
        result = 0.0
        cur_node = self._poly_head
        while cur_node is not None:
            result += cur_node.coefficient * (scalar ** cur_node.degree)
            cur_node = cur_node.next
        return result

    def __add__(self, rhs_poly):
        """
        Polynomial addition: newPoly = self + rhs_poly.
        :param rhs_poly: Polynomial
        :return: Polynomial
        """
        return self.calculate("add", rhs_poly)

    def __sub__(self, rhs_poly):
        """
        Polynomial subtraction: newPoly = self - rhs_poly.
        :param rhs_poly:
        :return:
        """
        return self.calculate("sub", rhs_poly)

    def calculate(self, action, rhs_poly):
        """
        Calculate math expression on Polynomial.
        :param action: str
        :param rhs_poly: Polynomial
        :return: Polynomial
        """
        degrees_set = set(self.get_all_degrees() + rhs_poly.get_all_degrees())
        degrees_set = sorted(degrees_set, reverse=True)

        final_pol = Polynomial()

        for degree in degrees_set:
            if action == "add":
                coeff = self[degree] + rhs_poly[degree]
            else:
                coeff = self[degree] - rhs_poly[degree]
            final_pol._append_term(degree, coeff)

        return final_pol

    def get_all_degrees(self):
        """
        Get all degrees in the polynomial
        :return: list
        """
        degrees_list = []
        next_node = self._poly_head

        while next_node is not None:
            degrees_list.append(next_node.degree)
            next_node = next_node.next

        return degrees_list

    def __mul__(self, rhs_poly):
        """
        Polynomial multiplication: newPoly = self * rhs_poly.
        :param rhs_poly:
        :return:
        """
        self_next = self._poly_head
        final_pol = Polynomial()
        polynom_dict = dict()

        while self_next is not None:
            rhs_poly_next = rhs_poly._poly_head
            while rhs_poly_next is not None:
                degree = self_next.degree + rhs_poly_next.degree
                coeff = self_next.coefficient * rhs_poly_next.coefficient
                if degree in polynom_dict:
                    polynom_dict[degree] += coeff
                else:
                    polynom_dict[degree] = coeff
                rhs_poly_next = rhs_poly_next.next
            self_next = self_next.next

        degrees_set = sorted(polynom_dict.keys(), reverse=True)
        for degree in degrees_set:
            final_pol._append_term(degree, polynom_dict[degree])

        return final_pol

    def __str__(self):
        """
        Polynomial string representation.
        :return: str
        """
        output = ""
        if self._poly_head:
            output = str(self._poly_head)
        next_node = self._poly_head.next

        while next_node is not None:
            if str(next_node).startswith("- "):
                output += " " + str(next_node)
            else:
                output += " + " + str(next_node)
            next_node = next_node.next

        return output

    def _append_term(self, degree, coefficient):
        """
        Add new link to polynomial.
        :param degree: float
        :param coefficient: float
        :return: None
        """
        new_node = _PolyTermNode(degree, coefficient)
        if self._poly_tail is None:
            self._poly_head = new_node
            self._poly_tail = new_node
        else:
            self._poly_tail.next = new_node
            self._poly_tail = new_node


class _PolyTermNode:
    """
    Class for creating polynomial term nodes used with the linked list.
    """
    def __init__(self, degree, coefficient):
        self.degree = degree
        self.coefficient = coefficient
        self.next = None

    def __str__(self):
        """
        Prints the value stored in self.
        __str__: Node -> Str
        """
        if self.coefficient < 0:
            return "- " + str(abs(self.coefficient)) + "x" + str(self.degree)
        return str(self.coefficient) + "x" + str(self.degree)
