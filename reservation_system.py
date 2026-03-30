from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Reservation:
    number_of_days: int
    from_date: str
    to_date: str
    persons: int
    rooms: int

    def to_lines(self) -> list[str]:
        return [
            str(self.number_of_days),
            self.from_date,
            self.to_date,
            str(self.persons),
            str(self.rooms),
        ]

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Reservation":
        cleaned = [line.strip() for line in lines if line is not None]
        if len(cleaned) < 5:
            raise ValueError("Reservation data is incomplete.")
        return cls(
            number_of_days=int(cleaned[0]),
            from_date=cleaned[1],
            to_date=cleaned[2],
            persons=int(cleaned[3]),
            rooms=int(cleaned[4]),
        )


class ReservationValidator:
    @staticmethod
    def validate(
        number_of_days: str,
        from_date_text: str,
        to_date_text: str,
        number_of_persons: str,
        number_of_rooms: str,
    ) -> Reservation:
        if not all(
            value.strip()
            for value in [
                number_of_days,
                from_date_text,
                to_date_text,
                number_of_persons,
                number_of_rooms,
            ]
        ):
            raise ValueError("Please fill all reservation fields.")

        try:
            days = int(number_of_days)
            persons = int(number_of_persons)
            rooms = int(number_of_rooms)
        except ValueError as exc:
            raise ValueError("Days, persons, and rooms must be whole numbers.") from exc

        if days <= 0 or persons <= 0 or rooms <= 0:
            raise ValueError("Days, persons, and rooms must be greater than 0.")

        try:
            from_date = datetime.strptime(from_date_text, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_text, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Please enter dates in YYYY-MM-DD format.") from exc

        if to_date <= from_date:
            raise ValueError("To Date must be after From Date.")

        actual_days = (to_date - from_date).days
        if days != actual_days:
            raise ValueError(
                f"Number of days does not match the dates. For these dates, days should be {actual_days}."
            )

        return Reservation(
            number_of_days=days,
            from_date=from_date_text,
            to_date=to_date_text,
            persons=persons,
            rooms=rooms,
        )


class ReservationRepository:
    def __init__(self, folder: str = "reservations") -> None:
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)

    def _path_for_user(self, user_key: str) -> Path:
        safe_user_key = user_key.strip()
        return self.folder / f"{safe_user_key}_reservation.txt"

    def save(self, user_key: str, reservation: Reservation) -> None:
        path = self._path_for_user(user_key)
        path.write_text("\n".join(reservation.to_lines()) + "\n", encoding="utf-8")

    def load(self, user_key: str) -> Reservation | None:
        path = self._path_for_user(user_key)
        if not path.exists():
            return None

        lines = path.read_text(encoding="utf-8").splitlines()
        try:
            return Reservation.from_lines(lines)
        except (ValueError, TypeError):
            return None

    def delete(self, user_key: str) -> bool:
        path = self._path_for_user(user_key)
        if not path.exists():
            return False
        path.unlink()
        return True


class ReservationService:
    def __init__(self, repository: ReservationRepository | None = None) -> None:
        self.repository = repository or ReservationRepository()

    def make_reservation(
        self,
        user_key: str,
        number_of_days: str,
        from_date_text: str,
        to_date_text: str,
        number_of_persons: str,
        number_of_rooms: str,
    ) -> Reservation:
        reservation = ReservationValidator.validate(
            number_of_days,
            from_date_text,
            to_date_text,
            number_of_persons,
            number_of_rooms,
        )
        self.repository.save(user_key, reservation)
        return reservation

    def view_reservation(self, user_key: str) -> Reservation | None:
        return self.repository.load(user_key)

    def modify_reservation(
        self,
        user_key: str,
        number_of_days: str,
        from_date_text: str,
        to_date_text: str,
        number_of_persons: str,
        number_of_rooms: str,
    ) -> Reservation:
        if self.repository.load(user_key) is None:
            raise FileNotFoundError("No reservation found")

        reservation = ReservationValidator.validate(
            number_of_days,
            from_date_text,
            to_date_text,
            number_of_persons,
            number_of_rooms,
        )
        self.repository.save(user_key, reservation)
        return reservation

    def cancel_reservation(self, user_key: str) -> bool:
        return self.repository.delete(user_key)