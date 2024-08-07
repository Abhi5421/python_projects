from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import settings
from database.connection import get_db, Base
from main import app
import pytest
from fastapi.testclient import TestClient

DATABASE_URL = settings.mysql_test_url
print("Database URL used for tests:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    print("Using test database session")
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_db():
    print("before over_ride")
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
    print("Teardown complete")




