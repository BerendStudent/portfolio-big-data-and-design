async function startNew() {
  document.getElementById('status').textContent = ''
  const res = await fetch('/new', { method: 'POST' })
  if (!res.ok) {
    const err = await res.json().catch(()=>({error:'server error'}))
    document.getElementById('status').textContent = err.error || 'Failed to start game'
    return
  }
  const data = await res.json()
  cols = data.target_length || (data.masked && data.masked.length) || 5
  buildBoard()
  buildKeyboard()
  curRow = 0
  curCol = 0
}

function buildBoard() {
  const board = document.getElementById('board')
  board.innerHTML = ''
  boardRows = []
  for (let r = 0; r < ROWS; r++) {
    const row = document.createElement('div')
    row.className = 'board-row'
    row.style.setProperty('--cols', cols)
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement('div')
      cell.className = 'tile'
      cell.dataset.row = r
      cell.dataset.col = c
      row.appendChild(cell)
    }
    board.appendChild(row)
    boardRows.push(row)
  }
  updateCursor()
}

function buildKeyboard() {
  keyStates = {}
  const kb = document.getElementById('keyboard')
  kb.innerHTML = ''
  const rows = [
    'QWERTYUIOP',
    'ASDFGHJKL',
    'ZXCVBNM'
  ]

  const top = document.createElement('div')
  top.className = 'kbd-row'
  rows[0].split('').forEach(ch => {
    const b = document.createElement('button')
    b.className = 'kbd-key'
    b.dataset.key = ch
    b.textContent = ch
    b.addEventListener('click', () => handleKey(ch))
    top.appendChild(b)
  })
  kb.appendChild(top)

  const mid = document.createElement('div')
  mid.className = 'kbd-row'
  rows[1].split('').forEach(ch => {
    const b = document.createElement('button')
    b.className = 'kbd-key'
    b.dataset.key = ch
    b.textContent = ch
    b.addEventListener('click', () => handleKey(ch))
    mid.appendChild(b)
  })
  kb.appendChild(mid)

  const bot = document.createElement('div')
  bot.className = 'kbd-row'
  const enter = document.createElement('button')
  enter.className = 'kbd-key'
  enter.dataset.key = 'ENTER'
  enter.textContent = 'ENTER'
  enter.addEventListener('click', handleEnter)
  bot.appendChild(enter)

  rows[2].split('').forEach(ch => {
    const b = document.createElement('button')
    b.className = 'kbd-key'
    b.dataset.key = ch
    b.textContent = ch
    b.addEventListener('click', () => handleKey(ch))
    bot.appendChild(b)
  })

  const back = document.createElement('button')
  back.className = 'kbd-key'
  back.dataset.key = 'BACK'
  back.textContent = '←'
  back.addEventListener('click', handleBack)
  bot.appendChild(back)

  kb.appendChild(bot)
  refreshKeyboard()
}

function handleKey(letter) {
  if (curRow >= ROWS) return
  if (curCol >= cols) return
  const cell = boardRows[curRow].children[curCol]
  cell.textContent = letter
  cell.classList.add('active')
  curCol++
  updateCursor()
}

function handleBack() {
  if (curRow >= ROWS) return
  if (curCol <= 0) return
  curCol--
  const cell = boardRows[curRow].children[curCol]
  cell.textContent = ''
  cell.classList.remove('active')
  updateCursor()
}

async function handleEnter() {
  if (curCol !== cols) {
    flashRow(curRow)
    return
  }
  const guess = Array.from(boardRows[curRow].children).map(t => t.textContent || '').join('').toLowerCase()
  const res = await fetch('/guess', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word: guess })
  })
  if (!res.ok) {
    const err = await res.json().catch(()=>({error:'server error'}))
    document.getElementById('status').textContent = err.error || 'Server error on guess'
    return
  }
  const data = await res.json()
  if (data.error) {
    document.getElementById('status').textContent = data.error
    return
  }

  const masked = Array.isArray(data.masked) ? data.masked : []
  const incorrectly = Array.isArray(data.incorrectly_placed) ? data.incorrectly_placed.slice() : []
  const statuses = []
  for (let i = 0; i < cols; i++) {
    const ch = guess[i]
    if (masked[i] && masked[i].toLowerCase() === ch) {
      statuses.push('correct')
    } else {
      const idx = incorrectly.indexOf(ch)
      if (idx !== -1) {
        statuses.push('present')
        incorrectly.splice(idx, 1)
      } else {
        statuses.push('absent')
      }
    }
  }

  await revealRow(curRow, statuses)
  updateKeyboardForGuess(guess, statuses)

  if (data.victory) {
    document.getElementById('status').textContent = 'You won! ' + (data.target || '')
    curRow = ROWS
    return
  }

  curRow++
  curCol = 0
  if (curRow >= ROWS) {
    document.getElementById('status').textContent = 'Out of attempts. Answer: ' + (data.target || '')
  }
  updateCursor()
}

function revealRow(row, statuses) {
  return new Promise((resolve) => {
    const tiles = Array.from(boardRows[row].children)
    tiles.forEach((tile, i) => {
      setTimeout(() => {
        tile.classList.add('flip')
        setTimeout(() => {
          tile.classList.remove('flip')
          tile.classList.add(statuses[i])
          tile.classList.remove('active')
        }, 200)
        if (i === tiles.length - 1) setTimeout(resolve, 350)
      }, i * 180)
    })
  })
}

function updateKeyboardForGuess(guess, statuses) {
  for (let i = 0; i < guess.length; i++) {
    const ch = (guess[i] || '').toUpperCase()
    if (!ch) continue
    const st = statuses[i]
    const prev = keyStates[ch] || ''
    const prio = statePriority(prev)
    const newPrio = statePriority(st)
    if (newPrio >= prio) keyStates[ch] = st
  }
  refreshKeyboard()
}

function statePriority(s) {
  if (s === 'correct') return 3
  if (s === 'present') return 2
  if (s === 'absent') return 1
  return 0
}

function refreshKeyboard() {
  document.querySelectorAll('.kbd-key').forEach(k => {
    const key = k.dataset.key
    const st = keyStates[key] || ''
    k.classList.remove('correct', 'present', 'absent')
    if (st) k.classList.add(st)
  })
}

function updateCursor() {
  document.querySelectorAll('.tile').forEach(t => t.classList.remove('active'))
  if (curRow < ROWS) {
    for (let c = 0; c < cols; c++) {
      const t = boardRows[curRow].children[c]
      if (t && !t.textContent) { t.classList.add('active'); break }
    }
  }
}

function flashRow(r) {
  const row = boardRows[r]
  if (!row) return
  row.classList.add('shake')
  setTimeout(() => row.classList.remove('shake'), 500)
}