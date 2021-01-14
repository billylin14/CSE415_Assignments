import math
import re

def is_multiple_of_9(n):
    """Return True if n is a multiple of 9; False otherwise."""
    return n%9==0


def next_prime(m):
    """Return the first prime number p that is greater than m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    m+=1
    while not isPrime(m):
        m+=1
    return m
            
            
def isPrime(m):
    if m==1: return False
    elif m<=3: return True
    else: 
        for i in range (2, m): #m exclusive
            if m%i==0: return False
        return True



def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    num = b**2-4*a*c
    if num < 0: return "complex"
    else:
       roots=((-1*b-math.sqrt(num))/(2*a), (-1*b+math.sqrt(num))/(2*a))
       return roots



def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    For example, [0, 1, 2, 3, 4, 5, 6, 7] => [0, 4, 1, 5, 2, 6, 3, 7]"""
    firstHalf = even_list[:len(even_list)//2]
    secondHalf = even_list[len(even_list)//2:]
    newList = []
    for i in range(len(firstHalf)):
        newList.append(firstHalf[i])
        newList.append(secondHalf[i])
    return newList



def triples_list(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 3."""
    return [i*3 for i in input_list]
    


def double_consonants(text):
    """Return a new version of text, with all the consonants doubled.
    For example:  "The *BIG BAD* wolf!" => "TThhe *BBIGG BBADD* wwollff!"
    For this exercise assume the consonants are all letters OTHER
    THAN A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""
    newText = ""
    vowels = ['a', 'e', 'i', 'o', 'u']
    for char in text:
        if char.isalpha():
            if char.lower() not in vowels: 
                newText+=char
        newText+=char
    return newText




def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', '*', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ]  ).
    Convert all the letters to lower-case before the counting."""
    text = text.lower() #convert to all lower case
    text = re.sub(r"^[^a-zA-Z0-9-+*/@#%']+", "", text) #remove leading non-letters
    text = re.sub(r"[^a-zA-Z0-9-+*/@#%']+$", "", text) #remove trailing non-letters
    dic= {}
    for word in re.split(r"[^a-zA-Z0-9-+*/@#%']+", text):
        #print("word = \"", word, "\"")
        if word not in dic:
            dic[word] = 1
        else: 
            dic[word] += 1
    return dic

def make_cubic_evaluator(a, b, c, d):
    """When called with 4 numbers, returns a function of one variable (x)
    that evaluates the cubic polynomial
    a x^3 + b x^2 + c x + d.
    For this exercise Your function definition for make_cubic_evaluator
    should contain a lambda expression."""
    f = lambda x: a*x**3+b*x**2+c*x+d
    return f


class Polygon:
    """Polygon class."""
    def __init__ (self, n_sides, lengths=None, angles=None):
        self.n_sides = n_sides
        self.lengths = lengths
        self.angles = angles
    
    def is_rectangle(self):
        """returns True if the polygon is a rectangle,
        False if it is definitely not a rectangle, and None
        if the angle list is unknown (None). """
        if self.n_sides==4:
            if self.angles!=None:
                return all(angle==90 for angle in self.angles)
            # elif self.lengths!=None:
            #     if self.lengths==4:
            #         return all(self.lengths.count(length)>=2 for length in self.lengths)
            #     else:
            #         return False
            else:
                return None
        else:
            return False

    def is_rhombus(self):
        """returns True if the polygon is a rhombus,
        False if it is definitely not a rhombus, and None
        if the lengths list is unknown (None). """
        if self.n_sides==4:
            if self.lengths!=None:
                return self.lengths.count(self.lengths[0])==len(self.lengths)
            else:
                return None
        else:
            return False

    def is_square(self):
        """returns True if the polygon is a square,
        False if it is definitely not a square, and None
        if the lengths list or the angles list is unknown (None). """
        if self.n_sides==4:
            if self.angles!=None and self.lengths!=None:
                return all(angle==90 for angle in self.angles) and self.lengths.count(self.lengths[0])==len(self.lengths)
            else:
                if self.angles!=None and any(angle!=90 for angle in self.angles):
                    return False
                elif self.lengths!=None and self.lengths.count(self.lengths[0])!=len(self.lengths):
                    return False
                return None
        else:
            return False

    def is_regular_hexagon(self):
        """returns True if the polygon is a regular hexagon,
        False if it is definitely not a regular hexagon, and None
        if the lengths list and angles list are unknown (None). """
        if self.n_sides==6:
            if self.lengths!=None and self.angles!=None:
                return self.lengths.count(self.lengths[0])==len(self.lengths) and all(angle==120 for angle in self.angles)
            else:
                if self.lengths!=None:
                    if self.lengths.count(self.lengths[0])!=len(self.lengths):
                        return False
                    else: 
                        return None
                elif self.angles!=None:
                    if any(angle!=120 for angle in self.angles):
                        return False
                    else: 
                        return None
                else:
                    return None
        else:
            return False

    def is_isosceles_triangle(self):
        """returns True if the polygon is an isosceles triangle,
        False if it is definitely not an isosceles triangle, and None
        if the lengths list and angles list are unknown (None). """
        if self.n_sides==3:
            if self.lengths!=None:
                return any(self.lengths.count(length)>=2 for length in self.lengths)
            elif self.angles!=None:
                if len(self.angles)==3:
                    return any(self.angles.count(angle)>=2 for angle in self.angles)
                else:
                    return False
            else:
                return None
        else:
            return False

    def is_equilateral_triangle(self):
        """returns True if the polygon is an equilateral triangle,
        False if it is definitely not an equilateral triangle, and None
        if the lengths list and angles list are unknown (None). """
        if self.n_sides==3:
            if self.lengths!=None:
                return all(self.lengths.count(length)==3 for length in self.lengths)
            elif self.angles!=None:
                if len(self.angles)==3:
                    return all(angle==60 for angle in self.angles)
                else:
                    return False
            else:
                return None
        else:
            return False


    def is_scalene_triangle(self):
        """returns True if the polygon is a scalene triangle,
        False if it is definitely not a scalene triangle, and None
        if the lengths list or angles list are unknown (None). """
        if self.n_sides==3:
            result = self.is_isosceles_triangle() or self.is_equilateral_triangle()
            if result is None:
                return None
            else:
                return not(result)
        else:
            return False
    
               
