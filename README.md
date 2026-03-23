# 🖱️ Lenovo Legion M300 RGB — Button Remapper

> 100% vibe coded. No cap.

Надоело что официальный софт от Lenovo почти ничего не умеет? Теперь можно запрограммировать **любую клавишу клавиатуры** прямо на мышку — на любую из 8 кнопок. Просто открываешь, выбираешь, нажимаешь Apply. Всё.

---

## ✨ Что умеет

- 🎹 Любая клавиша клавиатуры на любую кнопку мыши
- 🖱️ Переназначение кнопок мыши (левая, правая, средняя, вперёд, назад)
- 🎵 Медиаклавиши: громкость, плей/пауза, следующий/предыдущий трек, мьют
- ⚡ DPI Switch
- 🚫 Отключить любую кнопку
- 💾 Конфиг сохраняется при Apply — после перезапуска всё на месте
- 🚀 Не нужен Legion Software, никаких драйверов и фоновых сервисов

---

## 📥 Скачать

**[Скачать MemovoMemion300Binder.exe](../../releases/latest)** — Python не нужен, просто запускаешь.

---

## 🚀 Как пользоваться

1. Подключи мышь по USB
2. Запусти `MemovoMemion300Binder.exe`
3. Выбери действие для каждой кнопки из списка
4. Для клавиши клавиатуры — выбери "Keyboard Key...", кликни на поле справа и нажми нужную клавишу
5. Нажми **APPLY ALL**

---

## 🔧 Совместимость

| Устройство | Статус |
|---|---|
| Lenovo Legion M300 RGB (USB) | ✅ Проверено |
| Lenovo Legion M300s | ❓ Не проверено (вероятно работает) |

**Vendor ID:** `0x17ef` · **Product ID:** `0x60e4`

---

## 🛠️ Сборка из исходников

```bash
git clone https://github.com/aLegoz/memovo-memion-300-binder
cd memovo-memion-300-binder
pip install hidapi pynput pyinstaller
pyinstaller --onefile --windowed --name "MemovoMemion300Binder" memovo_binder.py
```

Результат: `dist/MemovoMemion300Binder.exe`

---

## 🔬 Как это работает

HID-протокол был реверс-инжинирен через захват USB-трафика с помощью **Wireshark + USBPcap** во время работы официального Legion Software. Все команды отправляются напрямую на мышь в виде 64-байтных HID-пакетов.

Полная документация протокола — в [ARCHITECTURE.md](ARCHITECTURE.md).

---

## ⚙️ Требования (запуск из исходников)

- Windows 10/11
- Python 3.8+
- `pip install hidapi pynput`

---

## ⚠️ Disclaimer

Программа отправляет сырые HID-команды напрямую на мышь. Используй на свой страх и риск. Автор не несёт ответственности за любые повреждения устройства.

---

## 🤖 Vibe coded

Весь проект сделан с помощью ИИ. Никакой ручной документации протокола — HID-пакеты реверс-инжинированы из Wireshark-дампов, остальное — вайбы.

---

## 🔍 Related searches

Lenovo Legion M300 RGB remap · Legion M300 RGB button binding · Legion M300 RGB alternative software · Legion mouse HID · M300 RGB keybind · Legion Zone alternative
