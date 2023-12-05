const nameField = document.getElementById('name-field')
const mdField = document.getElementById('md-field')

const toolbar = document.getElementById('toolbar')
const boldButton = document.getElementById('bold-button')
const italicButton = document.getElementById('italic-button')
const headerButton1 = document.getElementById('header-1-button')
const headerButton2 = document.getElementById('header-2-button')
const headerButton3 = document.getElementById('header-3-button')
const youtubeButton = document.getElementById('yt-button')
const strikeButton = document.getElementById('strike-button')
const quoteButton = document.getElementById('quote-button')
const articleForm = document.getElementById('article-form')
const linkButton = document.getElementById('link-button')
const imageButton = document.getElementById('image-button')


String.prototype.insert = function(index, string) {
  if (index > 0)
  {
    return this.substring(0, index) + string + this.substring(index, this.length);
  }

  return string + this;
}

function AddTag(openTag, exampleWord, closeTag, isNewLineTag) {
    let selectedText = mdField.selectionStart === mdField.selectionEnd ? exampleWord : mdField.value.slice(mdField.selectionStart, mdField.selectionEnd)
    let cursorStart = mdField.selectionStart + openTag.length
    let cursorEnd = mdField.selectionStart + openTag.length + selectedText.length
    if (isNewLineTag) {
        let splitterStart = mdField.value[mdField.selectionStart - 1] === '\n' ? '\n' : '\n\n'
        let splitterEnd = '\n\n'
        if (mdField.value === '' || selectedText.length === mdField.value.length) {
            mdField.setRangeText(openTag + selectedText + closeTag)
            cursorStart = mdField.selectionStart + openTag.length
            cursorEnd = mdField.selectionStart + openTag.length + + selectedText.length
        }
        else if (mdField.selectionStart === mdField.value.length){
            mdField.setRangeText(splitterStart + openTag + selectedText + closeTag)
            cursorStart = mdField.selectionStart + openTag.length + splitterStart.length
            cursorEnd = mdField.selectionStart + openTag.length + splitterStart.length + selectedText.length
        }
        else {
            mdField.setRangeText(splitterStart + openTag + selectedText + closeTag + splitterEnd)
            cursorStart = mdField.selectionStart + openTag.length + splitterStart.length
            cursorEnd = mdField.selectionStart + openTag.length + + splitterStart.length + selectedText.length
        }

    }
    else if (!isNewLineTag) {
        mdField.setRangeText(openTag + selectedText + closeTag)
    }
    mdField.parentNode.dataset.replicatedValue = mdField.value
    mdField.setSelectionRange(cursorStart, cursorEnd)
    mdField.focus()
}


document.addEventListener(
    'keydown',
    function (event) {
        if (event.key === 'Backspace' || event.key === 'Delete') {
            if (document.activeElement === mdField && mdField.value === '') {
                event.preventDefault()
                nameField.focus()
        }
    }
}
)

document.addEventListener(
    'keydown',
    function (event) {
        if (event.key === 'Enter') {
            if (document.activeElement === nameField) {
                event.preventDefault()
                mdField.focus()
        }
    }
}
)

mdField.onfocus = function () {
    toolbar.style.display = 'flex'
    articleForm.style.marginTop = '0'
}

window.onresize = function () {
    mdField.parentNode.dataset.replicatedValue = mdField.value
}

window.onload = function () {
    mdField.parentNode.dataset.replicatedValue = mdField.value
}

nameField.onfocus = function () {
    toolbar.style.display = 'none'
    articleForm.style.marginTop = '20px'
}

boldButton.parentNode.onclick = () => AddTag('**', 'жирный текст', '**', false)

italicButton.parentNode.onclick = () => AddTag('*', 'курсивный текст', '*', false)

headerButton1.parentNode.onclick = () => AddTag('# ', 'главный заголовок', '', true)

headerButton2.parentNode.onclick = () => AddTag('## ', 'второстепенный заголовок', '', true)

headerButton3.parentNode.onclick = () => AddTag('### ', 'заголовок 3 уровня', '', true) 

youtubeButton.parentNode.onclick = () => AddTag('![youtube](', 'ссылка', ')', true)

strikeButton.parentNode.onclick = () => AddTag('~~', 'зачеркнутый текст', '~~', false)

linkButton.parentNode.onclick = () => AddTag('[', 'гипертекст', '](ссылка)', false)

imageButton.parentNode.onclick = () => AddTag('![подпись](', 'ссылка', ')', true)

quoteButton.parentNode.onclick = () => AddTag('> ', 'цитата', '', true)