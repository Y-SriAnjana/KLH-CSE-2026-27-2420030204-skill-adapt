"""
SkillAdapt - Seed Data Generator
Generates realistic initial question banks, learning resources, ML synthetic dataset,
and demo user records for the SkillAdapt personalized learning platform.
"""

import json
import os
import hashlib
import secrets
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"{salt}:{key.hex()}"

# 1. Comprehensive Question Bank
QUESTIONS = [
    # ==================== PYTHON ====================
    {
        "question_id": "PY_001",
        "subject": "Python",
        "topic": "Python Basics & Syntax",
        "question_text": "Which of the following is an immutable data type in Python?",
        "options": ["List", "Dictionary", "Tuple", "Set"],
        "correct_answer": "Tuple",
        "explanation": "Tuples in Python cannot be modified once created, making them immutable. Lists, dictionaries, and sets are mutable.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "PY_002",
        "subject": "Python",
        "topic": "Python Basics & Syntax",
        "question_text": "What is the output of bool('False') in Python?",
        "options": ["False", "True", "None", "ValueError"],
        "correct_answer": "True",
        "explanation": "Any non-empty string in Python evaluates to True in a boolean context, regardless of string contents.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "PY_003",
        "subject": "Python",
        "topic": "Control Flow & Loops",
        "question_text": "What will `range(2, 10, 3)` produce when converted to a list?",
        "options": ["[2, 5, 8]", "[2, 5, 8, 11]", "[3, 6, 9]", "[2, 4, 6, 8]"],
        "correct_answer": "[2, 5, 8]",
        "explanation": "range(start, stop, step) starts at 2, increments by 3, and stops strictly before 10: 2, 5, 8.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "PY_004",
        "subject": "Python",
        "topic": "Functions & Scope",
        "question_text": "How does Python handle default mutable arguments (like def f(x=[]) )?",
        "options": [
            "A new list is created on every function call",
            "The list is instantiated once at function definition time and shared across calls",
            "Python raises a SyntaxError at compile time",
            "The list is automatically copied into local scope"
        ],
        "correct_answer": "The list is instantiated once at function definition time and shared across calls",
        "explanation": "Default argument expressions are evaluated once when the function definition is executed, leading to a persistent mutable object across invocations.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "PY_005",
        "subject": "Python",
        "topic": "Functions & Scope",
        "question_text": "What does the *args and **kwargs syntax in a Python function definition allow?",
        "options": [
            "Pointers to integer memory addresses",
            "Passing variable numbers of positional and keyword arguments respectively",
            "Passing mandatory keyword-only arguments",
            "Multiplying arguments by integer scale factors"
        ],
        "correct_answer": "Passing variable numbers of positional and keyword arguments respectively",
        "explanation": "*args collects arbitrary positional arguments as a tuple, while **kwargs collects arbitrary keyword arguments as a dictionary.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "PY_006",
        "subject": "Python",
        "topic": "Object-Oriented Python",
        "question_text": "In Python multiple inheritance, which algorithm determines the Method Resolution Order (MRO)?",
        "options": ["Depth-First Traversal", "C3 Linearization Algorithm", "Breadth-First Search", "Dijkstra Algorithm"],
        "correct_answer": "C3 Linearization Algorithm",
        "explanation": "Python uses the C3 Linearization algorithm to determine the Method Resolution Order (MRO) across complex inheritance hierarchies.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "PY_007",
        "subject": "Python",
        "topic": "Object-Oriented Python",
        "question_text": "What does defining `__slots__` inside a Python class accomplish?",
        "options": [
            "Restricts attribute creation and avoids creating an instance `__dict__`, reducing memory",
            "Enables multithreaded locks on class variables",
            "Automatically generates getter and setter properties",
            "Makes the class inherit directly from object metaclasses"
        ],
        "correct_answer": "Restricts attribute creation and avoids creating an instance `__dict__`, reducing memory",
        "explanation": "__slots__ reserves space for declared attributes, prevents dynamic __dict__ creation per instance, saving significant memory.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "PY_008",
        "subject": "Python",
        "topic": "Control Flow & Loops",
        "question_text": "When does the `else` clause attached to a Python `for` or `while` loop execute?",
        "options": [
            "Whenever the loop terminates normally without encountering a `break` statement",
            "Only when the loop condition evaluates to False on the very first check",
            "Every time after a `break` is triggered",
            "When an unhandled exception occurs inside the loop"
        ],
        "correct_answer": "Whenever the loop terminates normally without encountering a `break` statement",
        "explanation": "A loop's `else` block runs when the loop finishes its iterations without being interrupted by a `break`.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "PY_009",
        "subject": "Python",
        "topic": "Exception Handling & File I/O",
        "question_text": "Which clause in a Python try/except block is guaranteed to execute regardless of whether an exception occurred or was handled?",
        "options": ["finally", "else", "catch", "defer"],
        "correct_answer": "finally",
        "explanation": "The `finally` block always executes during clean-up actions, whether an exception was raised, handled, or even if return was called.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "PY_010",
        "subject": "Python",
        "topic": "Advanced Comprehensions & Generators",
        "question_text": "What is the key advantage of using a Generator expression `(x*2 for x in data)` instead of a List comprehension `[x*2 for x in data]`?",
        "options": [
            "Generators yield items lazily on demand, consuming minimal memory O(1)",
            "Generators execute in parallel on all CPU cores",
            "Generators allow arbitrary random index access",
            "Generators can only be iterated over backwards"
        ],
        "correct_answer": "Generators yield items lazily on demand, consuming minimal memory O(1)",
        "explanation": "Generators evaluate expressions lazily using the iterator protocol, maintaining O(1) space complexity regardless of stream size.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "PY_011",
        "subject": "Python",
        "topic": "Advanced Comprehensions & Generators",
        "question_text": "How does Python's GIL (Global Interpreter Lock) impact CPU-bound multithreaded programs in CPython?",
        "options": [
            "It allows multiple native threads to execute Python bytecode simultaneously across cores",
            "It restricts bytecode execution to one native thread at a time, preventing true multi-core CPU scaling",
            "It prevents threads from sharing process memory",
            "It automatically compiles Python loops to vectorized GPU code"
        ],
        "correct_answer": "It restricts bytecode execution to one native thread at a time, preventing true multi-core CPU scaling",
        "explanation": "CPython's GIL ensures thread-safe memory management by allowing only one thread to execute Python bytecode at any given instant.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "PY_012",
        "subject": "Python",
        "topic": "Exception Handling & File I/O",
        "question_text": "What happens when using the `with open(...) as f:` context manager in Python?",
        "options": [
            "The file descriptor is automatically closed upon leaving the block, even if an exception occurs",
            "The file contents are permanently locked from write operations",
            "The entire file is pre-loaded into an in-memory SQLite table",
            "The file pointer is reset to byte zero on every iteration"
        ],
        "correct_answer": "The file descriptor is automatically closed upon leaving the block, even if an exception occurs",
        "explanation": "The context manager protocol calls `__enter__` on entry and `__exit__` on departure, ensuring resources are reliably freed.",
        "difficulty": "Easy",
        "marks": 1
    },

    # ==================== JAVA ====================
    {
        "question_id": "JAVA_001",
        "subject": "Java",
        "topic": "Java Syntax & Basics",
        "question_text": "Which Java primitive type has a size of exactly 8 bits?",
        "options": ["byte", "short", "char", "boolean"],
        "correct_answer": "byte",
        "explanation": "In Java, a byte is an 8-bit signed two's complement integer, ranging from -128 to 127.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "JAVA_002",
        "subject": "Java",
        "topic": "Java Syntax & Basics",
        "question_text": "What is the default value of an uninitialized instance boolean variable in Java?",
        "options": ["false", "true", "null", "0"],
        "correct_answer": "false",
        "explanation": "Uninitialized boolean instance variables in Java default to false.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "JAVA_003",
        "subject": "Java",
        "topic": "OOP Concepts in Java",
        "question_text": "Which keyword prevents a Java class from being subclassed / extended?",
        "options": ["abstract", "static", "final", "sealed"],
        "correct_answer": "final",
        "explanation": "Declaring a class as `final` prevents it from being extended by any other class.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "JAVA_004",
        "subject": "Java",
        "topic": "OOP Concepts in Java",
        "question_text": "What is the primary difference between method overloading and method overriding?",
        "options": [
            "Overloading happens at runtime within subclasses; overriding happens at compile time",
            "Overloading involves same method name with different parameters; overriding replaces a superclass method with identical signature",
            "Overriding requires static methods, while overloading requires instance methods",
            "Overloading requires abstract classes, whereas overriding applies to concrete classes only"
        ],
        "correct_answer": "Overloading involves same method name with different parameters; overriding replaces a superclass method with identical signature",
        "explanation": "Method overloading is compile-time polymorphism (differing parameter lists), whereas overriding is runtime polymorphism with the identical method signature in a subclass.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "JAVA_005",
        "subject": "Java",
        "topic": "Collections Framework",
        "question_text": "Which Java Collections interface guarantees elements are stored in ascending sorted order?",
        "options": ["Set", "SortedSet / NavigableSet", "List", "Queue"],
        "correct_answer": "SortedSet / NavigableSet",
        "explanation": "SortedSet and its sub-interface NavigableSet (implemented by TreeSet) guarantee natural ascending order or custom Comparator ordering.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "JAVA_006",
        "subject": "Java",
        "topic": "Multithreading & Concurrency",
        "question_text": "What does the `volatile` keyword in Java guarantee for a variable?",
        "options": [
            "Atomic increment operations and thread locking",
            "Visibility of changes across threads by reading/writing directly to main memory",
            "Prevention of garbage collection on that reference",
            "Serialization across remote JVM nodes"
        ],
        "correct_answer": "Visibility of changes across threads by reading/writing directly to main memory",
        "explanation": "The `volatile` modifier ensures that reads and writes are done directly to main memory, avoiding CPU cache staleness, but it does not guarantee atomicity of compound operations.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "JAVA_007",
        "subject": "Java",
        "topic": "Multithreading & Concurrency",
        "question_text": "How does `ConcurrentHashMap` achieve high throughput compared to `Collections.synchronizedMap`?",
        "options": [
            "By locking the entire hash table on every read and write",
            "By utilizing lock striping / node-level synchronization instead of a single global lock",
            "By writing updates to an in-memory disk cache",
            "By executing all write operations in a single background thread"
        ],
        "correct_answer": "By utilizing lock striping / node-level synchronization instead of a single global lock",
        "explanation": "ConcurrentHashMap synchronizes at individual bucket/node levels using CAS and synchronized blocks, allowing concurrent writes without blocking unrelated buckets.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "JAVA_008",
        "subject": "Java",
        "topic": "Collections Framework",
        "question_text": "What happens in a Java HashMap when the load factor threshold (default 0.75) is exceeded?",
        "options": [
            "An OutOfMemoryError is thrown",
            "The capacity doubles and all existing entries are rehashed into new buckets",
            "The oldest entries are evicted via LRU policy",
            "A secondary tree bucket is written to temporary swap space"
        ],
        "correct_answer": "The capacity doubles and all existing entries are rehashed into new buckets",
        "explanation": "When the number of entries exceeds threshold (capacity * loadFactor), the table capacity is doubled and elements are rehashed.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "JAVA_009",
        "subject": "Java",
        "topic": "Generics & Lambdas",
        "question_text": "What is type erasure in Java generics?",
        "options": [
            "Removing type arguments at compile time so bytecode retains backwards compatibility with older JVM versions",
            "Deleting unused class definitions during garbage collection",
            "Converting object references into raw memory pointers at runtime",
            "Enforcing strict runtime class casting on all generic method invocations"
        ],
        "correct_answer": "Removing type arguments at compile time so bytecode retains backwards compatibility with older JVM versions",
        "explanation": "Java generics are implemented via type erasure: the compiler verifies type safety and inserts necessary casts, then erases generic type parameters in bytecode.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "JAVA_010",
        "subject": "Java",
        "topic": "Exception Handling",
        "question_text": "Which exception class hierarchy in Java represents unchecked exceptions that do not require explicit throws declarations?",
        "options": ["RuntimeException and its subclasses", "IOException and its subclasses", "SQLException", "ClassNotFoundException"],
        "correct_answer": "RuntimeException and its subclasses",
        "explanation": "In Java, RuntimeException (and Error) are unchecked exceptions and do not need to be declared in method signatures or caught explicitly.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "JAVA_011",
        "subject": "Java",
        "topic": "Generics & Lambdas",
        "question_text": "What is a Functional Interface in Java (introduced in Java 8)?",
        "options": [
            "An interface containing exactly one abstract method",
            "An interface that cannot have static utility methods",
            "An interface implemented only by anonymous inner classes",
            "An interface with no methods at all (marker interface)"
        ],
        "correct_answer": "An interface containing exactly one abstract method",
        "explanation": "A functional interface has exactly one abstract method (SAM - Single Abstract Method) and can be instantiated via lambda expressions or method references.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "JAVA_012",
        "subject": "Java",
        "topic": "OOP Concepts in Java",
        "question_text": "What is the difference between String, StringBuilder, and StringBuffer in Java?",
        "options": [
            "String is immutable; StringBuffer is mutable and thread-safe; StringBuilder is mutable and not synchronized (faster)",
            "String is thread-safe; StringBuilder is immutable; StringBuffer is deprecated",
            "All three are identical in terms of mutability and thread safety",
            "StringBuilder stores UTF-16, while StringBuffer stores ASCII only"
        ],
        "correct_answer": "String is immutable; StringBuffer is mutable and thread-safe; StringBuilder is mutable and not synchronized (faster)",
        "explanation": "String objects cannot change in place. StringBuffer uses synchronized methods for multi-thread safety. StringBuilder removes synchronization for higher single-threaded speed.",
        "difficulty": "Medium",
        "marks": 2
    },

    # ==================== DATA STRUCTURES ====================
    {
        "question_id": "DS_001",
        "subject": "Data Structures",
        "topic": "Arrays & Strings",
        "question_text": "What is the worst-case time complexity to access an element by index in a contiguous array?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_answer": "O(1)",
        "explanation": "Arrays provide direct address arithmetic (base_address + index * element_size), giving constant time O(1) random access.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "DS_002",
        "subject": "Data Structures",
        "topic": "Stacks & Queues",
        "question_text": "Which principle does a Queue data structure follow?",
        "options": ["LIFO (Last In, First Out)", "FIFO (First In, First Out)", "FILO (First In, Last Out)", "Random Access"],
        "correct_answer": "FIFO (First In, First Out)",
        "explanation": "Queues operate on First In First Out (FIFO): elements are inserted at the rear and removed from the front.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "DS_003",
        "subject": "Data Structures",
        "topic": "Linked Lists",
        "question_text": "What is the time complexity to insert a new node at the head of a Singly Linked List?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
        "correct_answer": "O(1)",
        "explanation": "Inserting at the head requires simply pointing the new node to the current head and updating the head pointer, taking O(1) operations.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "DS_004",
        "subject": "Data Structures",
        "topic": "Trees & Binary Search Trees",
        "question_text": "In a balanced Binary Search Tree (like an AVL tree), what is the worst-case time complexity for search, insertion, and deletion?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_answer": "O(log n)",
        "explanation": "AVL and Red-Black trees maintain height bounded by O(log n), guaranteeing logarithmic worst-case search, insertion, and deletion.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "DS_005",
        "subject": "Data Structures",
        "topic": "Sorting & Searching",
        "question_text": "Which sorting algorithm has a worst-case time complexity of O(n log n) and is guaranteed to be stable?",
        "options": ["Quick Sort", "Merge Sort", "Heap Sort", "Selection Sort"],
        "correct_answer": "Merge Sort",
        "explanation": "Merge Sort is guaranteed O(n log n) in all cases (worst, average, best) and preserves relative order of identical keys (stable).",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "DS_006",
        "subject": "Data Structures",
        "topic": "Graphs & Graph Algorithms",
        "question_text": "Which algorithm is suitable for finding all-pairs shortest paths in a directed weighted graph that may contain negative edges (but no negative cycles)?",
        "options": ["Dijkstra's Algorithm", "Floyd-Warshall Algorithm", "Prim's Algorithm", "Kruskal's Algorithm"],
        "correct_answer": "Floyd-Warshall Algorithm",
        "explanation": "Floyd-Warshall dynamic programming computes all-pairs shortest paths in O(V^3) time and supports negative edge weights (as long as no negative cycle exists).",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "DS_007",
        "subject": "Data Structures",
        "topic": "Graphs & Graph Algorithms",
        "question_text": "What is the time complexity of Breadth-First Search (BFS) using an adjacency list representation on a graph with V vertices and E edges?",
        "options": ["O(V + E)", "O(V * E)", "O(V^2)", "O(E log V)"],
        "correct_answer": "O(V + E)",
        "explanation": "BFS visits every vertex once and explores every edge incident to it once, yielding linear time O(V + E).",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "DS_008",
        "subject": "Data Structures",
        "topic": "Trees & Binary Search Trees",
        "question_text": "In a Red-Black Tree, what is the maximum possible height relative to the black-height (bh)?",
        "options": ["bh", "2 * bh", "bh^2", "log(bh)"],
        "correct_answer": "2 * bh",
        "explanation": "Because red nodes cannot be adjacent, any root-to-leaf path contains at most alternating red and black nodes, so the total height is at most 2 * bh <= 2 * log2(n + 1).",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "DS_009",
        "subject": "Data Structures",
        "topic": "Dynamic Programming Foundations",
        "question_text": "Which two core characteristics must an optimization problem possess to be solvable via Dynamic Programming?",
        "options": [
            "Optimal Substructure and Overlapping Subproblems",
            "Greedy Choice Property and Infinite Recursion",
            "Divide and Conquer and Branch & Bound",
            "Linear Independence and Constant Factors"
        ],
        "correct_answer": "Optimal Substructure and Overlapping Subproblems",
        "explanation": "Dynamic programming applies when the optimal solution to the problem incorporates optimal solutions to subproblems, and subproblems are solved repeatedly.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "DS_010",
        "subject": "Data Structures",
        "topic": "Arrays & Strings",
        "question_text": "What is the amortized time complexity of inserting n items consecutively into a dynamic array (like Python's list or C++ vector)?",
        "options": ["O(1) per insertion on average, O(n) total", "O(n) per insertion", "O(log n) per insertion", "O(n^2) total"],
        "correct_answer": "O(1) per insertion on average, O(n) total",
        "explanation": "Geometric doubling of capacity ensures that n insertions require at most 2n copies in total, resulting in amortized O(1) time per append.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "DS_011",
        "subject": "Data Structures",
        "topic": "Sorting & Searching",
        "question_text": "What is the best-case time complexity of Quick Sort with median-of-three pivot selection?",
        "options": ["O(n log n)", "O(n^2)", "O(n)", "O(1)"],
        "correct_answer": "O(n log n)",
        "explanation": "When partitions split into roughly equal halves, the recursion depth is log2(n), yielding O(n log n) best-case and average-case performance.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "DS_012",
        "subject": "Data Structures",
        "topic": "Dynamic Programming Foundations",
        "question_text": "What is the time complexity to solve the 0/1 Knapsack Problem with N items and capacity W using Dynamic Programming?",
        "options": ["O(N * W)", "O(2^N)", "O(N log W)", "O(W^2)"],
        "correct_answer": "O(N * W)",
        "explanation": "The DP table requires (N + 1) * (W + 1) states, with each cell computed in constant O(1) time, giving pseudo-polynomial time O(N * W).",
        "difficulty": "Hard",
        "marks": 3
    },

    # ==================== SQL ====================
    {
        "question_id": "SQL_001",
        "subject": "SQL",
        "topic": "SELECT & Basic Filtering",
        "question_text": "Which SQL clause is used to eliminate duplicate rows from a query result set?",
        "options": ["UNIQUE", "DISTINCT", "DIFFERENT", "GROUP"],
        "correct_answer": "DISTINCT",
        "explanation": "The SELECT DISTINCT syntax removes duplicate identical records from query output.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "SQL_002",
        "subject": "SQL",
        "topic": "SELECT & Basic Filtering",
        "question_text": "Which SQL operator matches a pattern containing wildcard characters such as '%' or '_'?",
        "options": ["EQUALS", "IN", "LIKE", "MATCHES"],
        "correct_answer": "LIKE",
        "explanation": "The LIKE operator evaluates pattern matches where '%' represents zero or more characters and '_' represents a single character.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "SQL_003",
        "subject": "SQL",
        "topic": "Joins & Set Operations",
        "question_text": "Which JOIN returns all rows from the left table and matching rows from the right table, filling nulls where there is no match?",
        "options": ["INNER JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "CROSS JOIN"],
        "correct_answer": "LEFT OUTER JOIN",
        "explanation": "A LEFT OUTER JOIN preserves all records from the left table regardless of whether a matching record exists in the right table.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "SQL_004",
        "subject": "SQL",
        "topic": "Aggregations & GROUP BY",
        "question_text": "What is the crucial difference between the WHERE clause and the HAVING clause in SQL?",
        "options": [
            "WHERE filters rows before aggregation; HAVING filters aggregated groups",
            "WHERE only works on numeric columns; HAVING works on text",
            "HAVING cannot be used together with GROUP BY",
            "WHERE is executed after the GROUP BY calculation completes"
        ],
        "correct_answer": "WHERE filters rows before aggregation; HAVING filters aggregated groups",
        "explanation": "WHERE filters individual rows prior to grouping, while HAVING applies conditions to aggregated metric calculations (like COUNT, SUM, AVG).",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "SQL_005",
        "subject": "SQL",
        "topic": "Subqueries & CTEs",
        "question_text": "What is a Common Table Expression (CTE) in SQL?",
        "options": [
            "A temporary named result set defined using the WITH clause",
            "A permanent physical table created in system tablespace",
            "A clustered index on composite primary keys",
            "A database stored procedure returning void"
        ],
        "correct_answer": "A temporary named result set defined using the WITH clause",
        "explanation": "A CTE is a temporary named result set defined by `WITH cte_name AS (...)` that can be referenced within the scope of a SELECT, INSERT, UPDATE, or DELETE.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "SQL_006",
        "subject": "SQL",
        "topic": "Indexing & Query Optimization",
        "question_text": "What is a 'covering index' in relational databases?",
        "options": [
            "An index that encrypts sensitive column values",
            "An index that includes all columns referenced by a query, allowing the engine to satisfy the query entirely from the index without a table lookup",
            "An index applied automatically to every foreign key constraint",
            "An index that spans all tables across the entire schema"
        ],
        "correct_answer": "An index that includes all columns referenced by a query, allowing the engine to satisfy the query entirely from the index without a table lookup",
        "explanation": "A covering index contains all the columns needed for the SELECT, WHERE, and JOIN clauses, eliminating the need to read table heap pages (Index-Only Scan).",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "SQL_007",
        "subject": "SQL",
        "topic": "Indexing & Query Optimization",
        "question_text": "Under the ANSI SQL standard, which transaction isolation level prevents dirty reads, non-repeatable reads, and phantom reads?",
        "options": ["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"],
        "correct_answer": "Serializable",
        "explanation": "Serializable is the highest isolation level and strictly prevents dirty reads, non-repeatable reads, and phantom reads.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "SQL_008",
        "subject": "SQL",
        "topic": "Joins & Set Operations",
        "question_text": "What does a FULL OUTER JOIN produce in SQL?",
        "options": [
            "Only rows with identical primary keys across both tables",
            "All rows from both tables, filling NULL where join conditions are not met on either side",
            "Cartesian product of all rows without checking conditions",
            "Only rows where right table matches left table"
        ],
        "correct_answer": "All rows from both tables, filling NULL where join conditions are not met on either side",
        "explanation": "FULL OUTER JOIN combines the results of both LEFT and RIGHT outer joins, outputting all rows and padding nulls where no match occurs.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "SQL_009",
        "subject": "SQL",
        "topic": "Constraints & DDL",
        "question_text": "Which SQL constraint ensures that all values in a column are distinct and cannot contain NULL values?",
        "options": ["PRIMARY KEY", "UNIQUE", "FOREIGN KEY", "CHECK"],
        "correct_answer": "PRIMARY KEY",
        "explanation": "A PRIMARY KEY constraint uniquely identifies each record in a table. It implicitly enforces both UNIQUE and NOT NULL constraints.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "SQL_010",
        "subject": "SQL",
        "topic": "Subqueries & CTEs",
        "question_text": "What is a Correlated Subquery in SQL?",
        "options": [
            "A subquery that references columns from the outer query and executes once for each candidate row processed by the outer query",
            "A subquery that runs independently of outer queries and caches its entire result table",
            "A subquery that performs cross-database replication",
            "A subquery used strictly inside the FROM clause"
        ],
        "correct_answer": "A subquery that references columns from the outer query and executes once for each candidate row processed by the outer query",
        "explanation": "Correlated subqueries depend on the values of the current row in the outer query, evaluating repeatedly for each row.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "SQL_011",
        "subject": "SQL",
        "topic": "Aggregations & GROUP BY",
        "question_text": "What does the COUNT(*) function return in SQL?",
        "options": [
            "The total number of rows in the table or group, including rows with NULL values",
            "Only rows where primary keys are positive integers",
            "Total number of columns in the result set",
            "Total non-null values in the first column only"
        ],
        "correct_answer": "The total number of rows in the table or group, including rows with NULL values",
        "explanation": "COUNT(*) counts total rows in the target table or grouped partition, regardless of whether specific columns contain NULL.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "SQL_012",
        "subject": "SQL",
        "topic": "Indexing & Query Optimization",
        "question_text": "What is the primary difference between a Clustered Index and a Non-Clustered Index?",
        "options": [
            "A clustered index physically determines the order in which rows are stored on disk; a non-clustered index stores a separate pointer structure",
            "A table can have multiple clustered indexes, but only one non-clustered index",
            "Non-clustered indexes are stored in memory only, while clustered indexes are on disk",
            "Clustered indexes cannot be used for range queries"
        ],
        "correct_answer": "A clustered index physically determines the order in which rows are stored on disk; a non-clustered index stores a separate pointer structure",
        "explanation": "Because a table's physical rows can only be ordered one way, there can only be one clustered index per table. Non-clustered indexes maintain auxiliary pointer pages.",
        "difficulty": "Hard",
        "marks": 3
    },

    # ==================== MACHINE LEARNING ====================
    {
        "question_id": "ML_001",
        "subject": "Machine Learning",
        "topic": "Supervised Learning",
        "question_text": "Which of the following is an example of a Supervised Learning task?",
        "options": [
            "Clustering customer profiles using K-Means",
            "Predicting house prices given historical sales features and target prices",
            "Dimensionality reduction using Principal Component Analysis",
            "Market basket analysis using Apriori algorithm"
        ],
        "correct_answer": "Predicting house prices given historical sales features and target prices",
        "explanation": "Predicting house prices relies on labeled training pairs (input features and ground-truth target price), which defines Supervised Learning.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "ML_002",
        "subject": "Machine Learning",
        "topic": "Supervised Learning",
        "question_text": "What type of problem is being solved when the target variable is continuous (e.g., student marks or salary)?",
        "options": ["Classification", "Regression", "Clustering", "Association"],
        "correct_answer": "Regression",
        "explanation": "Regression algorithms predict continuous numerical targets, whereas classification predicts discrete class labels.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "ML_003",
        "subject": "Machine Learning",
        "topic": "Model Evaluation & Metrics",
        "question_text": "What is the formula for Accuracy in a binary classification confusion matrix?",
        "options": [
            "(TP + TN) / (TP + TN + FP + FN)",
            "TP / (TP + FP)",
            "TP / (TP + FN)",
            "TN / (TN + FP)"
        ],
        "correct_answer": "(TP + TN) / (TP + TN + FP + FN)",
        "explanation": "Accuracy is the ratio of correctly predicted observations (True Positives + True Negatives) to the total observations.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "ML_004",
        "subject": "Machine Learning",
        "topic": "Model Evaluation & Metrics",
        "question_text": "What does a high Mean Absolute Error (MAE) indicate in a regression model?",
        "options": [
            "The model has zero residual variance",
            "On average, the predicted values deviate significantly from actual ground truth values",
            "The model is guaranteed to be overfitting the training data",
            "The target variable has high class imbalance"
        ],
        "correct_answer": "On average, the predicted values deviate significantly from actual ground truth values",
        "explanation": "MAE measures the average magnitude of absolute errors between predicted values and actual observation targets.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "ML_005",
        "subject": "Machine Learning",
        "topic": "Preprocessing & Feature Engineering",
        "question_text": "Why is feature scaling (e.g. StandardScaler or MinMaxScaler) crucial for distance-based algorithms like KNN and SVM?",
        "options": [
            "It prevents division by zero in categorical columns",
            "Features with larger numerical scales would otherwise dominate the Euclidean distance calculations",
            "It automatically converts non-linear relationships to linear relationships",
            "It eliminates all outliers from the dataset"
        ],
        "correct_answer": "Features with larger numerical scales would otherwise dominate the Euclidean distance calculations",
        "explanation": "Distance-based models compute Euclidean/Manhattan distances; without scaling, features with large numeric ranges heavily bias distance calculations.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "ML_006",
        "subject": "Machine Learning",
        "topic": "Overfitting & Regularization",
        "question_text": "What is the primary difference between L1 (Lasso) and L2 (Ridge) regularization?",
        "options": [
            "L1 adds squared coefficient penalty; L2 adds absolute coefficient penalty",
            "L1 adds absolute value penalty and can drive coefficients exactly to zero (feature selection); L2 penalizes squared weights",
            "L2 produces sparse models, whereas L1 never eliminates features",
            "L1 is only used in neural networks, whereas L2 is used only in linear regression"
        ],
        "correct_answer": "L1 adds absolute value penalty and can drive coefficients exactly to zero (feature selection); L2 penalizes squared weights",
        "explanation": "Lasso (L1) uses |w| penalty resulting in sparse weights (automatic feature selection). Ridge (L2) uses w^2 penalty shrinking weights smoothly toward zero.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "ML_007",
        "subject": "Machine Learning",
        "topic": "Overfitting & Regularization",
        "question_text": "In the Bias-Variance tradeoff, what condition is typically characterized by high training error and high validation error?",
        "options": ["High Variance (Overfitting)", "High Bias (Underfitting)", "Optimal Convergence", "Data Leakage"],
        "correct_answer": "High Bias (Underfitting)",
        "explanation": "High bias occurs when an overly simplistic model fails to capture underlying patterns, causing poor performance on both training and test data.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "ML_008",
        "subject": "Machine Learning",
        "topic": "Neural Networks & Deep Learning",
        "question_text": "How does the Vanishing Gradient problem manifest during backpropagation in deep neural networks using Sigmoid activations?",
        "options": [
            "Gradients become exponentially large, causing numeric overflow (NaN)",
            "Gradients become near zero as derivatives of sigmoid saturate at extremes, preventing early layers from updating weights",
            "Loss fluctuates wildly without converging",
            "The learning rate dynamically increases to infinity"
        ],
        "correct_answer": "Gradients become near zero as derivatives of sigmoid saturate at extremes, preventing early layers from updating weights",
        "explanation": "The maximum derivative of the sigmoid function is 0.25; chaining multiple layers multiplies fractions < 1, causing gradients to diminish exponentially towards zero.",
        "difficulty": "Hard",
        "marks": 3
    },
    {
        "question_id": "ML_009",
        "subject": "Machine Learning",
        "topic": "Unsupervised Learning & Clustering",
        "question_text": "In the K-Means clustering algorithm, how are cluster centroids updated at each iterative step?",
        "options": [
            "By computing the mean coordinates of all data points currently assigned to each cluster",
            "By selecting random boundary points on the convex hull",
            "By taking the median of the farthest outlier points",
            "By running Principal Component Analysis on the assignment matrix"
        ],
        "correct_answer": "By computing the mean coordinates of all data points currently assigned to each cluster",
        "explanation": "After assigning points to their nearest centroid, each centroid is updated to the geometric mean (center of mass) of all assigned points.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "ML_010",
        "subject": "Machine Learning",
        "topic": "Model Evaluation & Metrics",
        "question_text": "What does an R-squared (R2) score of 0.85 indicate in regression analysis?",
        "options": [
            "85% of the total variance in the dependent target variable is explained by the independent features in the model",
            "The model has an 85% probability of classifying a sample correctly",
            "The Mean Absolute Error is bounded strictly by 0.15",
            "85% of training samples were correctly predicted with zero error"
        ],
        "correct_answer": "85% of the total variance in the dependent target variable is explained by the independent features in the model",
        "explanation": "The coefficient of determination R2 measures the proportion of variance in the dependent variable predictable from the explanatory features.",
        "difficulty": "Medium",
        "marks": 2
    },
    {
        "question_id": "ML_011",
        "subject": "Machine Learning",
        "topic": "Preprocessing & Feature Engineering",
        "question_text": "What is the One-Hot Encoding technique primarily used for?",
        "options": [
            "Converting nominal categorical variables into binary dummy vectors without imposing false ordinal hierarchy",
            "Compressing image resolutions into 8-bit color channels",
            "Encrypting training labels with hash functions",
            "Normalizing continuous numbers to zero mean and unit variance"
        ],
        "correct_answer": "Converting nominal categorical variables into binary dummy vectors without imposing false ordinal hierarchy",
        "explanation": "One-hot encoding represents categorical levels as distinct binary columns (0 or 1), preventing machine learning algorithms from assuming an arbitrary numerical ordering.",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "question_id": "ML_012",
        "subject": "Machine Learning",
        "topic": "Neural Networks & Deep Learning",
        "question_text": "Why is the ReLU (Rectified Linear Unit, f(x) = max(0, x)) activation function preferred over Sigmoid in hidden layers of deep neural networks?",
        "options": [
            "Its gradient is 1 for positive inputs, which mitigates the vanishing gradient problem and accelerates training",
            "It maps all outputs smoothly into the bounded interval (0, 1)",
            "It guarantees that weights will never saturate or become zero",
            "It automatically performs L1 regularization across all synapses"
        ],
        "correct_answer": "Its gradient is 1 for positive inputs, which mitigates the vanishing gradient problem and accelerates training",
        "explanation": "ReLU has a constant derivative of 1 for x > 0, which prevents gradients from decaying through many backpropagation layers, while also being computationally efficient.",
        "difficulty": "Medium",
        "marks": 2
    }
]

# 2. Structured Learning Resources
LEARNING_RESOURCES = [
    # Python Resources
    {
        "resource_id": "RES_PY_01",
        "subject": "Python",
        "topic": "Python Basics & Syntax",
        "prerequisites": [],
        "title": "Mastering Python Data Types & Immutability",
        "description": "Comprehensive guide covering primitive data types, tuples vs lists, set theory, and memory representation in Python.",
        "learning_objectives": [
            "Understand mutable vs immutable objects in CPython",
            "Learn memory address inspection using id() and is operator",
            "Practice slicing, type casting, and literal notation"
        ],
        "estimated_minutes": 25,
        "difficulty": "Beginner",
        "resource_type": "Concept Guide",
        "summary_content": "In Python, objects are either mutable (can change in-place) or immutable (cannot be altered once allocated). Tuples, strings, and ints are immutable; lists, dictionaries, and sets are mutable. Understanding this distinction prevents common reference bugs.",
        "reference_url": "https://docs.python.org/3/tutorial/datastructures.html"
    },
    {
        "resource_id": "RES_PY_02",
        "subject": "Python",
        "topic": "Control Flow & Loops",
        "prerequisites": ["Python Basics & Syntax"],
        "title": "Iterators, Comprehensions, and Control Flow",
        "description": "Deep-dive into pythonic loop constructs, range generators, list comprehensions, and loop else clauses.",
        "learning_objectives": [
            "Implement clean list, dict, and set comprehensions",
            "Master while/else and for/else behavior with break/continue",
            "Utilize enumerate() and zip() for efficient iteration"
        ],
        "estimated_minutes": 30,
        "difficulty": "Intermediate",
        "resource_type": "Interactive Tutorial",
        "summary_content": "Python's iteration model allows idiomatic looping. The `for...else` pattern triggers only when the loop completes without hitting `break`. List comprehensions provide an expressive, optimized alternative to explicit map and filter loops.",
        "reference_url": "https://docs.python.org/3/tutorial/controlflow.html"
    },
    {
        "resource_id": "RES_PY_03",
        "subject": "Python",
        "topic": "Functions & Scope",
        "prerequisites": ["Control Flow & Loops"],
        "title": "Advanced Functions: *args, **kwargs & Closures",
        "description": "Demystify parameter packing/unpacking, default argument traps, scope resolution (LEGB), and inner closures.",
        "learning_objectives": [
            "Avoid default mutable argument traps",
            "Apply *args and **kwargs in flexible wrapper APIs",
            "Understand Local, Enclosing, Global, and Built-in (LEGB) scoping"
        ],
        "estimated_minutes": 35,
        "difficulty": "Intermediate",
        "resource_type": "Code Walkthrough",
        "summary_content": "Functions in Python are first-class citizens. Avoid `def func(lst=[])` because default values are evaluated once when defined. Use `lst=None` and initialize inside the function body.",
        "reference_url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"
    },
    {
        "resource_id": "RES_PY_04",
        "subject": "Python",
        "topic": "Object-Oriented Python",
        "prerequisites": ["Functions & Scope"],
        "title": "Python OOP: MRO, Magic Methods & Memory Optimization",
        "description": "Master multiple inheritance with C3 linearization, dunder methods (__str__, __repr__, __eq__), and __slots__.",
        "learning_objectives": [
            "Inspect class Method Resolution Order using Class.mro()",
            "Optimize high-volume object memory with __slots__",
            "Design robust abstract base classes with abc.ABCMeta"
        ],
        "estimated_minutes": 45,
        "difficulty": "Advanced",
        "resource_type": "Concept Guide",
        "summary_content": "Python uses the C3 Linearization algorithm to safely resolve method calls in multiple inheritance hierarchies without ambiguous diamond problems. Defining `__slots__` prevents per-instance dictionary creation, reducing memory footprint by up to 40%.",
        "reference_url": "https://docs.python.org/3/tutorial/classes.html"
    },

    # Java Resources
    {
        "resource_id": "RES_JAVA_01",
        "subject": "Java",
        "topic": "Java Syntax & Basics",
        "prerequisites": [],
        "title": "Java Fundamentals: Types, Variables & Memory",
        "description": "Essential Java foundational concepts including primitive types, reference types, stack vs heap allocation, and JVM execution.",
        "learning_objectives": [
            "Differentiate primitive types from wrapper classes",
            "Understand JVM bytecodes and garbage collection fundamentals",
            "Master variable scope, access modifiers, and type casting"
        ],
        "estimated_minutes": 25,
        "difficulty": "Beginner",
        "resource_type": "Concept Guide",
        "summary_content": "Java is statically typed. Primitive types (byte, short, int, long, float, double, char, boolean) store values directly on the stack or in objects, while references store pointers to heap-allocated objects.",
        "reference_url": "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html"
    },
    {
        "resource_id": "RES_JAVA_02",
        "subject": "Java",
        "topic": "OOP Concepts in Java",
        "prerequisites": ["Java Syntax & Basics"],
        "title": "Polymorphism, Inheritance & Interface Design",
        "description": "Master dynamic method dispatch, method overloading vs overriding, abstract classes, and default interface methods.",
        "learning_objectives": [
            "Implement runtime polymorphism via method overriding",
            "Design clean interfaces following SOLID principles",
            "Use final and sealed keywords to restrict class extension"
        ],
        "estimated_minutes": 35,
        "difficulty": "Intermediate",
        "resource_type": "Interactive Tutorial",
        "summary_content": "Java polymorphism allows parent references to invoke overridden methods in subclasses via virtual method tables (vtable). Use `@Override` annotations to let the compiler catch method signature mismatches.",
        "reference_url": "https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html"
    },
    {
        "resource_id": "RES_JAVA_03",
        "subject": "Java",
        "topic": "Collections Framework",
        "prerequisites": ["OOP Concepts in Java"],
        "title": "Deep Dive: Java Collections Framework Internals",
        "description": "Explore internal mechanics of ArrayList, LinkedList, HashMap bucketing, and TreeSet Red-Black tree balancing.",
        "learning_objectives": [
            "Understand HashMap hashing, collisions, and treeification",
            "Choose optimal collections for read vs write workloads",
            "Implement custom Comparators and Comparable interfaces"
        ],
        "estimated_minutes": 40,
        "difficulty": "Intermediate",
        "resource_type": "Code Walkthrough",
        "summary_content": "Java's HashMap uses an array of linked nodes that converts to Red-Black trees (TREEIFY_THRESHOLD = 8) when hash collisions accumulate in a single bucket, ensuring O(log n) worst-case lookups.",
        "reference_url": "https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html"
    },
    {
        "resource_id": "RES_JAVA_04",
        "subject": "Java",
        "topic": "Multithreading & Concurrency",
        "prerequisites": ["Collections Framework"],
        "title": "Java Concurrency: Volatile, CAS & ConcurrentHashMap",
        "description": "Advanced multi-threading patterns, Java Memory Model (JMM), thread safety, and lock-free concurrency.",
        "learning_objectives": [
            "Understand happens-before relationships and memory visibility",
            "Differentiate volatile from synchronized and atomic locks",
            "Apply concurrent collections like ConcurrentHashMap and BlockingQueue"
        ],
        "estimated_minutes": 50,
        "difficulty": "Advanced",
        "resource_type": "Concept Guide",
        "summary_content": "The `volatile` keyword guarantees memory visibility across threads by bypassing local CPU caches, but does not provide atomicity for operations like `count++`. For atomic thread-safe mutations, utilize `AtomicInteger` or explicit locks.",
        "reference_url": "https://docs.oracle.com/javase/tutorial/essential/concurrency/"
    },

    # Data Structures Resources
    {
        "resource_id": "RES_DS_01",
        "subject": "Data Structures",
        "topic": "Arrays & Strings",
        "prerequisites": [],
        "title": "Array Architecture, Memory Locality & Sliding Window",
        "description": "Foundations of linear contiguous data storage, cache locality benefits, two-pointer techniques, and sliding window paradigms.",
        "learning_objectives": [
            "Analyze cache performance differences between arrays and node lists",
            "Implement two-pointer and sliding window algorithms",
            "Calculate amortized O(1) dynamic array resizing costs"
        ],
        "estimated_minutes": 30,
        "difficulty": "Beginner",
        "resource_type": "Concept Guide",
        "summary_content": "Arrays provide O(1) random memory access due to continuous physical allocation. Dynamic arrays double capacity when full, achieving amortized O(1) append complexity despite occasional O(n) reallocations.",
        "reference_url": "https://en.wikipedia.org/wiki/Array_data_structure"
    },
    {
        "resource_id": "RES_DS_02",
        "subject": "Data Structures",
        "topic": "Stacks & Queues",
        "prerequisites": ["Arrays & Strings"],
        "title": "LIFO & FIFO Applications: Monotonic Stacks & Circular Queues",
        "description": "Practical implementations of stacks and queues, expression evaluation, parenthesis validation, and breadth-first search queues.",
        "learning_objectives": [
            "Implement circular queue buffers with modular indexing",
            "Solve next-greater-element challenges using monotonic stacks",
            "Simulate recursion using explicit stack state frames"
        ],
        "estimated_minutes": 35,
        "difficulty": "Intermediate",
        "resource_type": "Interactive Tutorial",
        "summary_content": "Stacks enforce LIFO ordering, ideal for parsing syntax and backtracking. Queues enforce FIFO ordering, powering breadth-first search traversals and asynchronous task queues.",
        "reference_url": "https://en.wikipedia.org/wiki/Stack_(abstract_data_type)"
    },
    {
        "resource_id": "RES_DS_03",
        "subject": "Data Structures",
        "topic": "Trees & Binary Search Trees",
        "prerequisites": ["Stacks & Queues"],
        "title": "Binary Trees, BSTs & Self-Balancing Trees (AVL / Red-Black)",
        "description": "Tree traversals (inorder, preorder, postorder, level order), BST invariants, and self-balancing tree rotations.",
        "learning_objectives": [
            "Perform tree traversals recursively and iteratively",
            "Identify when an un-balanced BST degrades to O(n) linear performance",
            "Understand left and right AVL tree rotations"
        ],
        "estimated_minutes": 45,
        "difficulty": "Intermediate",
        "resource_type": "Code Walkthrough",
        "summary_content": "A BST maintains the invariant that left children are strictly less and right children are strictly greater. In balanced trees like AVL and Red-Black trees, height is maintained at O(log n), preventing linear degradation.",
        "reference_url": "https://en.wikipedia.org/wiki/Binary_search_tree"
    },
    {
        "resource_id": "RES_DS_04",
        "subject": "Data Structures",
        "topic": "Graphs & Graph Algorithms",
        "prerequisites": ["Trees & Binary Search Trees"],
        "title": "Graph Algorithms: Shortest Paths & Minimum Spanning Trees",
        "description": "Adjacency matrix vs list, BFS/DFS, Dijkstra's algorithm, Bellman-Ford, Floyd-Warshall, and Prim/Kruskal MSTs.",
        "learning_objectives": [
            "Implement Dijkstra's shortest path with priority queues in O((V + E) log V)",
            "Detect negative cycles using Bellman-Ford algorithm",
            "Compute all-pairs shortest paths using Floyd-Warshall dynamic programming"
        ],
        "estimated_minutes": 50,
        "difficulty": "Advanced",
        "resource_type": "Concept Guide",
        "summary_content": "Graphs represent arbitrary relationships. BFS traverses layer-by-layer to discover unweighted shortest paths. Dijkstra solves single-source shortest paths for non-negative weights using priority queues.",
        "reference_url": "https://en.wikipedia.org/wiki/Graph_(abstract_data_type)"
    },

    # SQL Resources
    {
        "resource_id": "RES_SQL_01",
        "subject": "SQL",
        "topic": "SELECT & Basic Filtering",
        "prerequisites": [],
        "title": "Relational Querying: SELECT, WHERE, LIKE & Logical Operators",
        "description": "Master SQL querying, handling NULL values with IS NULL, pattern matching with LIKE, and logical precedence.",
        "learning_objectives": [
            "Write clean SELECT statements with column aliases",
            "Apply three-valued logic (TRUE, FALSE, UNKNOWN) with NULLs",
            "Utilize IN, BETWEEN, and LIKE pattern matching"
        ],
        "estimated_minutes": 20,
        "difficulty": "Beginner",
        "resource_type": "Interactive Tutorial",
        "summary_content": "SQL is a declarative domain-specific language. In SQL, expressions with NULL evaluate to UNKNOWN under three-valued logic, which is why explicit `IS NULL` checks are mandatory.",
        "reference_url": "https://www.w3schools.com/sql/sql_select.asp"
    },
    {
        "resource_id": "RES_SQL_02",
        "subject": "SQL",
        "topic": "Joins & Set Operations",
        "prerequisites": ["SELECT & Basic Filtering"],
        "title": "Visualizing Joins: INNER, LEFT, RIGHT, FULL & CROSS Joins",
        "description": "Comprehensive visual guide to joining relational tables, understanding Cartesian products, and preserving unmatched rows.",
        "learning_objectives": [
            "Distinguish between INNER JOIN and various OUTER JOIN variants",
            "Prevent unintentional cartesian explosion with proper ON clauses",
            "Combine queries using UNION, UNION ALL, and INTERSECT"
        ],
        "estimated_minutes": 35,
        "difficulty": "Intermediate",
        "resource_type": "Concept Guide",
        "summary_content": "Joins merge data across related tables based on common keys. INNER JOIN returns only records with matches in both tables. LEFT JOIN retains all rows from the left table, padding missing right attributes with NULL.",
        "reference_url": "https://www.w3schools.com/sql/sql_join.asp"
    },
    {
        "resource_id": "RES_SQL_03",
        "subject": "SQL",
        "topic": "Aggregations & GROUP BY",
        "prerequisites": ["Joins & Set Operations"],
        "title": "Aggregations, GROUP BY & The HAVING Filter",
        "description": "Understand query execution phase order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY.",
        "learning_objectives": [
            "Perform aggregate calculations with COUNT, SUM, AVG, MIN, MAX",
            "Filter grouped aggregations using HAVING instead of WHERE",
            "Apply multi-column GROUP BY rollups"
        ],
        "estimated_minutes": 30,
        "difficulty": "Intermediate",
        "resource_type": "Code Walkthrough",
        "summary_content": "Understanding the logical execution order of SQL queries explains why WHERE cannot filter aggregate outputs: WHERE executes before GROUP BY, whereas HAVING executes after grouping has completed.",
        "reference_url": "https://www.w3schools.com/sql/sql_groupby.asp"
    },
    {
        "resource_id": "RES_SQL_04",
        "subject": "SQL",
        "topic": "Indexing & Query Optimization",
        "prerequisites": ["Aggregations & GROUP BY"],
        "title": "Database Indexing, B-Trees & Query Execution Plans",
        "description": "Discover how database query optimizers work, examine EXPLAIN output, evaluate B-Tree vs Hash indexes, and design covering indexes.",
        "learning_objectives": [
            "Interpret database EXPLAIN and EXPLAIN ANALYZE execution trees",
            "Design composite and covering indexes for zero-heap lookups",
            "Understand transaction isolation levels and ACID guarantees"
        ],
        "estimated_minutes": 45,
        "difficulty": "Advanced",
        "resource_type": "Concept Guide",
        "summary_content": "Relational indexes are typically organized as balanced B-Trees. A covering index contains all attributes necessary for the query, allowing the database to fulfill the query purely from index leaves without touching physical table pages.",
        "reference_url": "https://use-the-index-luke.com/"
    },

    # Machine Learning Resources
    {
        "resource_id": "RES_ML_01",
        "subject": "Machine Learning",
        "topic": "Supervised Learning",
        "prerequisites": [],
        "title": "Foundations of Supervised Learning: Regression vs Classification",
        "description": "Core concepts in machine learning workflows, hypothesis functions, loss formulation, and gradient descent optimization.",
        "learning_objectives": [
            "Distinguish continuous regression tasks from discrete classification",
            "Formulate Mean Squared Error (MSE) and Cross-Entropy loss functions",
            "Understand training, validation, and test split protocols"
        ],
        "estimated_minutes": 25,
        "difficulty": "Beginner",
        "resource_type": "Concept Guide",
        "summary_content": "Supervised learning maps input features X to labeled targets Y. When Y is continuous, it is a regression problem; when Y is categorical, it is a classification problem. Models minimize an empirical loss function via optimization algorithms.",
        "reference_url": "https://scikit-learn.org/stable/supervised_learning.html"
    },
    {
        "resource_id": "RES_ML_02",
        "subject": "Machine Learning",
        "topic": "Model Evaluation & Metrics",
        "prerequisites": ["Supervised Learning"],
        "title": "Evaluating ML Models: MAE, RMSE, R-squared & Confusion Matrices",
        "description": "Statistical evaluation of predictive performance, interpretation of R^2, Precision, Recall, F1-score, and ROC-AUC curves.",
        "learning_objectives": [
            "Compute and interpret Mean Absolute Error (MAE) and R-squared (R^2)",
            "Diagnose precision-recall trade-offs in imbalanced datasets",
            "Apply K-Fold cross-validation for robust performance estimation"
        ],
        "estimated_minutes": 35,
        "difficulty": "Intermediate",
        "resource_type": "Interactive Tutorial",
        "summary_content": "MAE provides intuitive error measurement in original units, whereas RMSE penalizes large outlier errors quadratically. R-squared indicates the proportion of target variance explained by the input features relative to a naive mean baseline.",
        "reference_url": "https://scikit-learn.org/stable/modules/model_evaluation.html"
    },
    {
        "resource_id": "RES_ML_03",
        "subject": "Machine Learning",
        "topic": "Preprocessing & Feature Engineering",
        "prerequisites": ["Supervised Learning"],
        "title": "Feature Engineering & Data Pipelines with Scikit-learn",
        "description": "Handling missing data, one-hot encoding, feature normalization (StandardScaler), polynomial expansion, and Scikit-learn Pipelines.",
        "learning_objectives": [
            "Prevent data leakage by fitting transformers strictly on training sets",
            "Construct unified scikit-learn Pipeline and ColumnTransformer workflows",
            "Scale continuous features for gradient- and distance-based estimators"
        ],
        "estimated_minutes": 40,
        "difficulty": "Intermediate",
        "resource_type": "Code Walkthrough",
        "summary_content": "Data leakage occurs when test data inadvertently informs training transformations. Using Scikit-Learn `Pipeline` ensures scalers and encoders are fitted solely on training splits, preserving genuine out-of-sample evaluation.",
        "reference_url": "https://scikit-learn.org/stable/modules/preprocessing.html"
    },
    {
        "resource_id": "RES_ML_04",
        "subject": "Machine Learning",
        "topic": "Overfitting & Regularization",
        "prerequisites": ["Model Evaluation & Metrics"],
        "title": "Bias-Variance Tradeoff & Regularization (Lasso, Ridge, ElasticNet)",
        "description": "Understanding overfitting, mathematical formulations of L1 and L2 weight penalties, and hyperparameter tuning.",
        "learning_objectives": [
            "Diagnose high bias (underfitting) vs high variance (overfitting)",
            "Compare geometric contours of L1 (diamond) vs L2 (circular) constraints",
            "Tune regularization strength alpha using GridSearchCV"
        ],
        "estimated_minutes": 45,
        "difficulty": "Advanced",
        "resource_type": "Concept Guide",
        "summary_content": "Regularization combats overfitting by adding a penalty term proportional to weight magnitudes into the loss function. Ridge (L2) prevents coefficients from growing excessively large, while Lasso (L1) can force redundant coefficients to zero.",
        "reference_url": "https://scikit-learn.org/stable/modules/linear_model.html"
    }
]

def generate_student_performance_dataset(num_samples: int = 500) -> pd.DataFrame:
    """
    Generate a realistic synthetic academic dataset for ML regression training.
    Fields:
      - student_id: identifier
      - previous_score: float (0 - 100)
      - quiz_accuracy: float (0 - 100)
      - attempts_count: int (1 - 25)
      - completion_rate: float (0 - 100)
      - study_hours: float (1 - 35)
      - future_score: float (0 - 100, target)
    """
    np.random.seed(42)
    random.seed(42)

    student_ids = [f"STD_{i+1:04d}" for i in range(num_samples)]
    
    # Generate realistic base performance capabilities
    base_ability = np.random.normal(loc=65, scale=15, size=num_samples)
    base_ability = np.clip(base_ability, 30, 95)

    study_hours = np.random.gamma(shape=3.5, scale=3.0, size=num_samples)
    study_hours = np.clip(study_hours, 1.0, 35.0)

    attempts_count = np.random.poisson(lam=7, size=num_samples) + 1
    attempts_count = np.clip(attempts_count, 1, 25)

    completion_rate = base_ability * 0.7 + (study_hours / 35.0) * 25.0 + np.random.normal(0, 8, num_samples)
    completion_rate = np.clip(completion_rate, 5.0, 100.0)

    quiz_accuracy = base_ability * 0.8 + (study_hours / 35.0) * 15.0 + np.random.normal(0, 6, num_samples)
    quiz_accuracy = np.clip(quiz_accuracy, 25.0, 100.0)

    previous_score = quiz_accuracy * 0.85 + (completion_rate * 0.1) + np.random.normal(0, 5, num_samples)
    previous_score = np.clip(previous_score, 20.0, 100.0)

    # Future score: realistic regression relationship with slight non-linear contribution & realistic noise
    # Weightings:
    # 35% quiz accuracy, 25% previous score, 18% study hours, 12% completion rate, 10% attempts effect
    study_hours_effect = (study_hours / 35.0) * 100.0
    attempts_effect = np.minimum(attempts_count * 4.0, 100.0)
    
    future_score = (
        0.35 * quiz_accuracy +
        0.25 * previous_score +
        0.18 * study_hours_effect +
        0.12 * completion_rate +
        0.10 * attempts_effect +
        np.random.normal(loc=0, scale=3.5, size=num_samples)
    )
    future_score = np.clip(future_score, 0.0, 100.0)

    df = pd.DataFrame({
        "student_id": student_ids,
        "previous_score": np.round(previous_score, 2),
        "quiz_accuracy": np.round(quiz_accuracy, 2),
        "attempts_count": attempts_count,
        "completion_rate": np.round(completion_rate, 2),
        "study_hours": np.round(study_hours, 2),
        "future_score": np.round(future_score, 2)
    })
    return df

def seed_all():
    print("=== SkillAdapt Seed Data Generator ===")

    # 1. Save Questions
    questions_path = os.path.join(DATA_DIR, "questions.json")
    with open(questions_path, "w", encoding="utf-8") as f:
        json.dump(QUESTIONS, f, indent=2)
    print(f"[OK] Saved {len(QUESTIONS)} questions to {questions_path}")

    # 2. Save Learning Resources
    resources_path = os.path.join(DATA_DIR, "learning_resources.json")
    with open(resources_path, "w", encoding="utf-8") as f:
        json.dump(LEARNING_RESOURCES, f, indent=2)
    print(f"[OK] Saved {len(LEARNING_RESOURCES)} learning resources to {resources_path}")

    # 3. Generate & Save Synthetic ML Dataset
    csv_path = os.path.join(DATA_DIR, "student_performance.csv")
    df = generate_student_performance_dataset(500)
    df.to_csv(csv_path, index=False)
    print(f"[OK] Generated {len(df)} synthetic student performance records to {csv_path}")

    # 4. Create Demo User and seed user accounts
    demo_user = {
        "id": "std_demo_01",
        "username": "demo_student",
        "email": "demo.student@skilladapt.edu",
        "full_name": "Alex Morgan",
        "password_hash": hash_password("Student@123"),
        "learning_level": "Intermediate",
        "completed_resources": ["RES_PY_01", "RES_DS_01", "RES_SQL_01"],
        "created_at": (datetime.now() - timedelta(days=14)).isoformat()
    }

    users_path = os.path.join(DATA_DIR, "users.json")
    # Only create or update demo user
    users = [demo_user]
    with open(users_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    print(f"[OK] Initialized demo user 'demo_student' (pass: Student@123) in {users_path}")

    # 5. Create Seed Quiz Attempts for demo student
    # Providing 6 realistic attempts across Python, Java, Data Structures, SQL, ML
    now = datetime.now()
    demo_attempts = [
        {
            "attempt_id": "att_001",
            "user_id": "std_demo_01",
            "subject": "Python",
            "topic": "Python Basics & Syntax",
            "total_questions": 5,
            "correct_answers": 4,
            "score": 7,
            "max_score": 8,
            "percentage": 87.5,
            "difficulty_breakdown": {"Easy": 3, "Medium": 2, "Hard": 0},
            "adaptive_path": ["Easy", "Easy", "Medium", "Medium", "Hard"],
            "responses": [
                {"question_id": "PY_001", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Python Basics & Syntax"},
                {"question_id": "PY_002", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Python Basics & Syntax"},
                {"question_id": "PY_003", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Control Flow & Loops"},
                {"question_id": "PY_004", "is_correct": True, "marks": 2, "difficulty": "Medium", "topic": "Functions & Scope"},
                {"question_id": "PY_006", "is_correct": False, "marks": 0, "difficulty": "Hard", "topic": "Object-Oriented Python"}
            ],
            "started_at": (now - timedelta(days=10)).isoformat(),
            "completed_at": (now - timedelta(days=10, minutes=-12)).isoformat()
        },
        {
            "attempt_id": "att_002",
            "user_id": "std_demo_01",
            "subject": "Data Structures",
            "topic": "Arrays & Strings",
            "total_questions": 5,
            "correct_answers": 4,
            "score": 6,
            "max_score": 7,
            "percentage": 85.7,
            "difficulty_breakdown": {"Easy": 3, "Medium": 2, "Hard": 0},
            "adaptive_path": ["Easy", "Easy", "Medium", "Medium", "Hard"],
            "responses": [
                {"question_id": "DS_001", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Arrays & Strings"},
                {"question_id": "DS_002", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Stacks & Queues"},
                {"question_id": "DS_003", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Linked Lists"},
                {"question_id": "DS_004", "is_correct": True, "marks": 2, "difficulty": "Medium", "topic": "Trees & Binary Search Trees"},
                {"question_id": "DS_006", "is_correct": False, "marks": 0, "difficulty": "Hard", "topic": "Graphs & Graph Algorithms"}
            ],
            "started_at": (now - timedelta(days=7)).isoformat(),
            "completed_at": (now - timedelta(days=7, minutes=-14)).isoformat()
        },
        {
            "attempt_id": "att_003",
            "user_id": "std_demo_01",
            "subject": "SQL",
            "topic": "SELECT & Basic Filtering",
            "total_questions": 5,
            "correct_answers": 5,
            "score": 8,
            "max_score": 8,
            "percentage": 100.0,
            "difficulty_breakdown": {"Easy": 3, "Medium": 1, "Hard": 1},
            "adaptive_path": ["Easy", "Easy", "Medium", "Hard", "Hard"],
            "responses": [
                {"question_id": "SQL_001", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "SELECT & Basic Filtering"},
                {"question_id": "SQL_002", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "SELECT & Basic Filtering"},
                {"question_id": "SQL_003", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Joins & Set Operations"},
                {"question_id": "SQL_004", "is_correct": True, "marks": 2, "difficulty": "Medium", "topic": "Aggregations & GROUP BY"},
                {"question_id": "SQL_006", "is_correct": True, "marks": 3, "difficulty": "Hard", "topic": "Indexing & Query Optimization"}
            ],
            "started_at": (now - timedelta(days=5)).isoformat(),
            "completed_at": (now - timedelta(days=5, minutes=-10)).isoformat()
        },
        {
            "attempt_id": "att_004",
            "user_id": "std_demo_01",
            "subject": "Java",
            "topic": "Java Syntax & Basics",
            "total_questions": 5,
            "correct_answers": 3,
            "score": 4,
            "max_score": 7,
            "percentage": 57.1,
            "difficulty_breakdown": {"Easy": 3, "Medium": 2, "Hard": 0},
            "adaptive_path": ["Easy", "Easy", "Medium", "Medium", "Easy"],
            "responses": [
                {"question_id": "JAVA_001", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Java Syntax & Basics"},
                {"question_id": "JAVA_002", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Java Syntax & Basics"},
                {"question_id": "JAVA_003", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "OOP Concepts in Java"},
                {"question_id": "JAVA_004", "is_correct": False, "marks": 0, "difficulty": "Medium", "topic": "OOP Concepts in Java"},
                {"question_id": "JAVA_005", "is_correct": False, "marks": 0, "difficulty": "Medium", "topic": "Collections Framework"}
            ],
            "started_at": (now - timedelta(days=3)).isoformat(),
            "completed_at": (now - timedelta(days=3, minutes=-11)).isoformat()
        },
        {
            "attempt_id": "att_005",
            "user_id": "std_demo_01",
            "subject": "Machine Learning",
            "topic": "Supervised Learning",
            "total_questions": 5,
            "correct_answers": 2,
            "score": 2,
            "max_score": 7,
            "percentage": 28.6,
            "difficulty_breakdown": {"Easy": 3, "Medium": 1, "Hard": 1},
            "adaptive_path": ["Easy", "Easy", "Medium", "Easy", "Easy"],
            "responses": [
                {"question_id": "ML_001", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Supervised Learning"},
                {"question_id": "ML_002", "is_correct": True, "marks": 1, "difficulty": "Easy", "topic": "Supervised Learning"},
                {"question_id": "ML_004", "is_correct": False, "marks": 0, "difficulty": "Medium", "topic": "Model Evaluation & Metrics"},
                {"question_id": "ML_005", "is_correct": False, "marks": 0, "difficulty": "Medium", "topic": "Preprocessing & Feature Engineering"},
                {"question_id": "ML_006", "is_correct": False, "marks": 0, "difficulty": "Hard", "topic": "Overfitting & Regularization"}
            ],
            "started_at": (now - timedelta(days=1)).isoformat(),
            "completed_at": (now - timedelta(days=1, minutes=-15)).isoformat()
        }
    ]

    attempts_path = os.path.join(DATA_DIR, "quiz_attempts.json")
    with open(attempts_path, "w", encoding="utf-8") as f:
        json.dump(demo_attempts, f, indent=2)
    print(f"[OK] Seeded {len(demo_attempts)} quiz attempts to {attempts_path}")
    print("=== All Seed Data Generated Successfully! ===")

if __name__ == "__main__":
    seed_all()
