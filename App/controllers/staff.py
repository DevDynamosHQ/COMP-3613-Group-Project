from typing import Optional, List

from App.models import Staff
from App.database import db


def create_staff(username: str, user_id: int, password: str) -> Staff:
    """Create and persist a new Staff record.

    Returns the created `Staff` instance.
    """
    staff = Staff(username=username, user_id=user_id)
    staff.password = password
    db.session.add(staff)
    db.session.commit()
    return staff


def get_staff(id: int) -> Optional[Staff]:
    """Return a Staff by primary key or None if not found."""
    return db.session.get(Staff, id)


def get_staff_by_user(user_id: int) -> Optional[Staff]:
    """Return a Staff by `user_id` or None."""
    return db.session.execute(db.select(Staff).filter_by(user_id=user_id)).scalar_one_or_none()


def get_all_staff() -> List[Staff]:
    """Return all Staff records as a list."""
    return db.session.scalars(db.select(Staff)).all()


def get_all_staff_json() -> List[dict]:
    """Return JSON-serializable dicts for all staff records."""
    staff_list = get_all_staff()
    return [s.get_json() for s in staff_list]


def update_staff(id: int, username: Optional[str] = None) -> Optional[Staff]:
    """Update mutable fields on a Staff record.

    Only non-None values are applied. Returns the updated Staff or None.
    """
    staff = get_staff(id)
    if not staff:
        return None

    if username is not None:
        staff.username = username

    db.session.commit()
    return staff


def delete_staff(id: int) -> Optional[bool]:
    """Delete a Staff record.

    Returns True on successful deletion, or None if the record was not found.
    """
    staff = get_staff(id)
    if not staff:
        return None

    db.session.delete(staff)
    db.session.commit()
    return True
