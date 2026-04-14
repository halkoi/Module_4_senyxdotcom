from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
Base = declarative_base()




#Modul_4\Cinescope\db_requester\models.py
# Модель для таблицы accounts_transaction_template
class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)