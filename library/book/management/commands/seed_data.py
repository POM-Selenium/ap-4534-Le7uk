from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from book.models import Book
from author.models import Author
from order.models import Order
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample library data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # --- Authors ---
        authors_data = [
            ('Ivan', 'Franko', 'Yakovych'),
            ('Lesia', 'Ukrainka', 'Petrivna'),
            ('Taras', 'Shevchenko', 'Hryhorovych'),
            ('George', 'Orwell', 'Arthur'),
            ('Franz', 'Kafka', 'Zdenek'),
            ('Ernest', 'Hemingway', 'Miller'),
            ('Gabriel', 'Marquez', 'Garcia'),
            ('Albert', 'Camus', 'Louis'),
        ]

        authors = []
        for name, surname, patronymic in authors_data:
            author, created = Author.objects.get_or_create(
                name=name, surname=surname,
                defaults={'patronymic': patronymic}
            )
            authors.append(author)
            if created:
                self.stdout.write(f'  + Author: {name} {surname}')

        # --- Books ---
        books_data = [
            ('Kobzar', 'A landmark collection of poetry by Taras Shevchenko, the father of modern Ukrainian literature.', 8, [authors[2]]),
            ('Zakhar Berkut', 'A historical novel about the heroic defense of a Carpathian village against the Mongol invasion.', 5, [authors[0]]),
            ('Lisova Pisnia', 'A poetic drama about the eternal conflict between nature spirits and human civilization.', 6, [authors[1]]),
            ('Kaminnyi Khrest', 'A collection of stories depicting the hard life of Ukrainian peasants.', 4, [authors[0]]),
            ('1984', 'A dystopian novel set in a totalitarian society under the constant watch of Big Brother.', 5, [authors[3]]),
            ('Animal Farm', 'A satirical allegory of totalitarianism told through a rebellion of farm animals.', 4, [authors[3]]),
            ('The Trial', 'A man is arrested and prosecuted by a mysterious authority for an unspecified crime.', 6, [authors[4]]),
            ('The Metamorphosis', 'Gregor Samsa wakes one morning to find himself transformed into a giant insect.', 7, [authors[4]]),
            ('The Old Man and the Sea', 'An aging Cuban fisherman struggles with a giant marlin far out in the Gulf Stream.', 5, [authors[5]]),
            ('A Farewell to Arms', 'An American ambulance officer falls in love with a British nurse during the First World War.', 3, [authors[5]]),
            ('One Hundred Years of Solitude', 'Seven generations of the Buendia family in the mythical town of Macondo.', 4, [authors[6]]),
            ('Love in the Time of Cholera', 'A story of unrequited love that spans over fifty years in a Caribbean port city.', 2, [authors[6]]),
            ('The Stranger', 'A young man in Algeria kills an Arab and faces trial, exploring themes of absurdism.', 6, [authors[7]]),
            ('The Plague', 'A deadly plague sweeps through the Algerian city of Oran, testing its inhabitants.', 3, [authors[7]]),
            ('Contra Spem Spero', 'A poetry collection full of resilience and hope against all odds.', 0, [authors[1]]),
        ]

        saved_books = []
        for name, description, count, book_authors in books_data:
            book, created = Book.objects.get_or_create(
                name=name,
                defaults={'description': description, 'count': count}
            )
            if created:
                for author in book_authors:
                    book.authors.add(author)
                self.stdout.write(f'  + Book: {name} (count={count})')
            saved_books.append(book)

        # --- Users ---
        if not User.objects.filter(email='librarian@library.com').exists():
            librarian = User.objects.create_user(
                email='librarian@library.com',
                password='librarian123',
                first_name='Anna',
                middle_name='Ivanivna',
                last_name='Kovalenko',
                role=1,
                is_active=True,
            )
            self.stdout.write('  + Librarian: librarian@library.com / librarian123')
        else:
            librarian = User.objects.get(email='librarian@library.com')

        readers_data = [
            ('Mykola', 'Petrovych', 'Sydorenko', 'reader1@mail.com', 'reader123'),
            ('Olena', 'Vasylivna', 'Bondarenko', 'reader2@mail.com', 'reader123'),
            ('Dmytro', 'Oleksiyovych', 'Shevchuk', 'reader3@mail.com', 'reader123'),
        ]

        readers = []
        for first, middle, last, email, pwd in readers_data:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email, password=pwd,
                    first_name=first, middle_name=middle, last_name=last,
                    role=0, is_active=True,
                )
                readers.append(user)
                self.stdout.write(f'  + Reader: {email} / {pwd}')
            else:
                readers.append(User.objects.get(email=email))

        # --- Orders ---
        now = datetime.datetime.now()
        orders_data = [
            (readers[0], saved_books[0], now + datetime.timedelta(weeks=2), None),
            (readers[0], saved_books[4], now + datetime.timedelta(weeks=1), None),
            (readers[1], saved_books[6], now - datetime.timedelta(days=5), now - datetime.timedelta(days=1)),
            (readers[1], saved_books[10], now + datetime.timedelta(weeks=3), None),
            (readers[2], saved_books[8], now - datetime.timedelta(days=10), now - datetime.timedelta(days=3)),
        ]

        for user, book, plated_end_at, end_at in orders_data:
            if not Order.objects.filter(user=user, book=book).exists():
                order = Order(user=user, book=book, plated_end_at=plated_end_at, end_at=end_at)
                order.save()
                status = 'returned' if end_at else 'active'
                self.stdout.write(f'  + Order: {user.first_name} -> {book.name} [{status}]')

        self.stdout.write(self.style.SUCCESS('\nDone! Database seeded successfully.'))
        self.stdout.write('\nTest accounts:')
        self.stdout.write('  Librarian: librarian@library.com / librarian123')
        self.stdout.write('  Reader 1:  reader1@mail.com / reader123')
        self.stdout.write('  Reader 2:  reader2@mail.com / reader123')
        self.stdout.write('  Reader 3:  reader3@mail.com / reader123')