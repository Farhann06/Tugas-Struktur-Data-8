# 📝 Note-Taking App — Data Structure Implementation

> Implementasi struktur data untuk aplikasi note-taking menggunakan Python murni, tanpa library eksternal.

---

## 📋 Deskripsi

Proyek ini adalah implementasi **struktur data** untuk mendukung fitur-fitur utama aplikasi note-taking modern, mencakup:

- **Multi-linked list** untuk tagging sistem
- **Doubly Linked List** untuk tampilan kronologis & alfabetis
- **Circular Buffer** untuk pelacakan status sinkronisasi

Dibuat sebagai latihan perancangan struktur data dalam konteks aplikasi nyata.

---

## 🏗️ Arsitektur Struktur Data

```
NoteTakingApp
│
├── notes: dict[note_id → NoteNode]
│     └── NoteNode
│           ├── prev_chron / next_chron  ──► Doubly Linked List (Chronological)
│           ├── prev_alpha / next_alpha  ──► Doubly Linked List (Alphabetical)
│           └── tags: [tag_name, ...]   ──► Multi-linked by Tag
│
├── tags: dict[tag_name → TagNode]
│     └── TagNode
│           └── notes: [NoteNode, ...]  ──► Referensi ke semua note bertag ini
│
└── sync_buffer: deque(maxlen=N)        ──► Circular Buffer (recent changes)
```

---

## ✨ Fitur

| Fitur | Struktur Data | Keterangan |
|---|---|---|
| Multiple tags per note | **Multi-linked List** | Satu note bisa punya banyak tag; satu tag menghubungkan banyak note |
| Tampilan kronologis | **Doubly Linked List** | Traversal maju (terbaru) & mundur (terlama) |
| Tampilan alfabetis | **Doubly Linked List** | Insert terurut berdasarkan judul note |
| Sync status tracking | **Circular Buffer** | Menyimpan N perubahan terakhir, entri lama otomatis terganti |

---

## 🗂️ Struktur File

```
note-taking-ds/
│
├── main.py          # Implementasi utama + demo
└── README.md        # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan

### Prasyarat

- Python **3.7+**
- Tidak memerlukan library eksternal (hanya `collections` & `datetime` dari stdlib)

### Jalankan

```bash
python main.py
```

### Contoh Output

```
[+] Note ditambahkan: Note(N001, 'Belajar Python', tags=['python', 'belajar'])
[+] Note ditambahkan: Note(N002, 'Algoritma Sort', tags=['algo', 'belajar'])
...

=== Chronological View ===
  [10:01:00] Belajar Python   | tags: ['python', 'belajar']
  [10:01:01] Algoritma Sort   | tags: ['algo', 'belajar']
  [10:01:02] Database Dasar   | tags: ['db', 'belajar']
  ...

=== Alphabetical View ===
  Algoritma Sort   | tags: ['algo', 'belajar']
  API REST Design  | tags: ['web', 'algo']
  Belajar Python   | tags: ['python', 'belajar']
  ...

=== Notes dengan tag 'python' ===
  Note(N001, 'Belajar Python', ...)
  Note(N004, 'Flask Web App', ...)

=== Sync Buffer (Recent Changes) ===
  N001 | ADD | ✗ Pending
  N002 | ADD | ✗ Pending
  ...
[✓] Note N001 ditandai synced.
```

---

## 🔍 Penjelasan Komponen

### `NoteNode`
Node utama yang merepresentasikan satu catatan. Memiliki pointer ganda untuk dua doubly linked list (kronologis & alfabetis) sekaligus.

### `TagNode`
Menyimpan referensi ke semua `NoteNode` yang memiliki tag tertentu — membentuk **multi-linked structure** antar note melalui tag.

### `NoteTakingApp`
Kelas utama yang mengorkestrasi semua struktur data:
- `add_note()` — menambah note, otomatis masuk ke semua struktur
- `view_chronological()` — traversal DLL kronologis
- `view_alphabetical()` — traversal DLL alfabetis
- `get_notes_by_tag()` — query multi-linked list berdasarkan tag
- `mark_synced()` — update status di circular buffer
- `view_sync_status()` — tampilkan isi circular buffer

---

## 📐 Kompleksitas

| Operasi | Time Complexity |
|---|---|
| Tambah note | O(n) — sorted insert alphabetical |
| Traversal kronologis / alfabetis | O(n) |
| Cari note by tag | O(1) lookup + O(k) iterasi |
| Sync buffer insert | O(1) — `deque` dengan maxlen |

---

## 🧠 Konsep yang Dipelajari

- Doubly Linked List dengan dua dimensi sorting
- Multi-linked list untuk relasi many-to-many (note ↔ tag)
- Circular buffer menggunakan `collections.deque` dengan `maxlen`
- Pointer management tanpa built-in container

---

## 📚 Referensi

- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)
- [Linked List — GeeksforGeeks](https://www.geeksforgeeks.org/data-structures/linked-list/)
- Slide latihan: *Rancang struktur data untuk aplikasi note-taking*

---

## 👤 Author

Farhan Bagas Firmansyah / 039

Dibuat sebagai latihan mata kuliah / studi mandiri **Struktur Data**.

---

## 📄 License

MIT License — bebas digunakan untuk keperluan belajar.
