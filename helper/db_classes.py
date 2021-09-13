from datetime import datetime, timedelta, date

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.orm import aliased, sessionmaker, declarative_base, relationship
from sqlalchemy.sql.sqltypes import DateTime, Date


Base = declarative_base()
_CONNECTION = 'sqlite:///hw901.db'


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    address = Column(String)
    email = Column(String)
    tags = Column(String)

    phones = relationship("Phone", back_populates='record',
                          cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Record(name='%s', birthday='%s', address='%s', email='%s', tags='%s')>" % (self.name, self.birthday, self.address, self.email, self.tags)


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    phone_value = Column(String, nullable=False)
    record_id = Column(Integer, ForeignKey('records.id'))

    record = relationship("Record", back_populates="phones")

    def __repr__(self):
        return "<Phone(phone_value='%s')>" % self.phone_value


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note_tags = Column(String)
    note_text = Column(String)

    def add_note(self, session, text, hashtag):
        # добавляет заметку в таблицу Notes
        session.add(Note(note_tags=hashtag, note_text=text))
        session.commit()

    def delete_note(self, session, hashtag):
        # удаляет заметку из таблицы Notes, которая имеет note_tags=hashtag
        note_for_deleting = session.query(
            Note).filter_by(note_tags=hashtag).first()
        session.delete(note_for_deleting)
        session.commit()

    def edit_note(self, session, hashtag, new_text):
        # редактирует заметку из таблицы Notes, которая имеет note_tags=hashtag
        note_for_editing = session.query(
            Note).filter_by(note_tags=hashtag).one()
        note_for_editing.note_text = new_text
        print(session.dirty)
        print(note_for_editing)
        session.commit()

    def find_note(self, session, keyword):
        # находит все заметки  из таблицы Notes, в тэгах которых содержится keyword
        # возвращает note_list - список экземляра класса Note

        note_list = session.query(Note).filter_by(note_tags=keyword).all()
        return note_list

    def print_notes(self, session, note_list):
        # где note_list - список экземляра класса Note

        result = ""

        # Печать шапки с названием столбцов
        result += f" {72*'_'} \n"
        result += '|             TAGS             |                NOTE                     |\n'
        result += f"|{71*'_'} |\n"
        # Печать заметок
        for note in note_list:
            lines = note.note_text.split('\n')
            counter = 0
            for line in lines:
                if counter == 0:
                    result += f'|{note.note_tags:<30}| {line:<40}|\n'
                else:
                    result += f'|{" ":<30}| {line:<40}|\n'
                counter += 1
            result += f'|{30*"_"}|{41*"_"}|\n'
        print(result)

    def sort_notes(self, session, search_type="1"):
        # выводит список заметков в отсортированном виде
        # "1" - в алфавитном порядке
        # "2" - в обратном алфавитном порядке
        # "3" - от старых заметок к новым
        # "4" - от новых заметок к старым
        # возвращает Note_list

        if search_type == "1":
            note_list = session.query(Note).order_by(
                Note.note_tags.asc()).all()
        elif search_type == "2":
            note_list = session.query(Note).order_by(
                Note.note_tags.desc()).all()
        elif search_type == "3":
            note_list = session.query(Note).order_by(
                Note.id.asc()).all()
        elif search_type == "4":
            note_list = session.query(Note).order_by(
                Note.id.desc()).all()
        return note_list


class Model:
    def __init__(self):
        engine = create_engine('sqlite:///hw901.db', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)


def main():
    m_model = Model()

    # Добавление рекорд - телефон
    # bd = datetime.strptime('08.02.1984', "%d.%m.%Y").date()
    # a_record = Record(name='Anna Khodyka', birthday=bd,
    #                   address='Bucha, Vyshneva str. 84', email='anna.khodyka@bigmir.net', tags='friends')
    # a_record.phones = [Phone(phone_value='+380978440021'),
    #                    Phone(phone_value='+380671113029')]
    # session.add(a_record)
    # session.commit()

    # запросы JOIN
    phone_1 = m_model.session.query(Phone).filter_by(id=1).first()
    print(phone_1)
    print(phone_1.record.name)
    # КНИГА ЗАМЕТОК
    # Добавление заметок
    # Note().add_note(session, "Полить цветы, забрать детей с садика", "Список дел")
    # Note().add_note(session, "Полина\nНикита\nДаниил", "Гости")
    # Удаление заметок
    # Note().delete_note(session, "Тимофей")
    # Note().delete_note(session, "Гости")

    # Редактирование заметок
    # Note().edit_note(session, "Приоритеты", "Python")

    # note_list = session.query(Note).order_by(Note.id)
    # Note().print_notes(session, note_list)

    # Сортировка заметок
    # Note().print_notes(session, Note().find_note(session, "Приоритеты"))
    # Note().print_notes(session, Note().sort_notes(session, search_type="1"))
    # Note().print_notes(session, Note().sort_notes(session, search_type="2"))
    # Note().print_notes(session, Note().sort_notes(session, search_type="3"))
    # Note().print_notes(session, Note().sort_notes(session, search_type="4"))


if __name__ == "__main__":
    main()
