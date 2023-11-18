#!/usr/bin/env python3

from app import app
from models import db, Member, Book, Loan

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Member.query.delete()
    Book.query.delete()
    Loan.query.delete()

    print("Creating members...")
    karen = Member(name="Karen", year_joined='2019')
    sanjay = Member(name="Sanjay", year_joined='2020')
    kiki = Member(name="Kiki", year_joined='2023')
    members = [karen, sanjay, kiki]

    print("Creating books...")

    b1 = Book(title="Cracking the Coding Interview", author="Gayle Laakmann McDowell", number_of_pages=100)
    b2 = Book(title="Eloquent JavaScript", author="Marijn Haverbeke", number_of_pages=200)
    b3 = Book(title="Think Python: How to Think Like a Computer Scientist", author="Allen B. Downey", number_of_pages=150)
    books = [b1, b2, b3]

    print("Creating Loans...")

    l1 = Loan(member=karen, book=b1)
    l2 = Loan(member=sanjay, book=b2)
    l3 = Loan(member=kiki, book=b3)
    loans = [l1, l2, l3]

    db.session.add_all(members)
    db.session.add_all(books)
    db.session.add_all(loans)
    db.session.commit()

    print("Seeding done!")