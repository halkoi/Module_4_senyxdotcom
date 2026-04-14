import pytest
from sqlalchemy.orm import Session
from data.data_generator import DataGenerator
from db_models.models import AccountTransactionTemplate

def test_accounts_transaction_not_enough_money(db_session: Session):
    stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=100)
    bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)

    db_session.add_all([stan, bob])
    db_session.commit()

    def transfer_money(session, from_account, to_account, amount):
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()
        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")
        from_account.balance -= amount
        to_account.balance += amount
        session.commit()

    # Проверяем начальные балансы
    assert stan.balance == 100
    assert bob.balance == 500

    try:
        transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)
        pytest.fail("Должна была быть ошибка — денег недостаточно")

    except ValueError as e:
        db_session.rollback()
        db_session.refresh(stan)
        db_session.refresh(bob)

        # Проверяем что балансы не изменились
        assert stan.balance == 100, "Баланс Стена не должен измениться"
        assert bob.balance == 500, "Баланс Боба не должен измениться"

    finally:
        db_session.delete(stan)
        db_session.delete(bob)
        db_session.commit()
