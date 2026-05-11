from datetime import datetime
from collections import deque

# ============================================================
# NODE DEFINITIONS
# ============================================================

class NoteNode:
    """Node untuk Doubly Linked List (chronological & alphabetical)"""
    def __init__(self, note_id, title, content):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.tags = []          # list of tag names
        self.created_at = datetime.now()
        self.synced = False

        # Doubly linked list pointers
        self.prev_chron = None  # chronological
        self.next_chron = None
        self.prev_alpha = None  # alphabetical
        self.next_alpha = None

    def __repr__(self):
        return f"Note({self.note_id}, '{self.title}', tags={self.tags})"


class TagNode:
    """Node untuk Multi-linked list per tag"""
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.notes = []         # list of NoteNode yang punya tag ini

    def __repr__(self):
        return f"Tag('{self.tag_name}', notes={[n.note_id for n in self.notes]})"


# ============================================================
# NOTE-TAKING APP DATA STRUCTURE
# ============================================================

class NoteTakingApp:
    def __init__(self, sync_buffer_size=5):
        self.notes = {}          # note_id -> NoteNode
        self.tags = {}           # tag_name -> TagNode

        # Doubly linked list: chronological order
        self.chron_head = None
        self.chron_tail = None

        # Doubly linked list: alphabetical order
        self.alpha_head = None
        self.alpha_tail = None

        # Circular buffer untuk sync status tracking
        self.sync_buffer = deque(maxlen=sync_buffer_size)
        self._id_counter = 1

    # ----------------------------------------------------------
    # ADD NOTE
    # ----------------------------------------------------------
    def add_note(self, title, content, tags=[]):
        note_id = f"N{self._id_counter:03d}"
        self._id_counter += 1

        node = NoteNode(note_id, title, content)

        # Simpan ke dict
        self.notes[note_id] = node

        # Tambahkan ke chronological DLL (append di tail)
        self._insert_chron(node)

        # Tambahkan ke alphabetical DLL (sorted insert)
        self._insert_alpha(node)

        # Hubungkan dengan tags (multi-linked)
        for tag in tags:
            self._link_tag(node, tag)

        # Catat ke circular buffer sebagai "unsynced change"
        self.sync_buffer.append({
            "note_id": note_id,
            "action": "ADD",
            "timestamp": node.created_at,
            "synced": False
        })

        print(f"[+] Note ditambahkan: {node}")
        return node

    # ----------------------------------------------------------
    # DOUBLY LINKED LIST - CHRONOLOGICAL
    # ----------------------------------------------------------
    def _insert_chron(self, node):
        """Append di akhir (newest last)"""
        if self.chron_tail is None:
            self.chron_head = self.chron_tail = node
        else:
            self.chron_tail.next_chron = node
            node.prev_chron = self.chron_tail
            self.chron_tail = node

    # ----------------------------------------------------------
    # DOUBLY LINKED LIST - ALPHABETICAL
    # ----------------------------------------------------------
    def _insert_alpha(self, node):
        """Insert di posisi alphabetical yang benar"""
        if self.alpha_head is None:
            self.alpha_head = self.alpha_tail = node
            return

        current = self.alpha_head
        while current and current.title.lower() < node.title.lower():
            current = current.next_alpha

        if current is None:
            # Insert di akhir
            self.alpha_tail.next_alpha = node
            node.prev_alpha = self.alpha_tail
            self.alpha_tail = node
        elif current.prev_alpha is None:
            # Insert di awal
            node.next_alpha = self.alpha_head
            self.alpha_head.prev_alpha = node
            self.alpha_head = node
        else:
            # Insert di tengah
            prev = current.prev_alpha
            prev.next_alpha = node
            node.prev_alpha = prev
            node.next_alpha = current
            current.prev_alpha = node

    # ----------------------------------------------------------
    # MULTI-LINKED BY TAG
    # ----------------------------------------------------------
    def _link_tag(self, node, tag_name):
        if tag_name not in self.tags:
            self.tags[tag_name] = TagNode(tag_name)
        self.tags[tag_name].notes.append(node)
        node.tags.append(tag_name)

    def get_notes_by_tag(self, tag_name):
        if tag_name not in self.tags:
            print(f"Tag '{tag_name}' tidak ditemukan.")
            return []
        return self.tags[tag_name].notes

    # ----------------------------------------------------------
    # VIEW: CHRONOLOGICAL
    # ----------------------------------------------------------
    def view_chronological(self):
        print("\n=== Chronological View ===")
        current = self.chron_head
        while current:
            print(f"  [{current.created_at.strftime('%H:%M:%S')}] {current.title} | tags: {current.tags}")
            current = current.next_chron

    # ----------------------------------------------------------
    # VIEW: ALPHABETICAL
    # ----------------------------------------------------------
    def view_alphabetical(self):
        print("\n=== Alphabetical View ===")
        current = self.alpha_head
        while current:
            print(f"  {current.title} | tags: {current.tags}")
            current = current.next_alpha

    # ----------------------------------------------------------
    # SYNC STATUS TRACKING (Circular Buffer)
    # ----------------------------------------------------------
    def mark_synced(self, note_id):
        for entry in self.sync_buffer:
            if entry["note_id"] == note_id:
                entry["synced"] = True
                if note_id in self.notes:
                    self.notes[note_id].synced = True
                print(f"[✓] Note {note_id} ditandai synced.")
                return
        print(f"Note {note_id} tidak ada di sync buffer.")

    def view_sync_status(self):
        print("\n=== Sync Buffer (Recent Changes) ===")
        if not self.sync_buffer:
            print("  Buffer kosong.")
        for entry in self.sync_buffer:
            status = "✓ Synced" if entry["synced"] else "✗ Pending"
            print(f"  {entry['note_id']} | {entry['action']} | {status}")


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    app = NoteTakingApp(sync_buffer_size=5)

    # Tambah beberapa note
    app.add_note("Belajar Python",   "List, dict, OOP...",      tags=["python", "belajar"])
    app.add_note("Algoritma Sort",   "Bubble, merge, quick...", tags=["algo", "belajar"])
    app.add_note("Database Dasar",   "SQL, relational...",      tags=["db", "belajar"])
    app.add_note("Flask Web App",    "Routing, template...",    tags=["python", "web"])
    app.add_note("API REST Design",  "GET, POST, status code.", tags=["web", "algo"])

    # View chronological
    app.view_chronological()

    # View alphabetical
    app.view_alphabetical()

    # Multi-linked: cari notes by tag
    print("\n=== Notes dengan tag 'python' ===")
    for n in app.get_notes_by_tag("python"):
        print(f"  {n}")

    print("\n=== Notes dengan tag 'belajar' ===")
    for n in app.get_notes_by_tag("belajar"):
        print(f"  {n}")

    # Sync tracking
    app.view_sync_status()
    app.mark_synced("N001")
    app.mark_synced("N003")
    app.view_sync_status()