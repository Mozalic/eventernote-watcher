import tempfile
import unittest
from pathlib import Path

from app.calendar import generate_ics
from app.db import Database
from app.fetcher import Event


class CalendarExportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db = Database(Path(self.directory.name) / "test.db")
        self.db.add_actor(1, "Artist A")
        self.db.add_actor(2, "Artist B")

    def event(self, day):
        return Event(42, "Shared concert", day, "Venue", "18:00")

    def test_all_day_event_ends_on_next_date(self):
        for start, end in [
            ("2026-10-27", "20261028"),
            ("2026-10-31", "20261101"),
            ("2024-02-28", "20240229"),
            ("2024-02-29", "20240301"),
            ("2026-12-31", "20270101"),
        ]:
            with self.subTest(start=start):
                self.db.mark_seen(1, [self.event(start)])
                lines = generate_ics(self.db, include_past=True).splitlines()
                self.assertIn("DTSTART;VALUE=DATE:" + start.replace("-", ""), lines)
                self.assertIn("DTEND;VALUE=DATE:" + end, lines)

    def test_shared_event_has_one_entry_and_both_artists(self):
        for actor_id in (1, 2):
            self.db.mark_seen(actor_id, [self.event("2026-10-27")])
        calendar = generate_ics(self.db, include_past=True)
        self.assertEqual(calendar.count("BEGIN:VEVENT"), 1)
        self.assertIn("UID:42@eventernote-watcher\r\n", calendar)
        self.assertIn("Artist A", calendar)
        self.assertIn("Artist B", calendar)
        self.assertIn("DTEND;VALUE=DATE:20261028\r\n", calendar)


if __name__ == "__main__":
    unittest.main()
